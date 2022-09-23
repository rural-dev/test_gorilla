import json
import scrapy
from ..utils import clean


class TestDomeSpider(scrapy.Spider):
    name = 'testdome'

    def start_requests(self):
        url = 'https://testdome.com/api/v3/generators?$skip=0&$top=1000'
        yield scrapy.Request(
            url=f'{url}',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        if 'value' in jsonresponse:
            tests = jsonresponse["value"]
            for test in tests:
                detail_page = response.urljoin(test['url'])
                yield scrapy.Request(
                    url=f'{detail_page}',
                    callback=self.parse_detail,
                    dont_filter=True,
                    cb_kwargs={'source': test}
                )

    def parse_detail(self, response, **kwargs):
        title = response.xpath('//h1/text()').get()
        desc = " ".join(response.xpath('//*[@id="app"]/main/div/div[2]/div/section[1]/div/*').extract())
        questions = response.xpath('//*[@id="app"]/main/div/div[2]/div/section[2]/div')
        for idx, q in enumerate(questions):
            if q.xpath('.//div/div/div[1]/div[1]/div/div/a/text()').get():
                yield {
                    'url': response.request.url,
                    'id': kwargs['source']['id'],
                    'name': kwargs['source']['name'],
                    'skill': kwargs['source']['skill'],
                    'secondarySkills': kwargs['source']['secondarySkills'],
                    'descriptionHtml': kwargs['source']['descriptionHtml'],
                    'metaDescription': kwargs['source']['metaDescription'],
                    'tags': kwargs['source']['tags'],
                    'generatorCategories': kwargs['source']['generatorCategories'],
                    'supportedDifficulties': kwargs['source']['supportedDifficulties'],
                    'detail_page_title': title,
                    'detail_page_desc': desc,
                    'question_idx': idx,
                    'question_title': clean(q.xpath('.//div/div/div[1]/div[1]/div/div/a/text()').get()),
                    'question_diff': clean(q.xpath('.//div/div/div[1]/div[2]/div/div[1]/span/span/text()').get()),
                    'question_time': clean(q.xpath('.//div/div/div[1]/div[2]/div/div[2]/span/span/text()').get()),
                    'question_type': clean(q.xpath('.//div/div/div[1]/div[2]/div/div[3]/div/span/span/text()').get()),
                    'question_public': clean(q.xpath('.//div/div/div[1]/div[2]/div/div[4]/span/span/text()').get()),
                    'question_skills': clean(q.xpath('.//div/div/div[1]/div[3]/div/div/span/text()').getall()),
                    'question_desc': clean(" ".join(q.xpath('.//div/div/div[2]/*').extract())),
                    'question__link': clean(q.xpath('.//div/div/div[3]/div/a/@href').get()),
                }