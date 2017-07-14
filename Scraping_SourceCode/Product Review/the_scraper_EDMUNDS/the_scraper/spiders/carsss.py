# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
import os
import sys

class CarsSpider(scrapy.Spider):

    name = 'cars'

    def __init__(self):
        self.base_url = 'https://www.edmunds.com'
        self.year_links = []
        self.data = {}
        if not os.path.isdir('/tmp/cars'):
            os.makedirs('/tmp/cars')

    def start_requests(self):
        car_make = ["acura", "alfa-romeo", "aston-martin", "audi", "bentley", "bmw", "buick",
        "cadillac", "chevrolet", "chrysler", "dodge", "ferrari", "fiat", "ford", "genesis",
        "gmc", "honda", "hyundai", "infiniti", "jaguar", "jeep", "kia", "lamborghini",
        "land-rover", "lexus", "lincoln", "lotus", "maserati", "mazda", "mclaren", "mercedes-benz",
        "mini", "mitsubishi", "nissan", "porsche", "ram", "rolls-royce", "scion", "smart", "subaru",
        "tesla", "toyota", "volkswagen", "volvo"]

        for make in car_make:
            yield scrapy.Request(url="%s/%s/" % (self.base_url, make), callback=self.model_parse)

    def model_parse(self, response):
        models = response.selector.xpath('//div[@class="yui-content"]').xpath('//div[@class="card-container"]/a/@href').extract()
        for model in models:
            yield scrapy.Request('%s%s' % (self.base_url, model), callback=self.year_parse)

    def year_parse(self, response):
        data = {}
        make_years = response.selector.xpath('//div[@class="years"]').xpath('//li[@class="year_matrix"]/a/@href').extract()
        for link in make_years:
            yield scrapy.Request(link, callback=self.parse_pro_cons)

    def parse_pro_cons(self, response):
        pros_and_cons = response.selector.xpath('//div[@class="row container pros-cons-content"]/div')
        pros = pros_and_cons[0].xpath('./ul/li/text()').extract()
        cons = pros_and_cons[1].xpath('./ul/li/text()').extract()
        item = {}
        url_split = response.url.split('/')
        item['make'] = url_split[3]
        item['model']= url_split[4]
        item['year']= url_split[5]
        item['pros']= pros
        item['cons']= cons
        orig_stdout = sys.stdout
        f = open("out.txt", 'a')
        sys.stdout = f
        print (item)
        sys.stdout = orig_stdout
        f.close()
        return item
