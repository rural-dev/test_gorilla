import json
import scrapy
from ..utils import clean


class ImochaSpider(scrapy.Spider):
    name = 'imocha'
    cookies = {}

    def start_requests(self):
        start_url = 'https://www.imocha.io/pre-employment-testing/all-tests'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8,ms;q=0.7',
            'content-length': '0',
            'content-type': 'application/json;charset=utf-8',
            'origin': 'https://www.imocha.io',
            'referer': 'https://www.imocha.io/pre-employment-testing/all-tests',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': "Android",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        url = 'https://www.imocha.io/pre-employment-testing/search-test-data'
        meta = {'handle_httpstatus_all': True}

        yield scrapy.Request(
            method='POST',
            headers=headers,
            url=f'{url}',
            callback=self.parse,
            dont_filter=True,
            meta=meta
        )

    def parse(self, response, **kwargs):
        # jsonresponse = json.loads(response.text)
        print(response.text)
        # for job in jsonresponse:
        #     yield job
