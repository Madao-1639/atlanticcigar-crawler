import scrapy
from atlanticcigar.items import ACitem

class AcspiderSpider(scrapy.Spider):
    name = 'ACspider'
    allowed_domains = ['atlanticcigar.com']
    base_url = 'https://atlanticcigar.com'
    brand_list = ['10 Packs','Baccarat Havana Selection']
    #start_urls = ['https://atlanticcigar.com/brands/']                 # Send a POST request rather than a GET request

    def start_requests(self):
        post_url = 'https://app.atlanticcigar.com/brands/branding.php'
        for i in range(1,7):
            yield  scrapy.FormRequest(url=post_url,formdata={'page':str(i)},callback=self.parse_post)

    def parse_post(self, response):
        for item in response.json():
            if item['name'] in self.brand_list:
                brand_url = self.base_url+item['custom_url']['url']
                yield scrapy.Request(url=brand_url,callback=self.brand_parse)
    
    def brand_parse(self,response):
        product_urls=response.xpath('.//div[@class="product-item-details"]//a[@href]/@href').getall()
        for product_url in product_urls:
            yield scrapy.Request(url=product_url,callback=self.product_parse)
        next_page = response.xpath('.//li[span[@class="pagination-current"]]/following-sibling::li[position()=1]/a/@href').get()
        if next_page != None:
            next_page = self.base_url+next_page
            yield scrapy.Request(url=next_page,callback=self.brand_parse)
        
    def product_parse(self,response):
        info_box = response.xpath('.//div[@class="product-info"]')
        title = info_box.xpath('.//h1[@class="product-title"]/text()').get()
        brand = info_box.xpath('.//a[@class="product-brand"]/text()').get()
        size = info_box.xpath('.//span[@class="product-detail-key" and text()="Size"]/following-sibling::span/text()').get()
        price = info_box.xpath('.//span[@class="price-value"]/text()').get().strip()
        item = ACitem(title=title,brand=brand,size=size,price=price)
        yield item
