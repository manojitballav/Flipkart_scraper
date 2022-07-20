from lib2to3.pgen2 import driver
from typing import Collection
# from bson.py3compat import reraise_instances
from pymongo import MongoClient
import re,time
from selenium import webdriver
from selenium import *
from datetime import datetime, timedelta
from datetime import date

# connection to the db
client = MongoClient('10.56.146.102',27017)


db = client['MiTV']
collection = db['flipkart']

# function to get the product details
# chrome with headless
# op = webdriver.ChromeOptions()
# op.add_argument('headless')
# driver = webdriver.Chrome(options=op)

# chrome full view
driver = webdriver.Chrome()

# driver = webdriver.Firefox()

def get_reviews(fsn,rlink,reviews):
    page = (int(reviews)//10)+1
    col = db[fsn]
    for val in range(1,page+1):
        driver.get(rlink+str(val))
        time.sleep(5)
        for kal in range(3,13):
            kal = str(kal)
            try:
                # find read more button
                try:
                    read = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[2]/div/div/span/span').click()
                except Exception as e:
                    pass
                # getting the rating
                try:
                    rating = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[1]/div').text
                except Exception as e:
                    print(e)
                finally:
                    pass
                # getting the rating
                try:
                    heading = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[1]/p').text
                except Exception as e:
                    print(e)
                finally:
                    pass
                # getting the review
                try:
                    body = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[2]/div/div/div').text
                except Exception as e:
                    print(e)
                finally:
                    pass
                # getting the username
                try:
                    user = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[4]/div[1]/p[1]').text
                except Exception as e:
                    user = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[3]/div[1]/p[1]').text
                except Exception as e:
                    user  = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[2]/div['+kal+']/div/div/div/div[3]/div[1]/p[1]').text
                finally:
                    pass

                # check to not insert blank fields
                if (rating != None):
                    col.update_one({'user':user},{'$set':{'rating':rating,'heading':heading,'body':body,'user':user}})
                    # col.insert_one({'rating':rating,'heading':heading,'body':body,'user':user})               
                else:
                    pass
                # rendering all the variables to null
                rating = None
                heading = None
                body = None
                user = None
            except Exception as e:
                pass


if __name__ == '__main__':
    # get the product details
    for doc in collection.find({'fsn':{"$in":["TVSG5ZGZQKRDMQVZ"]}}):
        fsn = doc['fsn']
        rlink = doc['rlink']
        reviews = doc['reviews']
        print(fsn)
        print(rlink)
        print(reviews)
        get_reviews(fsn,rlink,reviews)
        driver.quit()