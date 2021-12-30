import pandas as pd 
import orangepeel.orangepeel.spiders.news_spider as spider

spider.runSpider(url_list, url_tags, title_tag, region_tag, date_tag, text_tag, output_file, base_url)
