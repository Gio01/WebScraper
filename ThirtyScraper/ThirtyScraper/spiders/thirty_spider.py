import scrapy 

class SuggestionsSpider(scrapy.Spider):
	suggestions = "tasks"

	start_urls = [
		'http://somewebsite.com/user/suggestions'
	]

	#we parse the html source code of the location we scraped from which are the url links in the
	#start url object we created! We then are creting a file to save that source code from which 
	#we can then use to parse the data and see what we can find and hence be able to extract
	#exactly the certain components that we need for making the task suggestions!
	def parse(self, response):
		page = response.url.splt("/")
		filename = f'sugesstion-{page}.html'
		with open(filename, 'wb') as f:
			f.write(response.body)

