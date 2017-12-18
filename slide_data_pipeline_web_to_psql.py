# 1. import libraries 
from selenium import webdriver
from datetime import datetime, timedelta 
import psycopg2
import os 
import time
import shutil

# 2. functions, variables & selenium options
def date_extract (days_before_today):
    ''' define the day to extract'''
    date_yesterday = (datetime.today() - timedelta(days = days_before_today)).strftime('%m/%d/%Y')
    return str(date_yesterday)

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'C:/Users/vanderstraatenj/Desktop/Slide_data_pipeline'}
chrome_options.add_experimental_option('prefs', prefs)

# 3. Connection and navigation to home page
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://start.slidebristol.com/adminzone/login/?next=/adminzone/')
username = browser.find_element_by_id("id_username")
password = browser.find_element_by_id("id_password")
username.send_keys("xxxx")
password.send_keys("xxx")
browser.find_element_by_xpath("//input[@type='submit']").click()
browser.get('https://start.slidebristol.com/adminzone/statistics/')

# 4. Dowload data files
for i in range(1,5):
    browser.find_element_by_xpath("//div[@class='all']//li[%s]"%i).click()
    time.sleep(1) 
    browser.find_element_by_xpath("(//input[@id='id_start'])[%s]"%i).send_keys(date_extract(1))
    browser.find_element_by_xpath("(//input[@id='id_end'])[%s]"%i).send_keys(date_extract(1))
    time.sleep(1) 
    browser.find_element_by_xpath("(//button[@type='submit'])[%s]"%i).click()
    time.sleep(1) 
    browser.refresh()
    time.sleep(1) 
browser.quit()

# 5 transfer file to PostresQL

# 5.1 connection PSQL database
time.sleep(5) 
path = 'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline'
conn_string = "host='localhost' dbname='Slide_data' user='postgres' password='xxx'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
conn.rollback()

# 5.2 Upload file in DB and archive csv file 
files = os.listdir(path)
print(files)
files_path_dict = {'users_stat':'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/customers','reservations_stat':'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/bookings','search_stat':'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/searches','mads_stat':'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/shift'}

for i in files:
    if 'users_stat' in i:
        f = open('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s'%i,'r')
        cursor.copy_expert(r"copy customers FROM 'C:\Users\vanderstraatenj\Desktop\slide_data_pipeline\%s' WITH (FORMAT CSV, DELIMITER ',', NULL 'N/A', HEADER)" %i, f)
        conn.commit()
        f.close()
        shutil.move('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s' %i,'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/customers') 

for i in files:
    if 'reservations_stat' in i:
        f = open('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s'%i,'r')
        cursor.copy_expert(r"copy bookings FROM 'C:\Users\vanderstraatenj\Desktop\slide_data_pipeline\%s' WITH (FORMAT CSV, DELIMITER ',', NULL 'N/A', HEADER)" %i, f)
        conn.commit()
        f.close()
        shutil.move('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s' %i,'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/bookings') 

for i in files:
    if 'search_stat' in i:
        f = open('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s'%i,'r')
        cursor.copy_expert(r"copy searches FROM 'C:\Users\vanderstraatenj\Desktop\slide_data_pipeline\%s' WITH (FORMAT CSV, DELIMITER ',', NULL 'N/A', HEADER)" %i, f)
        conn.commit()
        f.close()
        shutil.move('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s' %i,'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/searches') 

for i in files:
    if 'mads_stat' in i:
        f = open('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s'%i,'r')
        cursor.copy_expert(r"copy shift FROM 'C:\Users\vanderstraatenj\Desktop\slide_data_pipeline\%s' WITH (FORMAT CSV, DELIMITER ',', NULL 'N/A', HEADER)" %i, f)
        conn.commit()
        f.close()
        shutil.move('C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/%s' %i,'C:/Users/vanderstraatenj/Desktop/slide_data_pipeline/shift') 