# This program is the primary control program to scrap reviews from Flipkart
from pymongo import MongoClient
import re,time
from selenium import webdriver
from selenium import *
from datetime import datetime, timedelta
from datetime import date

# connection to the db
client = MongoClient('10.56.146.102',27017)
db = client['flipkart']
col1 = db['r_data']
# webdriver connection
driver = webdriver.Chrome()

def r_update(rating,heading,body,pc):
    col2 = db[pc]
    # col2.update_one({"body": body},{'$set':{"body":body,"rating":rating,"heading":heading}},upsert=True)

def sreview(r_link,pn,pc):
    read = 0
    rating = 0
    heading = 0
    body = 0
    name = 0
    date = 0
    # griver = webdriver.Firefox()f
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
                # print(rating)
            except Exception as e:
                print(e)
            try:
                heading = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[1]/p').text
                # print(heading)
            except Exception as e:
                print(e)
            try:
                body = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[2]/div/div/div').text
                # print(body)
            except Exception as e:
                print(e)

            # try:
            #     name = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[3]/div[1]/p[1]').text
            #     print(name)
            # except Exception as e:
            #     # print(e)
            #     pass
            # else:
            #     name = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[3]/div[1]/p[1]').text
            #     print(name)
            try:
                # when character does not shift
                date = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[3]/div[1]/p[3]').text
            except:
                # when character shifts
                date = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[4]/div[1]/p[3]').text
            # to determine if integer is present in date string
            if (bool(re.search(r'\d', date)) == True):
                # get only integer from string
                tmp5 = re.findall(r'\d+',date)
                res5 = list(map(int,tmp5))
                date = int(res5[0])
                print(date)
                # get actual date using time delta
                n = int(date)
                date = datetime.now()-timedelta(days=n)
                date = (date.strftime("%d"+"/"+"%m"+"/"+"%Y"))
                print(date)
            else:
                # convert today into date
                print(date)
                x = datetime.now()
                date = (x.strftime("%d"+"/"+"%m"+"/"+"%Y"))
                print(date)

            # try:
            #     date = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[4]/div[1]/p[3]').text
            #     print(date)
            # except Exception as e:
            #     print(e)
            


            # r_update(rating,heading,body,pc)
            # time.sleep(5)
    driver.quit()

def read():
    for dic in col1.find({'db':{"$in":["MOBFVQJ5TZTF5JHC"]}}):
        link = dic['link']
        r_link = dic['r_link']
        pc = dic['db']
        driver.get(link)
        review = int(317)
        # try:
        #     review = 0
        #     if(review == 0):
        #         review = (driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[3]').text)
        #         review = review.replace(' Reviews','')
        #         review = review.replace(' ','')
        #         review = review.replace(',','')
        #     else:
        #         review = (driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[3]').text)
        # except Exception as NoSuchElementException:
        #     pass
            # print("No element found")
        # print(review)
        pn = (int(review)//10)
        # driver.quit()
        sreview(r_link,pn,pc)

def main():
    read()

if __name__ == '__main__':
    main()



