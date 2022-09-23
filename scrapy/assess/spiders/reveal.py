import json
import scrapy
import csv
from ..utils import clean


class RevealSpider(scrapy.Spider):
    name = 'reveal'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }
    login_url = 'https://app.hiringindicators.com/Home/Login'
    username = 'azizsaefulhidayat@gmail.com'
    password = 'Yv3NpAXGW5pzAT7@'

    def start_requests(self):
        yield scrapy.Request(
            url=self.login_url,
            callback=self.parse_login,
            dont_filter=True,
        )

    def parse_login(self, response, **kwargs):
        token = response.xpath('//input[@name="__RequestVerificationToken"]/@value').get()
        form = {
            'Username': self.username,
            'Password': self.password,
            '__RequestVerificationToken': token,
        }
        yield scrapy.FormRequest(
            url=self.login_url,
            callback=self.loop_job,
            formdata=form,
            dont_filter=True,
        )

    def loop_job(self, response, **kwargs):
        for i in range(1, 2000):
            yield scrapy.Request(
                url=f'https://app.hiringindicators.com/organizations/positions/create/{i}',
                callback=self.parse,
                dont_filter=True,
                cb_kwargs={'id': i}
            )

    def parse(self, response, **kwargs):
        title = response.xpath('//input[@id="Title"]/@value').get()
        desc = response.xpath('//textarea[@id="Description"]/@value').get()
        token = response.xpath('//input[@name="__RequestVerificationToken"]/@value').get()
        form = {
            'Title': title,
            'Description': desc,
            'JobId': str(kwargs["id"]),
            '__RequestVerificationToken': token,
        }
        yield scrapy.FormRequest(
            url=f'https://app.hiringindicators.com/organizations/positions/create/{kwargs["id"]}',
            callback=self.parse_detail,
            formdata=form,
            dont_filter=True,
            cb_kwargs={'form': form}
        )

    def parse_detail(self, response, **kwargs):
        competency = response.xpath('//ul[@class="competency-list"]/li/text()').getall()
        form = kwargs['form']
        form.pop('__RequestVerificationToken')
        form['competency'] = competency
        yield form
