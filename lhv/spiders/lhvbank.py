import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from lhv.items import Article


class lhvbankSpider(scrapy.Spider):
    name = 'lhvbank'
    start_urls = ['https://lhv.co.uk/news/']

    def parse(self, response):
        links = response.xpath('//a[@class="arrow-bold"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2[@class="text-center margin-bottom-50"]//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="news-date"]/text()').get()
        if date:
            try:
                date = datetime.strptime(date.strip(), '%d.%m.%Y')
            except:
                date = datetime.strptime(date.strip(), '%d. %B %Y')

            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//article//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
