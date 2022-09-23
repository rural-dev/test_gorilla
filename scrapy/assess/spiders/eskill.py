import json
import scrapy
import csv
from ..utils import clean


class EskillSpider(scrapy.Spider):
    name = 'eskill'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }
    def start_requests(self):
        links = [
            {'id': 'Modular', 'link': 'https://es.eskill.com/es/subjects/export/json/Subjects.json'},
            {'id': 'Subject-Based', 'link': 'https://es.eskill.com/es/subjects/export/json/TestCategoriesWithSubjectBasedTests.json'},
            {'id': 'Job-Based', 'link': 'https://es.eskill.com/es/subjects/export/json/TestCategoriesWithJobBasedTests.json'},
        ]
        for idx, link in enumerate(links):
            yield scrapy.Request(
                url=f'{link["link"]}',
                callback=self.parse,
                dont_filter=True,
                cb_kwargs={'id': link['id'], 'idx': idx}
            )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        if kwargs['id'] == 'Modular':
            for cat_idx, category in enumerate(jsonresponse):
                cat_id = category['id']
                cat_name = category['name']
                subjects = category['subjects']
                for sbj_idx, subject in enumerate(subjects):
                    ids = subject['id']
                    name = subject['name']
                    language = subject['language']
                    topics = subject['topics']
                    yield {
                        'idx': kwargs['idx'],
                        'type': kwargs['id'],
                        'cat_idx': cat_idx,
                        'cat_id': cat_id,
                        'cat_name': clean(cat_name),
                        'sbj_idx': sbj_idx,
                        'id': ids,
                        'name': clean(name),
                        'language': language,
                        'topics': clean(topics),
                        'description': '',
                        'questionsCount': '',
                        'questionsTypes': '',
                    }
        else:
            for cat_idx, category in enumerate(jsonresponse):
                cat_id = category['id']
                cat_name = category['name']
                tests = category['tests']
                for sbj_idx, test in enumerate(tests):
                    ids = test['id']
                    name = test['name']
                    description = test['description']
                    questionsCount = test['questionsCount']
                    questionsTypes = test['questionsTypes']

                    yield {
                        'idx': kwargs['idx'],
                        'type': kwargs['id'],
                        'cat_idx': cat_idx,
                        'cat_id': cat_id,
                        'cat_name': clean(cat_name),
                        'sbj_idx': sbj_idx,
                        'id': ids,
                        'name': clean(name),
                        'language': '',
                        'topics': '',
                        'description': clean(description),
                        'questionsCount': questionsCount,
                        'questionsTypes': questionsTypes,
                    }
