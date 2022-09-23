import json
import scrapy
import csv
from ..utils import clean

class VervoeSpider(scrapy.Spider):
    name = 'vervoe'

    def start_requests(self):
        yield scrapy.Request(
            url=f'https://vervoe.com/assessment-library/',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        links = response.xpath('//*[@id="all-assessments"]/div/div/div/div/div/section/div/div/div/section[1]/div/div/div/div[1]/div/h5/a/@href').getall()
        for link in links:
            yield scrapy.Request(
                url=f'{link}',
                callback=self.parse_detail,
                dont_filter=True,
            )

        next = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next:
            yield scrapy.Request(
                url=f'{next}',
                callback=self.parse,
                dont_filter=True,
            )

    def parse_detail(self, response, **kwargs):
        title = response.xpath('//h1/text()').get()
        author = response.xpath('//h6[contains(text(),"Author")]/parent::div/parent::div/following-sibling::div[1]/div/h6/a/text()').get()
        questions = response.xpath('//h6[contains(text(),"Questions")]/parent::div/parent::div/following-sibling::div[1]/div/h6/text()').get()
        question_types = response.xpath('//h6[contains(text(),"Questions")]/parent::div/parent::div/following-sibling::div[2]/div/div/a/text()').getall()
        skills = response.xpath('//h6[contains(text(),"Skills")]/parent::div/parent::div/following-sibling::div[1]/div/h6/text()').get()
        skill_types = response.xpath('//h6[contains(text(),"Skills")]/parent::div/parent::div/following-sibling::div[2]/div/div/a/text()').getall()
        summary = response.xpath('//h5[contains(text(),"Assessment Summary")]/parent::div/parent::div/following-sibling::div[1]/div').extract()
        skill_tested = response.xpath('//h5[contains(text(),"Skills tested in this assessment")]/parent::div/parent::div/following-sibling::div[1]/div').extract()
        what_test = response.xpath('//h5[contains(text(),"What to test with this assessment")]/parent::div/parent::div/following-sibling::div[1]/div').extract()

        yield {
            'url': response.request.url,
            'title': title,
            'author': author,
            'questions': questions,
            'question_types': question_types,
            'skills': skills,
            'skill_types': skill_types,
            'summary': summary,
            'skill_tested': skill_tested,
            'what_test': what_test
        }