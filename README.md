# Scrapy-Start

A Repo for introducing the scrapy framework.

## Run the Project

Steps and Requirements to install and run de project

- You will need Pipenv >= 2020.11.15. Otherwise Scrapy install will throw an error.

1. Clone the project  
   `git clone https://github.com/LucasEduardoRomero/scrapy-start`

1. Create the virtualenv  
   `pipenv shell`

1. Install dependencies  
   `pipenv install`

1. You are ready to go!

## Robots

The project consists on three Spiders / Crawlers inside 2 files:

### quotes_spider.py

Here we have the file with the Spiders that Crawls the [quote.toscrape.com](http://quotes.toscrape.com/) site.

1. QuotesSpider

- This Class is responsible to get the site content, Crawl every quote with text (the quote itself), author and tags. And finally, search for a 'next' button to follow to the next page and repeat the proccess.

- Run the Spider. The output will be prompted in terminal  
  `scrapy crawl quotes`

- Run the Spider and save the content in a json lines file.  
  `scrapy crawl quotes -O quotes.jl`

1. AuthorSpider

- This Class is quite similar to _QuotesSpider_. It opens the same page, search for links to the author's page, open then and passes to another function called _parse_author_. Then it searchs for 'next' button to go to the next page and repeat the proccess.

- The _parse_author_ function receives the response of the request to the author's page, and parse the name, birthdate and the bio (a simple text resuming the author's life)

- Run the Spider.  
  `scrapy crawl author -O author.jl`

### tutorial_spider.py

This File has just one Spider, that crawls the [zyte blog page](https://www.zyte.com/blog/).

1. PostSpider

This Spider gets every post title (its a link to the post page), request its and forward to _parse_post_ function. Then it searchs for next button and repeat the proccess on the next page.

- The _parse_post_ function receives the content from the page, and parse the post_title and the post_first_text (The first paragraph from the post).

- Run the Robot  
  `scrapy crawl -O posts.jl`
