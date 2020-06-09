import pandas as pd 
import orangepeel.spiders.news_spider as spider 

def pullNews(pages, News, output_file): 
    df = pd.read_csv('../metadata.csv')
    args = list(df[df.name == News].iloc[0,2:].values) 
    print(args)
    spider.pullArticles(pages, *args, output_file)

pullNews(5, 'The Edge', 'test.json')
