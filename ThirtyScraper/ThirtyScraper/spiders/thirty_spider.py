import scrapy

class SuggestionsSpider(scrapy.Spider):
	name = "tasks"
		
	def start_requests(self):
		scrape_urls = [
			'https://www.brainyquote.com/topics/motivational-quotes'
		]
	
	#by using yield we are creating a generator object which we can use to iterate. So here
	#we are essentially just calling the request func from scrapy and then iterating it on the
	#diff url links that we are giving it and in each iteration we are also parsing the 
	#data we get back from each of the url requests.

	#the reason we use yield is that since we are going through a lot of data, by yielding we are
	#stopping for each scrapy.Request to fully terminate before going to the next iteration of the
	#urls. Hence we do not need to run through all the urls and use up a lot of memory space and
	#run through them one by one which requires less memory! (yiels gives us a generator = iterable obj 
		for url in scrape_urls:
			yield scrapy.Request(url=url, callback=self.parse)

	#we parse the html source code of the location we scraped from which are the url links in the
	#start url object we created! We then are creting a file to save that source code from which 
	#we can then use to parse the data and see what we can find and hence be able to extract
	#exactly the certain components that we need for making the task suggestions!
	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = f'tasks-{page}.html'
		with open(filename, 'wb') as f:
			f.write(response.body)

