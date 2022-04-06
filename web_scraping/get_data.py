import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import math
from datetime import date, timedelta
import datetime

chrome_path = ChromeDriverManager().install()
chrome_options = Options()
chrome_options.add_argument("--headless")

horse_year = '1112'
directory = 'C:/Users/s1155126103/Desktop/CSCI4998/Data/' + horse_year + '/'
#directory = 'C:/Users/chang/Downloads/CSCI4998/Data/' + horse_year + '/'

wrong_course = 'Wrong_course'

data = [   # store race data
    #["YYYY", "MM", "DD", "場次", "名次", "馬號", "馬名", "馬齡", "騎師", "練馬師", "實際負磅", "排位體重", "檔位", "完成時間", "獨贏賠率"]
]
#link_data = [  # store links
#    ["馬名", "騎師", "練馬師"]
#]
location_data = [   # store track location data
    #["YYYY", "MM", "DD", "場次", "馬場", "跑道/賽道", "途程", "場地狀況", "賽事班次"]
]
horse_data = [      # store horse name and its points
    #["馬名", "評分"]
]
jockey_data = [     # store jockey name and his points
    #["練馬師", "評分"]
]
trainer_data = [    # store trainer name and his points
    #["練馬師", "評分"]
]

basic_points = 100
horse_dict = {}     # dictionary for horse name and points got
jockey_dict = {}     # dictionary for jockey name and points got
trainer_dict = {}     # dictionary for trainer name and points got

race_year = 2018
race_month = 2
race_day = 25
today = datetime.date.today()

#get dates
def read_dates(file_name):
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    dates = [rows for rows in reader]
    inp.close()
    return dates

# get all racing days
def all_race_day(year):
    d = date(race_year, race_month, race_day)
    while d <= today:
        yield d
        d += timedelta(days = 3)
        yield d
        d += timedelta(days = 4)

# validate url
def validate_url(url):
    try:
        #Get Url
        get = requests.get(url)
        # if the request succeeds 
        if get.status_code == 200:
            return True
        else:
            return False

    #Exception
    except requests.exceptions.RequestException as e:
        return False


# get the html from hkjc
def get_html(url, className):
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    try:
        driver.get(url)
    except Exception as e:
        return None
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
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    error_div = soup.find('div', attrs={'class':'errorright'})
    if error_div is not None:
        return None
    driver.close()
    return soup

# get horse data (age)
def get_horse_data(url):
    soup = get_html(url, '.table_top_right.table_eng_text')
    if soup is None:
        return

    table = soup.find('table', attrs={'class':'table_top_right table_eng_text'})  # get the table of horse age
    table_body = table.find('tbody')

    row = table_body.find('tr')
    cols = row.find_all('td')
    origin_age = cols[-1].text.strip()
    horse_age = origin_age.split()[-1]
    if not horse_age.isnumeric():
        horse_age = -1
    return horse_age

# calculate points got
def cal_points(points, name, dictionary):
    if name in dictionary:
        dictionary[name] = dictionary.get(name) + points
    else:
        dictionary[name] = basic_points + points

# get race table data
def get_race_data(url, year, month, day, race_no, first=False):
    soup = get_html(url, '.f_tac.table_bd.draggable')
    print('soup is none', soup is None)
    if soup is None:
        print('hello?')
        return wrong_course

    table = soup.find('table', attrs={'class':'f_tac table_bd draggable'})  # get the table of race result
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    row_len = len(rows)
    rounded_row_len = math.floor(row_len * 0.4)
    print(row_len, rounded_row_len)
    for row_idx, row in enumerate(rows):
        cols = row.find_all('td')
        # store race table data
        row_data = [ele.text.strip() for idx, ele in enumerate(cols) if idx != 8 and idx != 9]

        # get horse url and get horse data
        horse_url = "https://racing.hkjc.com" + cols[2].a.get('href')
        #horse_age = get_horse_data(horse_url)

        # insert data got into data in correct order
        row_data.insert(0, year)
        row_data.insert(1, month)
        row_data.insert(2, day)
        row_data.insert(3, race_no)
        #row_data.insert(7, horse_age)
        row_data.insert(7, horse_url)

        # store data
        data.append(row_data)
        #link_row_data = ["https://racing.hkjc.com" + ele.a.get('href') for idx, ele in enumerate(cols) if idx == 2 or idx == 3 or idx == 4]
        #link_data.append(link_row_data)

        # calculate points got
        points = 0
        if row_idx < rounded_row_len:
            points = rounded_row_len - row_idx
        elif row_idx >= row_len - rounded_row_len:
            points = row_idx - (row_len - rounded_row_len - 1)
            points = -points
        horse_name = cols[2].text.strip()
        jockey_name = cols[3].text.strip()
        trainer_name = cols[4].text.strip()
        cal_points(points, horse_name, horse_dict)
        cal_points(points, jockey_name, jockey_dict)
        cal_points(points, trainer_name, trainer_dict)

    
    span = soup.find('span', attrs={'f_fl f_fs13'}) # get the race location
    location = span.text.strip().split()[2]

    table_body_2 = soup.find('tbody', attrs={'class':'f_fs13'})  # get the table of race location data
    rows = table_body_2.find_all('tr')
    for row_idx, row in enumerate(rows):
        cols = row.find_all('td')
        print(row_idx, cols)
        if row_idx == 1:
            class_distance = cols[0].text.strip()
            condition = cols[2].text.strip()
        elif row_idx == 2:
            track_course = cols[2].text.strip()
    
    race_class = class_distance.split()[0]
    distance = class_distance.split()[2]
    if len(track_course.split()) > 1:
        track_course = track_course.replace("\"", "")
        print(track_course)
    """track = track_course.split()[0]
    course = track_course.split()[2]"""

    location_data.append([year, month, day, race_no, location, track_course, distance, condition, race_class])

    if first is True:
        table = soup.find('table', attrs={'class':'f_fs12 f_fr js_racecard'})  # get the number of races of the day
        table_body = table.find('tbody')

        row = table_body.find('tr')
        cols = row.find_all('td')
        number_of_races = len(cols) - 2
        if (number_of_races > 10):
            number_of_races = 10
        return number_of_races

    return

def write_file(data_list, file_name, write_type):
    # open the file in the write mode
    f = open(directory + file_name, write_type, newline='', encoding="utf-8")

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    data_len = len(data_list)
    print(data_len)
    for i in range(0, data_len):
        writer.writerow(data_list[i])

    # close the file
    f.close()

def dict_to_list(dictionary, data_list):
    for k, v in dictionary.items():
        data_list.append([k, v])
    return data_list

# write data got into all files
def write():
    global data
    global location_data
    global horse_dict
    global horse_data
    global jockey_dict
    global jockey_data
    global trainer_dict
    global trainer_data
    write_file(data, 'races_with_horse_link.csv', 'a')
    write_file(location_data, 'location.csv', 'a')

    data = []
    location_data = []

    horse_data = dict_to_list(horse_dict, horse_data)
    jockey_data = dict_to_list(jockey_dict, jockey_data)
    trainer_data = dict_to_list(trainer_dict, trainer_data)

    write_file(horse_data, 'horse.csv', 'w')
    write_file(jockey_data, 'jockey.csv', 'w')
    write_file(trainer_data, 'trainer.csv', 'w')

    horse_data = []
    jockey_data = []
    trainer_data = []

def read_csv_file(file_name):
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    data_dict = {rows[0]:int(rows[1]) for rows in reader}
    inp.close()
    return data_dict

def csv_to_dict():
    global horse_dict
    global horse_data
    global jockey_dict
    global jockey_data
    global trainer_dict
    global trainer_data
    
    horse_dict = read_csv_file('horse.csv')
    jockey_dict =  read_csv_file('jockey.csv')
    trainer_dict = read_csv_file('trainer.csv')


if __name__ == '__main__':
    dates = read_dates(horse_year + '_racing_dates.csv')
    print(dates)
    csv_to_dict()
    print(horse_dict, jockey_dict, trainer_dict)
    x = input()
    if x == 'exit':
        exit()
    # for all wed and sun
    total_count = 1
    for days, day in enumerate(dates):
        if days >= 1 and len(data) > 0:
            write()
        #course_count = 0
        year, month, day, race_course = day
        print(year, month, day, race_course)
        if int(year) > 2018:
            break

        number_of_races = get_race_data("https://racing.hkjc.com/racing/information/chinese/Racing/LocalResults.aspx?RaceDate=" + year + "/" + month + "/" + day + "&Racecourse=" + race_course + "&RaceNo=1", year, month, day, total_count, first=True)
        print(number_of_races)
        total_count = total_count + 1
        for i in range(2, number_of_races+1):
            race_no = str(i)
            url = "https://racing.hkjc.com/racing/information/chinese/Racing/LocalResults.aspx?RaceDate=" + year + "/" + month + "/" + day + "&Racecourse=" + race_course + "&RaceNo=" + race_no
            course_check = get_race_data(url, year, month, day, total_count)
            total_count = total_count + 1

    write()