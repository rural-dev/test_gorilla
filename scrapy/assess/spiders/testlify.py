import json
import scrapy
from ..utils import clean


class TestlifySpider(scrapy.Spider):
    name = 'testlify'
    cookies = {}

    def start_requests(self):
        headers = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9,id;q=0.8,ms;q=0.7",
                "content-type": "multipart/form-data; boundary=----WebKitFormBoundarymROcd7tssnXaii6S",
                "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            }

        url = 'https://testlify.com/?wpgb-ajax=render'
        meta = {'handle_httpstatus_all': True}
        forms = {
            'wpgb': {"is_main_query": 0,
                     "main_query": [],
                     "permalink": "https://testlify.com/test-library/",
                     "facets": [1, 2, 3, 4, 5, 12],
                     "lang": "",
                     "id": 1
                     }
        }
        yield scrapy.FormRequest(
            method='POST',
            url=f'{url}',
            headers=headers,
            formdata=forms,
            callback=self.parse,
            dont_filter=True,
            meta=meta
        )

    def parse(self, response, **kwargs):
        # jsonresponse = json.loads(response.text)
        print(response.text)
        # for job in jsonresponse:
        #     yield job
