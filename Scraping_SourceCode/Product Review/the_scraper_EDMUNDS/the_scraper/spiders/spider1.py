# -*- coding: utf-8 -*-
import scrapy


class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    # lines = [line.rstrip('\n') for line in open('abc.txt')]
    # for names in [line.rstrip('\n') for line in open('abc.txt')]:
    #     print("()()()()"+names+"()()()()")
    start_urls = [
        'https://www.edmunds.com/toyota/4runner/2017',
        # 'https://www.edmunds.com/honda/',
        # 'https://www.edmunds.com/ford/',
    ]
    def parse(self, response):
        for quote in response.xpath('//div[@class="row container pros-cons-content"]'):
            # review_link = quote.xpath('//div[@class="card-container"]/div[@class="card-img"]/a[@href]/text()').extract()
            # print ("[[[[]]]]"+str(review_link)+"[[[[]]]]")
            yield {
                'pros': quote.xpath('./div[contains(h3,\'pros\')]/ul/li/text()').extract(),
                'cons': quote.xpath('./div[contains(h3,\'cons\')]/ul/li/text()').extract()
                # 'href': quote.xpath('./div[@class="card-img"]/a//@href/text()').extract()
            }
            # next_page_url = str(review_link[0])1111
            # print ("----------"+next_page_url+"----------")
            # if next_page_url is not None:
            #     yield scrapy.Request(response.urljoin(next_page_url))
    # def parse(self, response):
    #     for quote in response.xpath('//div[@class="col-make"]/select/option[@class="bg-white medium text-capitalize"]'):
    #         op = str(quote.xpath('//div[@class="col-make"]/select/option[@class="bg-white medium text-capitalize"]/text()').extract_first())
    #         print ("$$$$$$$"+op+"$$$$$$$")
    #         yield {
    #             'options': quote.xpath('//div[@class="col-make"]/select/option[@class="bg-white medium text-capitalize"]/text()').extract()
    #         }
    #         next_page_url = op[0]
    #         if next_page_url is not None:
    #             yield scrapy.Request(response.urljoin(next_page_url))
