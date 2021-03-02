import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AosFatosSpider(scrapy.Spider):
    name = 'fatos'

    allowed_domains = ['aosfatos.org']
    start_urls = ['https://www.aosfatos.org/']

    def parse(self, response):
        links = response.xpath(
            '//nav/ul//li/a[re:test(@href, "checamos")]/@href'
        ).getall()
        if(links is not None):
            yield from response.follow_all(links, self.parse_category)

    def parse_category(self, response):
        cards = response.xpath(
            '//a[@class="entry-card infinite-item "]/@href'
        ).getall()
        if(cards is not None):
            yield from response.follow_all(cards, self.parse_fato)

        next_btn = response.xpath('//a[@class="next-arrow"]/@href').getall()
        if(next_btn is not None):
            yield from response.follow_all(next_btn, self.parse_category)

    def parse_fato(self, response):
        title = response.xpath(
            '//article[@class="ck-article"]/h1/text()').get()
        date = response.xpath('//p[@class="publish_date"]/text()').get()
        url = response.url

        citacao = response.xpath('//article//blockquote//p')
        for cit in citacao:
            cit_text = cit.xpath('./text()').getall()
            cit_status = cit.xpath(
                './parent::blockquote//preceding-sibling::figure/figcaption/figure/figcaption/text()'
            ).get()
            if(cit_status is None):
                cit_status = cit.xpath(
                    './parent::blockquote//preceding-sibling::p'
                )[-2].xpath('./text()').get()
            if(cit_status is None):
                continue

            yield {
                'title': title,
                'date': date,
                'url': url,
                'citacao': cit_text,
                'status': cit_status,
            }


class AosFatosCrawler(CrawlSpider):
    name = 'fatos_crawler'

    allowed_domains = ['aosfatos.org']
    start_urls = ['https://www.aosfatos.org/']

    rules = (
        # Rule(
        #     LinkExtractor(
        #         restrict_xpaths=('//li[contains(text(), "Checamos")]//ul/li')
        #     ),
        #     callback='parse_category'
        # ),
        Rule(
            LinkExtractor(
                restrict_xpaths=('//nav/ul//li/a[re:test(@href, "checamos")]')
            ),
            callback='parse_category'
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths=('//a[@class="next-arrow"]')
            ),
            callback='parse_category'
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths=(
                    '//a[@class="card"]',
                    '//a[@class="entry-card infinite-item "]',
                )
            ),
            callback='parse_fato'
        )
    )

    def parse_category(self, response):
        cards = response.xpath(
            '//a[@class="entry-card infinite-item "]/@href'
        ).getall()
        if(cards is not None):
            yield from response.follow_all(cards, self.parse_fato)

        next_btn = response.xpath('//a[@class="next-arrow"]/@href').getall()
        if(next_btn is not None):
            yield from response.follow_all(next_btn, self.parse_category)

    def parse_fato(self, response):
        title = response.xpath(
            '//article[@class="ck-article"]/h1/text()').get()
        date = response.xpath('//p[@class="publish_date"]/text()').get()
        url = response.url

        citacao = response.xpath('//article//blockquote//p')
        for cit in citacao:
            cit_text = cit.xpath('./text()').getall()
            cit_status = cit.xpath(
                './parent::blockquote//preceding-sibling::figure/figcaption/figure/figcaption/text()'
            ).get()
            if(cit_status is None):
                cit_status = cit.xpath(
                    './parent::blockquote//preceding-sibling::p'
                )[-2].xpath('./text()').get()
            if(cit_status is None):
                continue

            yield {
                'title': title,
                'date': date,
                'url': url,
                'citacao': cit_text,
                'status': cit_status,
            }
