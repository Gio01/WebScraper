import scrapy
from urllib.parse import urlencode
import json
from datetime import datetime
import os
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from scrapy.exceptions import CloseSpider
from scrapy import Selector
API_KEY = os.getenv('API_KEY')

# To run: scrapy crawl tasks -o test.csv
# -o = ouput to the file test.csv for csv formated data

"""
We are creating a proxy link that we can target our requests to. In reality
this link will tell the scraperapi to go and fetch the requests that we want
from all of the diff proxies that they give us so that we do not get banned
by google for calling so many requests to them (might look like a DoS coming
from me so... yah)
"""


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true',
               'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


"""
We are creating the google search queries that we will use for the google
requests. We are doing it dynamically so that we can properly automate the
big number of requests

site
    we can specify a certain site we want to query
query
    value we would pass to a google search via the proxies
"""


def create_google_url(query):
    # num is the number of result links we want per google result page
    google_dictionary = {'q': query, 'num': 2}

    return 'http://www.google.com/search?' + urlencode(google_dictionary)


class SuggestionsSpider(scrapy.Spider):
    name = 'tasks'
    allowed_domains = ['api.scraperapi.com']
    # these settings are for the free Scaper API plan!
    # the original req per domain was 10

    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 10}

    """
    we create the query for the google search by calling the create_google_url
    function we craeted above and then passing it a url query. If the
    query has more than one word then we need to append the work with the +
    as we would normally do when doing a query in the url!
    """

    def start_requests(self):
        url = create_google_url('coffee+shops')

        yield scrapy.Request(get_url(url), callback=self.parse,
                             meta={'pos': 0})

    """
    We are now looping through the response object and extracting the data
    we want to see. We are keeping track of the pages we see with the position
    to count how many webpages we have scraped.

    The item obj then holds all of the data we want for each single page and
    we are then using that item to ouput to a csv file from where we can then
    see the collection of pages with their data based on the way we parsed the
    response obj in the parse() function
    """
    def parse(self, response):
        data = json.loads(response.text)
        #position = response.meta['pos']
        #queried_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # url_links = []
        for res in data['organic_results']:
            title = res['title']
            # snippet = res['snippet']
            # url_links.append(res['link'])
            #item = {'title': title, 'link': link}
            #position += 1
            # If another page exists in the query search then get that page's
            # data
            yield scrapy.Request(res['link'], callback=self.parse_page)

    def parse_page(self, response):
        # sel = Selector(response)
        print(response.xpath('//title/text()')).getall()
