# News Article Archive on Undocumented Immigrants in Malaysia

## About
This is a curated data set of Malaysian reporting on undocumented immigrants in the country. News articles are scraped in the cloud with scrapinghub.
XPath selectors and some quick testing using the scrapy shell can be used to quickly scrape text form Malaysia's primary news providers. 

## Testing out links using the scrapy shell
For those who want a quick way to check that either their xpath or css selectors are giving the correct elements in the page, just do 
```
scrapy shell [url]
```
You can do a quick test by generating a json file of your results through the command
```
scrapy crawl [spider name]  -o [desired filename].json
```
## The XPath syntax
I would like to take this opportunity to credit https://devhints.io/xpath#class-check
which is a wonderful cheat sheet for learning about XPath syntax and selection. I previously used css selectors but this turned out to be a lot more intuitive and easier to use.  
