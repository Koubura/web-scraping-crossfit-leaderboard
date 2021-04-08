import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

class CrossfitLeaderScraper():

    def __init__(self, scaled, page):
        self.url = "https://games.crossfit.com/leaderboard/open/2021?view=0&division=1&region=0&scaled=" + scaled + "&sort=0&page=" + page
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
        athletes.remove(athletes[0])
        for a in athletes:
            rank = a.contents[0].find("div", {"class": "cell-inner"}).text
            first_name = a.find("div", {"class": "first-name"}).text
            last_name = a.find("div", {"class": "last-name"}).text
            countrie = a.find("div", {"class": "country-flag"}).next.attrs['title']
            total_point = a.contents[2].find("div", {"class": "cell-inner"}).text
            result_21_1 = a.contents[3].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            result_21_2 = a.contents[4].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            result_21_3 = a.contents[5].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            result_21_4 = a.contents[6].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            
            self.data.append([rank, first_name, last_name, countrie, total_point, result_21_1, result_21_2, result_21_3, result_21_4])
        return self.data
        end_time = time.time()
        
        print(str(round(((end_time - start_time) / 60), 2)) + " minutos")

    def data2csv(self, filename):
		# Overwrite to the specified file.
		# Create it if it does not exist.
        with open('./web-scrapping-crossfit-leaderboard/csv/' + filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["Rank", "Name", "Lastname", "Country", "Points", "21.1", "21.2", "21.3", "21.4"])
            for i in range(len(self.data)):
                csvwriter.writerow(self.data[i])
