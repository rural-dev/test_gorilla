import json
import scrapy
from ..utils import clean


class MekiPeopleSpider(scrapy.Spider):
    name = 'mekipeople'

    def start_requests(self):
        url = 'https://www.makipeople.com/tests'
        yield scrapy.Request(
            url=f'{url}',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        for idx, link in enumerate(response.xpath("//div[@role='listitem']/div/div[2]/a/@href").getall()):
            detail_page = response.urljoin(link)
            yield scrapy.Request(detail_page, callback=self.parse_detail, cb_kwargs={'idx': idx, 'url': response.request.url})
        next_page = response.xpath('//a[@aria-label="Next Page"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response, **kwargs):
        title = response.xpath('//h1/text()').get()
        desc = response.xpath('//html/body/div[1]/header/div/div/div/div[1]/div[2]/p/text()').get()
        tags = response.xpath('//div[@class="hero-tags-text"]/text()').getall()
        skills = response.xpath('//html/body/div[1]/header/div/div/div/div[1]/div[7]/div/div[2]/div/div/div/text()').getall()
        jobs = response.xpath('//html/body/div[1]/header/div/div/div/div[1]/div[8]/div/div[2]/div/div/div/text()').getall()
        image = response.xpath('//html/body/div[1]/header/div/div/div/div[2]/div/div/img/@src').extract()
        auth_title = response.xpath('//html/body/div[1]/section[1]/div/div/div/div[2]/div/div[1]/h2/text()').get()
        auth_image = response.xpath('//html/body/div[1]/section[1]/div/div/div/div[1]/div/img/@src').extract()
        auth_name = response.xpath('//div[@class="about-author-name"]/text()').get()
        auth_job = response.xpath('//div[@class="about-author-job"]/text()').get()
        auth_desc = response.xpath('//html/body/div[1]/section[1]/div/div/div/div[2]/div/div[2]/div[3]/p/text()').get()

        yield {
            'source': kwargs['url'],
            'idx': kwargs['idx'],
            'url': response.request.url,
            'title': title,
            'desc': desc,
            'tags': tags,
            'skills': skills,
            'jobs': jobs,
            'image': image,
            'auth_title': auth_title,
            'auth_image': auth_image,
            'auth_name': auth_name,
            'auth_job': auth_job,
            'auth_desc': auth_desc,
        }