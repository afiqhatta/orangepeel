import scrapy
import os

def pullArticles(pages, base, url_tags, title_tag, region_tag, date_tag, text_tag, base_url, output_file): 

    # generate the list of urls from the base url in the right range
    url_list = urlList(base, pages) 
    
    # run the spider 
    runSpider(url_list, url_tags, title_tag, region_tag, date_tag, text_tag, base_url, output_file)  


def urlList(base, pages): 
    """
    generate the list of urls in a given page range
    """
    url_list = []
    for i in range(1, pages): 
        url_list.append(base.format(number=str(i)))
    return url_list 


def runSpider(url_list, url_tags, title_tag, region_tag, date_tag, text_tag, base_url, output_file):
    """
    This function runs a scrapy command in the terminal which 
    takes our list of urls, title, region, text and date tags and 
    then parses it into the scrapy shell. It then spits out a json file which 
    contains the output of our scrape. 
    
    The base_url optional argument is there in the case that 
    our links given in the search page is are relative links or full absolute links. 
    The base_url is given in our metadata csv file like any other. In the case that it's not needed, 
    it's a zero. 

    """
    stringy_url_list = ','.join(url_list)
    base_string = "scrapy crawl news -a url_list='{url_list}' -a url_tags='{url_tags}' -a title_tag='{title_tag}' -a region_tag='{region_tag}' -a date_tag='{date_tag}' -a text_tag='{text_tag}'".format(url_list=stringy_url_list, url_tags=url_tags, title_tag=title_tag, region_tag=region_tag, text_tag=text_tag, date_tag=date_tag)
    
    # check if we need a base url to add to our links  
    base_string += " -a base_url='{base_url}'".format(base_url=base_url)
    
    # append our output string to output files
    output_string = " -o {output}".format(output=output_file)
    os.system(base_string + output_string)
     

class HistoricalSpider(scrapy.Spider):
    """
    This spider scrapes news articles by first generating the list of links in the 
    search page. Then, it parses through those links via the call back to 
    to get the page specific information. 
    """

    name = 'news'  

    def __init__(self, *args, **kwargs): 
        super(HistoricalSpider, self).__init__(*args, **kwargs) 
        self.start_urls = self.url_list.split(',') 

    def parse(self, response):
        urls = response.xpath(self.url_tags).extract()
        if self.base_url != '0': 
            urls = [self.base_url + extension for extension in urls]
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse_details)

    def parse_details(self, response):
        yield {
                'title': response.xpath(self.title_tag).extract_first(),
                'region': response.xpath(self.region_tag).extract_first(), 
                    'date': response.xpath(self.date_tag).extract_first(),  
                    'text': ' '.join(response.xpath(self.text_tag).extract()), 
                    }

# runSpider(url_list, star_urls, star_title, star_region, star_text, 'test.json')
