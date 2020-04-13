import scrapy
import datetime
import json
import re
import sys


# def convert_to_json(file):
#     f = open(file, 'r')
#     data = f.read()
#     f.close()
#     json_file = json.loads(data)
#     with open('form_data.json', 'w') as fi:
#         fi.write(data)

#     return True



class WebSpider(scrapy.Spider):

    name = 'webspider'

    allowed_domains = ['tauntondeeds.com']
    start_urls =['http://www.tauntondeeds.com/Searches/ImageSearch.aspx']

    res_dict = {}
    classes = ['gridRow', 'gridAltRow']

    
    def open_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return data


    def parse(self, response):
        
        form_datas = [self.open_json('form_data.json'), self.open_json('form_data2.json')]

        for page in form_datas:

            yield scrapy.FormRequest(response.url, formdata=page, callback=self.parce_page)


    def parce_page(self, response):

        for cl in self.classes: 

            for el in response.xpath(f'.//div/table/tr[@class="{cl}"]'):
                
                res_list = el.xpath('.//td/text()').getall()

                date = res_list[1] 
                doc_type = res_list[2]

                book = None if ' ' else res_list[3]
                
                page_num = None if ' ' else res_list[4]
                
                doc_num = res_list[5]

                

                city = res_list[6]

                description = el.xpath('.//td/span/text()').get()
                
                try:
                    cost = float(re.search(r'[$].*', description).group(0).replace('$', ''))
                except AttributeError:
                    cost = None

                try:
                    street_address = re.search(r'^.+[,]', description).group(0).replace(',', '').strip()
                except AttributeError:
                    street_address = None
                
                try:
                    zip_value = re.search(r'\sSP\s\S+\s', description).group(0).replace(',', '').strip()
                except AttributeError:
                    zip_value = None

                try:
                    state = re.search(r'.STATE\s\S+\s', description).group(0).strip()
                except AttributeError:
                    state = None
               
                
                date = datetime.date(int(date[6:]), int(date[:2]), int(date[3:5]) )
                
                
                

                yield {
                    'datetime' : str(date),
                    'type': doc_type,
                    'book': book,
                    'page_num': page_num,
                    'doc_num': doc_num,
                    'city': city,
                    'description': description,
                    'cost': cost,
                    'street_address': street_address,
                    'state': state,
                    'zip': zip_value
                        }
               
                   

        