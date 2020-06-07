import scrapy
import os

base = 'https://www.thestar.com.my/search?pgno={number}&q=undocumented&qsort=newest&qrec=10&qstockcode='
url_list = []
for i in range(1, 4):
    url_list.append(base.format(number=str(i)))


def runSpider(url_list, url_tags, title_tag, region_tag, date_tag, text_tag, output_file):
    """
    This function runs a scrapy command in the terminal which 
    takes our list of urls, title, region, text and date tags and 
    then parses it into the scrapy shell. It then spits out a json file which 
    contains the output of our scrape. 
    """
    stringy_url_list = ','.join(url_list)
    os.system("scrapy crawl news -a url_list='{url_list}' -a url_tags='{url_tags}' -a title_tag='{title_tag}' -a region_tag='{region_tag}' -a date_tag='{date_tag}' -a text_tag='{text_tag}' -o {output_file}".format(url_list=stringy_url_list, url_tags=url_tags, title_tag=title_tag, region_tag=region_tag, text_tag=text_tag, date_tag=date_tag, output_file=output_file))
     

class HistoricalSpider(scrapy.Spider):
    """
    This spider scrapes news articles by first generating the list of links in the 
    search page. Then, it parses through those links via the call back to 
    to get the page specific information. 
    """

    name = 'news'  

    def __init__(self, *args, **kwargs): 
        super(HistoricalSpider, self).__init__(*args, **kwargs) 
        self.start_urls = url_list 

    def parse(self, response):
        urls = response.xpath(self.url_tags).extract()
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse_details)

    def parse_details(self, response):
        yield {
                'title': response.xpath(self.title_tag).extract_first(),
                'region': response.xpath(self.region_tag).extract_first(), 
                    'date': response.xpath(self.date_tag).extract_first(),  
                    'text': ' '.join(response.xpath(self.text_tag).extract()), 
                    }

 
star_urls ='//*[@class="f18"]/a/@href'
star_title  = '//*[@class="headline story-pg"]//h1//text()' 
star_region = '//*[@class="kicker"][@data-list-type="Article"]/text()' 
star_date = '//*[@class="date"]//text()' 
star_text = '//*[@id="story-body"]//text()'

 
# runSpider(url_list, star_urls, star_title, star_region, star_text, 'test.json')
