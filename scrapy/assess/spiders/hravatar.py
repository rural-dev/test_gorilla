import scrapy
from scrapy import Selector

from ..utils import clean

class HRAvatarSpider(scrapy.Spider):
    name = 'hravatar'
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 1
    }
    def start_requests(self):
        cookies = {
            'hravataruid': 'duid81663311141328',
            'hravatarcpid': 'prodvwsrvlt',
            'hrackiewrng': '1',
            'primefaces.download_catalog_producttop.xhtml': 'true',
            'JSESSIONID': '34123bd890d7a44bdd7008c3f05e',
            '_ga': 'GA1.2.1872247515.1663311135',
            '_gid': 'GA1.2.1474578472.1663543863',
            '_gat_gtag_UA_52538012_1': '1',
            'AWSALB': '5IsAKHWkAL9BRBK7AzQPFO3nzOPfxktWMg1lt7BIun5X/uC/fwKWe2ZtHURvrx+oKVsu/fFz1qkbrG0KcQsTLA0L31Cx7z8rtTxpdEibSLdDCXq4eVVc54u1WwI4',
            'AWSALBCORS': '5IsAKHWkAL9BRBK7AzQPFO3nzOPfxktWMg1lt7BIun5X/uC/fwKWe2ZtHURvrx+oKVsu/fFz1qkbrG0KcQsTLA0L31Cx7z8rtTxpdEibSLdDCXq4eVVc54u1WwI4'
        }
        header = {
            "accept": "application/xml, text/xml, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9,id;q=0.8,ms;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "faces-request": "partial/ajax",
            "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }
        form = {
            'javax.faces.partial.ajax': 'True',
            'javax.faces.source': 'productlisttable',
            'javax.faces.partial.execute': 'productlisttable',
            'javax.faces.partial.render': 'productlisttable',
            'productlisttable': 'productlisttable',
            'productlisttable_pagination': 'True',
            'productlisttable_first': '0',
            'productlisttable_rows': '25',
            'productlisttable_skipChildren': 'True',
            'productlisttable_encodeFeature': 'True',
            'j_idt202': 'j_idt202',
            'vtzo': '-300',
            'vtzid': 'America/Chicago',
            'javax.faces.ViewState': '-9083303727645994305:134279373493924987'
        }
        for i in range(0, 18):
            copy_form = form.copy()
            copy_form['productlisttable_first'] = str(i * 25)
            yield scrapy.FormRequest(
                url=f'https://www.hravatar.com/ta/catalog/producttop.xhtml',
                headers=header,
                cookies=cookies,
                formdata=copy_form,
                callback=self.parse,
                dont_filter=True,
                cb_kwargs=({"page": i})
            )

    def parse(self, response, **kwargs):
        data = Selector(text=response.xpath('//partial-response/changes/update/text()').extract()[1])
        links = data.xpath('//tr[@role="row"]/td/div/@onclick').getall()
        for idx, link in enumerate(links):
            l = link.replace("location.href='", "").replace("'", "")
            yield scrapy.Request(
                url=f'https://www.hravatar.com{l}',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs=({"page": kwargs["page"], "idx": idx})
            )

    def parse_detail(self, response, **kwargs):
        title = response.xpath('//h1/text()').get()
        subtitle = response.xpath('//h2/text()').get()
        descriptop = response.xpath('//p[@class="proddescriptop"]/b/text()').get()
        jobdescrip = " ".join(response.xpath('//div[@itemtype="http://schema.org/Product"]/p').getall())
        activities = response.xpath(
            '//span[contains(text(),"Top activities and tasks for this job")]/following-sibling::ul[1]/li/text()').getall()
        cognitive = response.xpath(
            '//span[contains(text(),"Cognitive Ability")]/following-sibling::ul[1]/li/text()').getall()
        skills = response.xpath(
            '//span[contains(text(),"Knowledge and Skills")]/following-sibling::ul[1]/li/text()').getall()
        personality = response.xpath(
            '//span[contains(text(),"Personality")]/following-sibling::ul[1]/li/text()').getall()
        emotional = response.xpath(
            '//span[contains(text(),"Emotional Intelligence")]/following-sibling::ul[1]/li/text()').getall()
        behaviour = response.xpath(
            '//span[contains(text(),"Behavioral History")]/following-sibling::ul[1]/li/text()').getall()
        language = response.xpath('//td[contains(text(),"Language:")]/following-sibling::td[1]/text()').get()
        time = response.xpath('//td[contains(text(),"Time to Complete:")]/following-sibling::td[1]/text()').get()
        specifications = response.xpath('//td[contains(text(),"Specifications:")]/following-sibling::td[1]/text()').get()

        soc = response.xpath('//td[contains(text(),"O*Net SOC Code:")]/following-sibling::td[1]/text()').get()
        simulation = response.xpath(
            '//td[contains(text(),"Simulation Context:")]/following-sibling::td[1]/text()').get()
        context = response.xpath('//td[contains(text(),"O*Net Context:")]/following-sibling::td[1]/text()').get()
        top_knowledge = response.xpath('//div[contains(text(),"Top Knowledge Requirements")]/ul/li/text()').getall()
        top_skills = response.xpath('//div[contains(text(),"Top Skills")]/ul/li/text()').getall()
        top_abilities = response.xpath('//div[contains(text(),"Top Abilities")]/ul/li/text()').getall()

        yield {
            'page': kwargs["page"],
            'idx': kwargs["idx"],
            'url': response.request.url,
            'title': title,
            'subtitle': subtitle,
            'descriptop': descriptop,
            'jobdescrip': jobdescrip,
            'activities': activities,
            'cognitive': cognitive,
            'skills': skills,
            'personality': personality,
            'emotional': emotional,
            'behaviour': behaviour,
            'language': language,
            'time': time,
            'specifications': specifications,
            'soc': soc,
            'simulation': simulation,
            'context': context,
            'top_knowledge': top_knowledge,
            'top_skills': top_skills,
            'top_abilities': top_abilities,
        }
