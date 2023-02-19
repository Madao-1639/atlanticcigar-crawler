# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook

class AtlanticcigarPipeline:
    def __init__(self):
        self.wb = Workbook()
        self.wb.create_sheet("product_info")
        self.ws = self.wb["product_info"]
        self.ws.append(
            ['title','brand', 'size', 'price'])
        
    def process_item(self, item, spider):
        self.ws.append([item['title'], item['brand'], item['size'], item['price']])
     
    def close_spider(self, spider):
        self.wb.save('result.xlsx')
