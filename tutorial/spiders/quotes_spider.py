import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # guardando html capturado em um arquivo. desativado
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')

        # guardando dados peneirados em um arquivo.
        for quote_selector in response.xpath('//div[@class="quote"]'):
            # capturando para quote, o texto, autor e tags
            yield {
                'text': quote_selector.xpath(
                    './span[@class="text"]/text()'
                ).get(),
                'author': quote_selector.xpath('./span/small/text()').get(),
                'tags': quote_selector.xpath(
                    './div[@class="tags"]/text()'
                ).get(),
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        author_page_links = response.xpath(
            '//a[preceding::small[@class="author"]]')
        yield from response.follow_all(author_page_links, self.parse_author)

        next_page = response.xpath('//li[@class="next"]/a')
        if next_page is not None:
            yield response.follow_all(next_page, self.parse)

    def parse_author(self, response):
        def query_xpath(xpath):
            return response.xpath(xpath).get(default='').strip()

        yield {
            "name": query_xpath('//h3[@class="author-title"]/text()'),
            "birthdate": query_xpath('//span[@class="author-born-date"]/text()'),
            "bio": query_xpath('//div[@class="author-description"]/text()'),
        }
