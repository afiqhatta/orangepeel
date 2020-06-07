# Design document for the code 

## Usage by the user
One part of the functionality is that a user should be able to, on their own, scrape websites. There is a wrapper function of which takes xpath parameters as an input. 

## Design of spiders 
We have a single spider indexed with a name to represent scraping of one type of medium. 
For example, the spider dedicated to scraping just news websites is called 'news'.For a given spider, we pass arguments which are pertinent to the type of media we're scraping through a wrapper function. 

Now, it seems like the best way to input arguments for each spider is to pass them through command-line arguments, 
those of which are listed in the scrapy documentation at https://docs.scrapy.org/en/latest/topics/spiders.html#spider-arguments. 

