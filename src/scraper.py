import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import pathlib
import time
import json


class CrossfitLeaderScraper():

    def __init__(self):
        self.data = []
        self.path = str(pathlib.Path().absolute())
        self.numAthlete = 0
        
    def __download_html(self, url):
        browser = webdriver.Chrome(executable_path=self.path+'/Drivers/chromedriver')
        browser.get(url)
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'athletes'))
        WebDriverWait(browser, 20).until(element_present)
        body = browser.execute_script("return document.body")
        source = body.get_attribute('innerHTML')   

        #html = response.read()
        return source
    
    def __download_html_without_javascript(self, url):
        response = urlopen(url)
        html = response.read()
        return html
    
    def __download_json(self, url):
        response = urlopen(url)
        _json = response.read()
        return json.loads(_json)
    
    def scrapeWithJson(self,scaled, page, division):
		# Start timer
        start_time = time.time()
        urlJson = "https://c3po.crossfit.com/api/competitions/v2/competitions/open/2021/leaderboards?view=0&division="+ division +"&region=0&scaled=" + scaled + "&sort=0&page=" + page
        print("Web Scraping CrossFit Leaderboard of Opens 2021 data from " + "'" + urlJson + "'...")

		# Download HTML
        _json = self.__download_json(urlJson)
        
        
        for a in _json['leaderboardRows']:
            athlete_info = {}
            affiliate_info = {}
            rank = a['overallRank']
            competitor_id = a['entrant']['competitorId']
            first_name = a['entrant']['firstName']
            last_name = a['entrant']['lastName']
            countrie = a['entrant']['countryOfOriginName']
            total_point = a['overallScore']
            result_21_1 = a['scores'][0]['rank'] + ' (' + a['scores'][0]['scoreDisplay']+')'
            result_21_2 = a['scores'][1]['rank'] + ' (' + a['scores'][1]['scoreDisplay']+')'
            result_21_3 = a['scores'][2]['rank'] + ' (' + a['scores'][2]['scoreDisplay']+')'
            result_21_4 = a['scores'][3]['rank'] + ' (' + a['scores'][3]['scoreDisplay']+')'
            athlete_info=self.getAthleteInfo(competitor_id)
            if (athlete_info['affiliate_code']!=''):
                affiliate_info= self.getAffiliateInfo(athlete_info['affiliate_code'])   
            self.data.append([competitor_id,rank, first_name, last_name, countrie, total_point, result_21_1, result_21_2, result_21_3, result_21_4])
            for x in athlete_info:
                self.data[self.numAthlete].append(athlete_info[x])
            for x in affiliate_info:
                self.data[self.numAthlete].append(affiliate_info[x])
            self.numAthlete+=1
            time.sleep(0.5)
            #self.data.append()
        end_time = time.time()
        print(str(round(((end_time - start_time) / 60), 2)) + " minutos")
        return self.data
        
        
    def scrape(self,scaled, page, division):
		# Start timer
        start_time = time.time()
        url = "https://games.crossfit.com/leaderboard/open/2021?view=0&division="+ division +"&region=0&scaled=" + scaled + "&sort=0&page=" + page
        print("Web Scraping CrossFit Leaderboard of Opens 2021 data from " + "'" + url + "'...")

		# Download HTML
        html = self.__download_html(url)
        bs = BeautifulSoup(html, 'html.parser')

        athletes = bs.findAll("tr")
        athletes.remove(athletes[0])
        for a in athletes:
            athlete_info = {}
            affiliate_info = {}
            rank = a.contents[0].find("div", {"class": "cell-inner"}).text
            competitor_id = a.find("a",{"class": "profile-link"}).attrs['href'].replace('/athlete/','')
            first_name = a.find("div", {"class": "first-name"}).text
            last_name = a.find("div", {"class": "last-name"}).text
            countrie = a.find("div", {"class": "country-flag"}).next.attrs['title']
            total_point = a.contents[2].find("div", {"class": "cell-inner"}).text
            result_21_1 = a.contents[3].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            result_21_2 = a.contents[4].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            result_21_3 = a.contents[5].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            result_21_4 = a.contents[6].find("span", {"class": "rank"}).text + a.contents[3].find("span", {"class": "result"}).text
            athlete_info=self.getAthleteInfo(competitor_id)
            if (athlete_info['affiliate_code']!=''):
                affiliate_info= self.getAffiliateInfo(athlete_info['affiliate_code'])   
            self.data.append([competitor_id,rank, first_name, last_name, countrie, total_point, result_21_1, result_21_2, result_21_3, result_21_4])
            for x in athlete_info:
                self.data[self.numAthlete].append(athlete_info[x])
            for x in affiliate_info:
                self.data[self.numAthlete].append(affiliate_info[x])
            self.numAthlete+=1
            time.sleep(0.5)
            #self.data.append()
        end_time = time.time()
        print(str(round(((end_time - start_time) / 60), 2)) + " minutos")
        return self.data

    def getAthleteInfo(self,competitor_id):
        html_athlete = self.__download_html_without_javascript("https://games.crossfit.com/athlete/"+competitor_id)
        bsAthlete = BeautifulSoup(html_athlete, 'html.parser')
        athlete_info={}
        info_bar = bsAthlete.find("ul",{"class": "infobar"})
        if (info_bar is not None):
            #athlete_info['athlete_country']=info_bar.find_all("li")[0:1][0].find("div",{"class": "text"}).text.replace("\n","").replace(" ","")
            info_bar_list = info_bar.find_all("li")[2:]
            for x in info_bar_list:
                field=x.find("div",{"class": "item-label"}).text.replace("\n","").replace(" ","").lower()
                athlete_info[field]=x.find("div",{"class": "text"}).text.replace("\n","").replace(" ","")
            if (athlete_info['affiliate']!='--') :
                athlete_info['affiliate_code'] = gym_code= bsAthlete.find("ul",{"class": "infobar"}).find_all("li")[6].find("a").attrs['href'].replace('/affiliate/','')
            else :
                athlete_info['affiliate_code'] = ''
        return athlete_info;
    
    def getAffiliateInfo(self,affiliate_id):
        html_affiliate = self.__download_html_without_javascript("https://games.crossfit.com/affiliate/"+affiliate_id)
        bsAffiliate = BeautifulSoup(html_affiliate, 'html.parser')
        affiliate_info={}
        info_bar = bsAffiliate.find("ul",{"class": "infobar"})
        if (info_bar is not None):
            affiliate_info['affiliate_country'] = info_bar.find_all("li")[0:1][0].find("div",{"class": "text"}).text.replace("\n","")
            info_bar_list = info_bar.find_all("li")[1:3]
            for x in info_bar_list:
                field=x.find("div",{"class": "item-label"}).text.replace("\n","").replace(" ","").lower()
                affiliate_info[field]=' '.join(x.find("div",{"class": "text"}).text.replace("\n","").split())
        return affiliate_info

    def data2csv(self, filename):
		# Overwrite to the specified file.
		# Create it if it does not exist.
        pathDirectoryAbsolute = str(pathlib.Path().absolute())
        with open(pathDirectoryAbsolute + '/csv/' + filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', )
            csvwriter.writerow(["CompetitorId","Rank", "Name", "Lastname", "Country", "Points", "21.1", "21.2", "21.3", "21.4","Division","Age","Height","Weight","Affiliate","Affiliate_code","Affiliate_country","Localitation","Phone"])
            for i in range(len(self.data)):
                csvwriter.writerow(self.data[i])
