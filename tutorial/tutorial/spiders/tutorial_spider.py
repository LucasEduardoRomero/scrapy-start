import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.zyte.com/blog/']

    def parse(self, response):
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)


class PostSpider(scrapy.Spider):
    name = 'postspider'
    start_urls = ['https://www.zyte.com/blog/']

    def parse(self, response):
        for title in response.css('.oxy-post-title'):
            yield response.follow(title, self.parse_post)

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        post_title = response.css('span#span-68-674.ct-span::text').get()
        post_first_text = response.css(
            'span.ct-span.oxy-stock-content-styles p:first-of-type::text'
        ).get()
        yield {"title": post_title, "first_text": post_first_text}
