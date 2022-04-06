from os import read
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

chrome_path = ChromeDriverManager().install()
chrome_options = Options()
chrome_options.add_argument("--headless")

#directory = 'C:/Users/s1155126103/Desktop/CSCI4998/Data/'
directory = 'C:/Users/chang/Downloads/CSCI4998/Data/'

def get_horse_name(file_name):
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    horse_name = []
    for rows in reader:
        result = re.search(r"\(([A-Za-z0-9_]+)\)", rows[6])
        horse_name.append(result.group(1))
    inp.close()
    return horse_name

def get_redirected_url(url, className):
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, className + ', .errorright')))
    except:
        driver = webdriver.Chrome(chrome_path)
        driver.get(url)
        while(True):
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, className + ', .errorright')))
                break
            except:
                pass
        pass
    r_url = driver.current_url
    return r_url

def read_csv_file(file_name):
    cnt = 1
    race_data = []  # store all race data (element is a race)
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    for row in reader:
        race_data.append(row)
    inp.close()
    return race_data

def write_link(file_name, row_idx, link, old_data):
    outp = open(directory + file_name, mode='w', newline='', encoding="utf-8")
    writer = csv.writer(outp)

    # write a row to the csv file
    for row in old_data:
        row[row_idx] = link
        writer.writerow(row)

    # close the file
    outp.close()

def write_csv_file(data_list, file_name, write_type):
    # open the file in the write mode
    f = open(directory + file_name, write_type, newline='', encoding="utf-8")

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(data_list)

    # close the file
    f.close()

if __name__ == '__main__':
    """file_name = '1718/races.csv'
    names = get_horse_name(file_name)
    names = names[577:]
    old_data = read_csv_file(file_name)
    for name in names:
        url = "https://racing.hkjc.com/racing/information/chinese/Horse/HorseSearch.aspx?HorseName=&SearchType=BrandNumber&BrandNumber=" + name
        r_url = get_redirected_url(url, '.table_top_right.table_eng_text')
        write_csv_file([name, r_url], '1718/h_name.csv', 'a')"""
    file_name = 'demo/races_with_horse_link.csv'
    data = read_csv_file(file_name)

    for row in data:
        link = row[7]
        start_year = link.split('_')[1]
        age = int(row[0])-int(start_year)+1
        old_data = read_csv_file(file_name)
        write_link('demo/races_with_age.csv', 7, age, old_data)
    
