import scrapy


class QuotesSpider(scrapy.Spider):
    name = "autotrader"
    global g_nextpage
    start_urls = [
        'http://www.autotrader.co.uk/content/suzuki',
    ]
    	    
    def parse(self, response):
        for i in response.css('article'):
            href= i.css("span.review-page--review-all-image > a::attr(href)").extract()
            #print ('href::',href[0])
            next_page = href[0] if len(href) > 0 else 'null'
            #print ('next_page::',next_page)
            if next_page is not None:
        	    next_page1 = response.urljoin(next_page)
        	    print ('next_page1::',next_page1)
        	    for  j in response.css('ul.proscons__proscons--list'):
		            	print ('j::',j)
		            	yield  {
		            		'text': j.css("ul.proscons__proscons--list > li > span::text").extract(),
      				}
            
            
      		
      		