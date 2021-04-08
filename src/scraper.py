import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CrossfitLeaderScraper():

    def __init__(self, scaled):
        self.url = "https://games.crossfit.com/leaderboard/open/2021?view=0&division=1&region=0&scaled=0&sort=0"
        self.page = 1
        self.data = []
        
    def __download_html(self, url):
        browser = webdriver.Chrome(executable_path=r'/Users/ivanaguilarnieto/Downloads/chromedriver89')
        browser.get(url)
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'athletes'))
        WebDriverWait(browser, 10).until(element_present)
        body = browser.execute_script("return document.body")
        source = body.get_attribute('innerHTML')   

        #html = response.read()
        return source

    def scrape(self):
        print("Web Scraping CrossFit Leaderboard of Opens 2021 data from " + "'" + self.url + "'...")
		# Start timer
        start_time = time.time()

		# Download HTML
        html = self.__download_html(self.url)
        bs = BeautifulSoup(html, 'html.parser')

        athletes = bs.findAll("tr")
        print(athletes)

		# # For each year, get its accidents' links
		# accidents_links = []
		# for y in years_links:
		# 	print "Found link to a year of crash: " + self.url + y
		# 	html = self.__download_html(self.url + y)
		# 	current_year_accidents = self.__get_accidents_links(html)
		# 	accidents_links.append(current_year_accidents)

		# 	# Uncomment this break in case of debug mode
		# 	# break

		# # For each accident, extract its data
		# for i in range(len(accidents_links)):
		# 	for j in range(len(accidents_links[i])):
		# 		print "scraping crash data: " + self.url + \
		# 			accidents_links[i][j]
		# 		html = self.__download_html(self.url +
		# 			accidents_links[i][j])
		# 		self.__scrape_example_data(html)

		# Show elapsed time
        end_time = time.time()
		# print "\nelapsed time: " + \
		#	str(round(((end_time - start_time) / 60), 2)) + " minutes"

    def data2csv(self, filename):
		# Overwrite to the specified file.
		# Create it if it does not exist.
        file = open("../csv/" + filename, "w+")

		# Dump all the data with CSV format
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";")
            file.write("\n")
