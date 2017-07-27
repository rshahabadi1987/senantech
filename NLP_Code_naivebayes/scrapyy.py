# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
import os
import sys
import csv

class CarsSpider(scrapy.Spider):
    name = 'car_review'

    def __init__(self):
        self.base_url = 'https://www.edmunds.com'

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
        make_years = response.selector.xpath('//div[@class="years"]').xpath('//li[@class="year_matrix"]/a/@href').extract()
        for link in make_years:
            yield scrapy.Request(link, callback=self.parse_cus_review_link)


    def parse_cus_review_link(self, response):
        # make_review_links = response.url+"consumer-reviews/pg-1/?sorting=CONFIDENCE"
        make_review_links = ["consumer-reviews/pg-1/?sorting=CONFIDENCE", "consumer-reviews/pg-2/?sorting=CONFIDENCE", "consumer-reviews/pg-3/?sorting=CONFIDENCE", "consumer-reviews/pg-4/?sorting=CONFIDENCE"]
        for make_links in make_review_links:
            yield scrapy.Request(response.url+make_links, callback=self.parse_get_review)

    def parse_get_review(self, response):
        var_review = response.selector.xpath('//div/div[contains(h3/strong,\'Review\')]/p/text()').extract()
        # var_review = response.selector.xpath('//div[@class="individual-overal-rating"]/span[@class="reviewTitle"]/strong/text()').extract()
        var_rating = response.selector.xpath('//div[@class="individual-overal-rating"]/div/span/@title').extract()
        # item = {}
        url_split = response.url.split('/')
        # item['make'] = url_split[3]
        # item['model']= url_split[4]
        # item['year']= url_split[5]
        # item['review']= var_review
        # item['rating']= var_rating
        count = 0
        orig_stdout = sys.stdout
        f = open("ratingandreview_fix.txt", 'a')
        sys.stdout = f
        for i in var_rating:
            # print ("{ \"Rating\" : "+var_rating[count]+", \"Review\" : "+var_review[count]+"} ,")
            myreview = var_review[count]._replace('\n',' ').replace('\r','')
            print (url_split[3]+"#"+url_split[4]+"#"+url_split[5]+"#"+var_rating[count]+"#"+myreview)
            count=count+1
        sys.stdout = orig_stdout
        f.close()
        item = {}

        return item
