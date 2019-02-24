# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['squawka.com/teams/manchester-city/results']

    def start_requests(self):
        self.driver = webdriver.Chrome('/home/ksyp/chromedriver')
        self.driver.get('http://squawka.com/teams/manchester-city/results')
        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//td[@class="match-centre"]/a/@href').extract()
        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[@title="Click to View Next Page"]')
                next_page.click()
                sleep(10)
                sel = Selector(text=self.driver.page_source)
                books += sel.xpath('//td[@class="match-centre"]/a/@href').extract()
                break
            except NoSuchElementException:
                self.driver.quit()
                break
        print("****************************************************************************************")
        for book in books:
            if book[7]!='c':
                print("hiii")
                yield Request(book,callback=self.parse_book)


    def parse_book(self, response):
        self.driver = webdriver.Chrome('/home/ksyp/chromedriver')
        self.driver.get(response.url)
        #sleep(10)
        listOfPlayerElement=self.driver.find_elements_by_xpath('//li[@class="mc-option"]')


        teamHomeElement=self.driver.find_element_by_xpath('//li[@id="team1-select"]')
        teamHomeElement.click()
        sleep(3)
        shotElement=self.driver.find_element_by_xpath('//div[@id="mc-stat-shot"]')
        shotElement.click()
        sleep(3)
        selector = Selector(text=self.driver.page_source)

        teamHomeName=selector.xpath('//div[@id="mc-header-team-1"]/div[@class="header-team"]/text()').extract_first()
        shotifTeam1=selector.xpath('//div[@id="mc-stat-shot"]/div[@class="mc-stat-data"]/div[@class="team1-data"]/text()').extract_first()
        #shotifTeam2=selector.xpath('//div[@id="mc-stat-shot"]/div[@class="mc-stat-data"]/div[@class="team2-data"]/text()').extract_first()
        #shotTakenbyTeam1=max(int(shotifTeam1),int(shotifTeam2))
        shotTakenbyTeam1=int(shotifTeam1)
        missedTeam1=len(selector.xpath('//g/path[@stroke="#f95a0b"]').extract())/2
        savedTeam1=len(selector.xpath('//g/path[@stroke="#982230"]').extract())/2
        scoredTeam1=len(selector.xpath('//g/path[@stroke="#333333"]').extract())/2
        blockedTeam1=len(selector.xpath('//g/path[@stroke="#f7bd06"]').extract())/2

        dic1={'TeamHome':teamHomeName,
              'Attempt on Goal': shotTakenbyTeam1,
              'Shot off the bar':missedTeam1,
              'Shot saved ':savedTeam1,
              'Shot blocked':blockedTeam1,
              'Scored Goal':scoredTeam1,
        }



        teamAwayElement=self.driver.find_element_by_xpath('//li[@id="team2-select"]')
        teamAwayElement.click()
        sleep(3)
        teamHomeElement.click()
        sleep(3)
        shotElement=self.driver.find_element_by_xpath('//div[@id="mc-stat-shot"]')
        shotElement.click()
        sleep(3)
        selector=Selector(text=self.driver.page_source)
        #shotifTeam1=selector.xpath('//div[@id="mc-stat-shot"]/div[@class="mc-stat-data"]/div[@class="team1-data"]/text()').extract_first()
        teamAwayName=selector.xpath('//div[@id="mc-header-team-2"]/div[@class="header-team"]/text()').extract_first()
        shotifTeam2=selector.xpath('//div[@id="mc-stat-shot"]/div[@class="mc-stat-data"]/div[@class="team2-data"]/text()').extract_first()
        #shotTakenbyTeam1=max(int(shotifTeam1),int(shotifTeam2))
        shotTakenbyTeam2=int(shotifTeam2)
        missedTeam2=len(selector.xpath('//g/path[@stroke="#f95a0b"]').extract())/2
        savedTeam2=len(selector.xpath('//g/path[@stroke="#982230"]').extract())/2
        scoredTeam2=len(selector.xpath('//g/path[@stroke="#333333"]').extract())/2
        blockedTeam2=len(selector.xpath('//g/path[@stroke="#f7bd06"]').extract())/2


        dic2={'TeamAway':teamAwayName,
              'Attempt on Goal': shotTakenbyTeam2,
              'Shot off the bar':missedTeam2,
              'Shot saved ':savedTeam2,
              'Shot blocked':blockedTeam2,
              'Scored Goal':scoredTeam2,
        }

        yield{'source':response.url,
              'Home Team':dic1,
              'Away Team':dic2,
        }

        self.driver.quit()
