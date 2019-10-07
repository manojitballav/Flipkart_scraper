# This program is the primary control program to scrap reviews from Flipkart
from pymongo import MongoClient
import re,time
from selenium import webdriver
from selenium import *

# connection to the db
client = MongoClient('127.0.0.1',27017)
db = client['flipkart']
col1 = db['r_data']
# webdrive connection
driver = webdriver.Firefox()

def r_update(rating,heading,body,pc):
    col2 = db[pc]
    col2.update_one({"body": body},{'$set':{"body":body,"rating":rating,"heading":heading}},upsert=True)

def sreview(r_link,pn,pc):
    read = 0
    rating = 0
    heading = 0
    body = 0
    for val in range(1,int(pn)+1):
        driver.get(r_link+str(val))
        for kal in range(3,13):
            kal = str(kal)
            try:
                read = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[2]/div/div/span/span').click()
            except Exception as e:
                pass
            try:
                rating = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[1]/div').text
            except Exception as e:
                print(e)
            try:
                heading = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[1]/p').text
            except Exception as e:
                print(e)
            try:
                body = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[2]/div/div/div').text
            except Exception as e:
                print(e)
            r_update(rating,heading,body,pc)
            time.sleep(1)
    driver.quit()

def read():
    for dic in col1.find({}):
        link = dic['link']
        r_link = dic['r_link']
        pc = dic['db']
        driver.get(link)
        try:
            review = 0
            if(review == 0):
                review = (driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[3]').text)
                review = review.replace(' Reviews','')
                review = review.replace(' ','')
                review = review.replace(',','')
            else:
                review = (driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[3]').text)
        except Exception as NoSuchElementException:
            pass
            print("No element found")
        pn = (int(review)//10)
        sreview(r_link,pn,pc)

def main():
    read()

if __name__ == '__main__':
    main()
