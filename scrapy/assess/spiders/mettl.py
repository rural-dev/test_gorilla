import json
import scrapy
from ..utils import clean


class MettlSpider(scrapy.Spider):
    name = 'mettl'

    def start_requests(self):
        url = 'https://mettl.com/preLogin/admin/pbt/getAddEditPreBuiltTestData?pbtId='
        for i in range(1, 1400):
            yield scrapy.Request(
                url=f'{url}{i}',
                callback=self.parse,
                dont_filter=True,
                cb_kwargs={'id': i}
            )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        if 'preBuitTestDetails' in jsonresponse:
            obj = jsonresponse["preBuitTestDetails"]
            for key, value in obj.items():
                if key == 'relatedPbtsNew':
                    rel = []
                    for pbt in obj[key]:
                        rel.append(pbt['pbtId'])
                    obj[key] = rel
                else:
                    obj[key] = clean(value)
            yield obj
