from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from newsplease import NewsPlease
import pandas as pd
import time


def get_links(url):
    text = urlopen(url).read()
    soup = BeautifulSoup(text, 'lxml')

    link_list = []
    data = soup.findAll('div',attrs={'class':'articles'})
    for div in data:
        links = div.findAll('a')
        for a in links:
            if a['href'][:5] == 'https':
                link_list.append(a['href'])

    return link_list


def unwrap_data(urls):
    dat = NewsPlease.from_urls(urls, timeout=6)
    for key, value in dat.items():
        dat[key] = [value.title, value.date_publish, value.description, value.maintext, value.authors]
    return dat


def parse_into_frame(url):
    urls = get_links(url)
    df = pd.DataFrame(unwrap_data(urls)).T
    df.columns = ['Title', 'Date', 'Description', 'Text', 'Authors']
    return df


def parse_multiple_pages(base_url, pages=15):

    full_dat = []
    page_urls = ([base_url]
                 + ['{base_url}&page={i}'.format(base_url=base_url, i=i) for i in
                    range(1, pages)])

    for url in page_urls:
        print(url)
        full_dat.append(parse_into_frame(url))

    return pd.concat(full_dat)



if __name__=='__main__':

    urls = {'Malaysia': 'https://reliefweb.int/updates?advanced-search=%28PC147%29_%28DT4611%29',
            'Philippines': 'https://reliefweb.int/updates?advanced-search=%28C188%29_%28DT4611%29'}

    print(parse_multiple_pages(base_url=urls['Philippines'], pages=2))