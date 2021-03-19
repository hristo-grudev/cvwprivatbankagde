import scrapy

from scrapy.loader import ItemLoader

from ..items import CvwprivatbankagdeItem
from itemloaders.processors import TakeFirst


class CvwprivatbankagdeSpider(scrapy.Spider):
	name = 'cvwprivatbankagde'
	start_urls = ['https://www.dje.de/unternehmen/aktuelles/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="orange-text"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="arr-right"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//ul[@class="breadcrumbs"]/li[position()=last()]/span/text()').get()
		description = response.xpath('//div[@class="article-text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//h3/text()').get().split('-')[0]

		item = ItemLoader(item=CvwprivatbankagdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
