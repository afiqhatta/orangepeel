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
    # data = soup.findAll('main',attrs={'class':'site-main'}) # floodlist
    print(data)

    for div in data:
        links = div.findAll('a')
        for a in links:
            if a['href'][:5] == 'https':
                link_list.append(a['href'])

    return link_list


def unwrap_data(urls):
    dat = NewsPlease.from_urls(urls, timeout=6)
    for key, value in dat.items():
        dat[key] = [value.title, value.date_publish, value.description, value.authors]
    return dat


def parse_into_frame(url):
    urls = get_links(url)
    print(urls)
    df = pd.DataFrame(unwrap_data(urls)).T
    df.columns = ['Title', 'Date', 'Description', 'Authors']
    return df


def parse_multiple_pages(base_url, pages=15, init_page=1, extension=None):

    # take a set of links in a page, and then scrape them
    full_dat = []
    page_urls = ([base_url]
                 + ['{base_url}&page={i}'.format(base_url=base_url, i=i) for i in
                    range(init_page, pages)])

    for url in page_urls:
        print(url)
        full_dat.append(parse_into_frame(url))

    return pd.concat(full_dat)


def parse_multiple_pages_from_urls(page_urls, pages=15, init_page=1, extension=None):
    full_dat = []

    for url in page_urls:
        print(url)
        full_dat.append(parse_into_frame(url))

    return pd.concat(full_dat)


def update_reliefweb(urls, prefix='flood'):

    for country, url in urls.items():
        print('updating ')
        save_string = 'metadata/flood_{}.pickle'.format(country)
        df = pd.read_pickle(save_string)
        updated_df = pd.concat([df, parse_multiple_pages(base_url=url, pages=2)])
        updated_df.to_pickle(save_string)

    return 0



if __name__=='__main__':

    floodlist_url = {'Malaysia': 'https://floodlist.com/tag/Malaysia',
                      'Thailand': 'https://floodlist.com/tag/Thailand',
                      'Vietnam': 'https://floodlist.com/tag/Vietnam',
                      'Indonesia': 'https://floodlist.com/tag/Indonesia',
                      'Philippines': 'https://floodlist.com/tag/Philippines'}

    floodlist_pattern = 'https://floodlist.com/tag/'

    # do this to load url from relief webdriver
    # for country, url in urls.items():
    #     parse_multiple_pages(base_url=url, pages=2).to_pickle('metadata/flood_{}.pickle'.format(country))


    # # do this for floodlist
    # for country, url in floodlist_url.items():
    #     url_list = [url] + ['{base_url}/page/{i}'.format(base_url=url, i=i) for i in range(2, 3)]
    #     print(url_list)
    #     parse_multiple_pages_from_urls(url_list).to_pickle('metadata/floodlist_{}.pickle'.format(country))
    #
    # print(pd.read_pickle('metadata/floodlist_Malaysia.pickle'))

    # update
    update_reliefweb(urls)