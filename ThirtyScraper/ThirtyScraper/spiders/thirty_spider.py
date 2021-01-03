import scrapy
import pandas as pd
from urllib.parse import urlencode
from urllib.parse import urlparse
import json
from datetime import datetime
import os

API_KEY = os.getenv('API_KEY')

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


def create_google_url(query, site=''):
    google_dictionary = {'q': query, 'num': 100}
    if site:
        web = urlparse(site).netloc
        google_dictionary['as_sitesearch'] = web
        return 'http://www.google.com/search?' + urlencode(google_dictionary)
    return 'http://www.google.com/search?' + urlencode(google_dictionary)


class SuggestionsSpider(scrapy.Spider):
    name = 'tasks'
    allowed_domains = ['api.scraperapi.com']
    #these settings are for the free Scaper API plan!
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

    def parse(self, response):
        data = json.loads(response.text)
        position = response.meta['pos']
        data_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for res in data['organic_results']:
            title = res['title']
            snippet = res['snippet']
            link = res['link']
            item = {'title': title, 'snippet': snippet, 'link': link, 'pos':
                    position, 'date':  data_time}
            position += 1
            yield item

        next_web_page = data['pagination']['nextPageUrl']
        if next_web_page:
            yield scrapy.Request(get_url(next_web_page), callback=self.parse,
                                 meta={'pos': position})


