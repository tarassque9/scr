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
    n = 0
    classes = ['gridRow', 'gridAltRow']

    
    def open_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return data


    def parse(self, response):
        
        #print(response.body)
        print('-----')


        page1 = self.open_json('form_data.json')
        page2 = self.open_json('form_data2.json')
        form_datas = [page1, page2]



        #formdata = formdata['__EVENTARGUMENT'] = 'Page$2'
        
        #yield scrapy.FormRequest(response.url, formdata=formdata, callback=self.parce_page, meta={'formdata': formdata})

        #page = response.meta['formdata']['__EVENTARGUMENT'] = 'Page$2'

        #yield scrapy.FormRequest(response.url, formdata={'__EVENTARGUMENT': 'Page$2'}, callback=self.parce)
        headers = {

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Length': '35683',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'ASP.NET_SessionId=h1qytrvdolryflhnz0yye0bt',
            'Host': 'www.tauntondeeds.com',
            'Origin': 'http://www.tauntondeeds.com',
            'Referer': 'http://www.tauntondeeds.com/Searches/ImageSearch.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'

        }

        for page in form_datas:
        

            yield scrapy.FormRequest(response.url, formdata=page, callback=self.parce_page)
        #yield scrapy.FormRequest(response.url, formdata=page, callback=self.parce_page)


    def parce_page(self, response):
        

        # print(response.meta['formdata']['__EVENTARGUMENT'])
        #print(response.meta['formdata'])

        for cl in self.classes: 

            for el in response.xpath(f'.//div/table/tr[@class="{cl}"]'):
                self.n += 1
                
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
            
                   

        