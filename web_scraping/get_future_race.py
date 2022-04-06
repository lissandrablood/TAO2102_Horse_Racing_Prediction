from ast import Num
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
import re
import sys

chrome_path = ChromeDriverManager().install()
chrome_options = Options()
chrome_options.add_argument("--headless")

#directory = 'C:/Users/s1155126103/Desktop/CSCI4998/Data/' + horse_year + '/'
#directory = 'C:/Users/chang/Downloads/CSCI4998/future_data/'
directory = '../future_data/'

wrong_course = 'Wrong_course'

data = [   # store race data
    #["YYYY", "MM", "DD", "場次", "名次", "馬號", "馬名", "馬齡", "騎師", "練馬師", "實際負磅", "排位體重", "檔位", "完成時間", "獨贏賠率"]
    ["year", "month", "day", "races_id", "result", "horse_id", "horse", "age", "jockey", "trainer", "horse_weight", "actual_weight", "draw", "time", "odd"],
    ["2011", "9", "11", "0", "1", "14", "厲行星(L029)", "3", "白德民", "沈集成", "119", "1131", "11", "1:10.92", "4.4"],
    ["2011", "9", "11", "0", "2", "6", "龍船快(M144)", "2", "蔡明紹", "告東尼", "127", "1118", "9", "1:11.16", "6.4"],
    ["2011", "9", "11", "0", "3", "4", "上浦駿將(L020)", "3", "潘頓", "呂健威", "132", "1137", "8", "1:11.25", "7.2"],
    ["2011", "9", "11", "0", "4", "5", "快意(L271)", "3", "郭立基", "霍利時", "130", "1139", "6", "1:11.27", "7.4"],
    ["2011", "9", "11", "0", "5", "11", "你好我好(K086)", "4", "梁家俊", "梁定華", "121", "1116", "7", "1:11.43", "11"],
    ["2011", "9", "11", "0", "6", "12", "金莊(K394)", "4", "都爾", "苗禮德", "121", "1045", "4", "1:11.55", "14"],
    ["2011", "9", "11", "0", "7", "9", "嘻哈大少(L208)", "3", "杜利萊", "文家良", "125", "1025", "12", "1:11.57", "10"],
    ["2011", "9", "11", "0", "8", "3", "開心好多(K284)", "4", "韋達", "李易達", "133", "1113", "14", "1:11.70", "15"],
    ["2011", "9", "11", "0", "9", "10", "叻先生(M065)", "2", "鄭雨滇", "何良", "123", "1008", "5", "1:11.73", "12"],
    ["2011", "9", "11", "0", "10", "7", "一般高(L064)", "3", "吳嘉晉", "葉楚航", "118", "1138", "13", "1:11.87", "65"],
    ["2011", "9", "11", "0", "11", "13", "好小子(K080)", "4", "普萊西", "告達理", "121", "1235", "3", "1:11.89", "11"],
    ["2011", "9", "11", "0", "12", "1", "航天之星(L339)", "3", "楊明綸", "姚本輝", "128", "1037", "2", "1:12.65", "99"],
    ["2011", "9", "11", "0", "13", "2", "金勝福星(M016)", "2", "賴維銘", "吳定強", "131", "1008", "10", "1:13.46", "26"],
    ["2011", "9", "11", "0", "14", "8", "民和國富(M133)", "2", "湯智傑", "徐雨石", "124", "1113", "1", "1:14.07", "83"]
]
#link_data = [  # store links
#    ["馬名", "騎師", "練馬師"]
#]
location_data = [   # store track location data
    #["YYYY", "MM", "DD", "場次", "馬場", "跑道/賽道", "途程", "場地狀況", "賽事班次"]
    ["year", "month", "day", "races_id", "venue", "track", "distance", "going", "class"],
    ["2011", "9", "11", "0", "沙田", "草地 - A 賽道", "1200", "好地", "第五班"]
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

horse_table_data = {    # store horse table data

}

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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, className)))
    except Exception as e:
        print(e)
        input("Error happened")
        driver.close()
        
        return None

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    error_div = soup.find('div', attrs={'class':'errorright'})
    if error_div is not None:
        input("Error happened")
        return None
    driver.close()
    return soup

# get horse data (age)
def get_horse_table(url):
    soup = get_html(url, 'bigborder')
    if soup is None:
        return

    table = soup.find('table', attrs={'class':'bigborder'})  # get the table of horse age
    table = table.find('tbody')
    table = table.find('tr')
    table = table.find('td')
    table = table.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    rows.pop(0)
    global horse_table_data
    for row in rows:
        cols = row.find_all('td')
        row_data = [ele.text.strip() for idx, ele in enumerate(cols) if idx != 1]
        horse_name = cols[1].text.strip().replace(" ", "")
        horse_table_data.update({horse_name: row_data})
    return

# get odds
def get_odd_data(url):
    soup = get_html(url, last_class)
    if soup is None:
        return
    
    table = soup.find('table', attrs={'id':table_id})  # get the table of race result
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    rows.pop(-1)
    odds_data = []
    for row_idx, row in enumerate(rows):
        col = row.find_all('td')[7]
        odd = col.span.text.strip()
        odds_data.append(odd)
    return odds_data

# get race table data
def get_race_data(url, race_no):
    soup = get_html(url, last_class)
    print('hello?')
    print('soup is none', soup is None)
    if soup is None:
        print('hello?')
        return wrong_course

    date_place = soup.find('div', attrs={'class':date_place_class})  # get the place
    race_place = date_place.find_all('nobr')[1].text.strip()
    print(race_place)
    
    total_race = soup.find('div', attrs={'class':total_race_class})  # get total races
    total_race = total_race.find_all('div')
    global total_races
    for tag in reversed(total_race):
        if tag.get('id') is not None:
            total_races = re.search(r'raceSel(\d+(?:\.\d+)?)', tag.get('id')).group(1)
            print(total_races)
            if total_races.isnumeric():
                break
    
    place_details_tag = soup.find('span', attrs={'class':place_details_class}) # get place details
    place_details = place_details_tag.text.strip().split(', ')
    print(place_details)
    race_date = place_details[1].split('/')

    # get details
    race_year = race_date[-1]
    race_month = race_date[1]
    race_day = race_date[0]
    race_class = place_details[3]
    if len(place_details) == 7:
        race_track = place_details[4]
    elif len(place_details) == 8:
        race_track = place_details[4] + ' - ' + place_details[5].split('"')[1] + ' 賽道'
    race_distance = place_details[-2].split('米')[0]
    race_going = place_details[-1]
    print(race_year, race_month, race_day, race_class, race_track, race_distance, race_going)

    table = soup.find('table', attrs={'id':table_id})  # get the table of race result
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    rows.pop(0)
    rows.pop(-1)
    row_len = len(rows)
    global data
    global location_data

    odd_url = f"https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=ch&raceno={race_no}"
    odds = get_odd_data(odd_url)

    for row_idx, row in enumerate(rows):
        cols = row.find_all('td')
        # store race table data
        row_data = [ele.text.strip().split(' ')[0] for idx, ele in enumerate(cols) if idx != 0 and idx != 2 and idx != 9 and idx != 10 and idx != 11]

        # append horse name with its code
        row_data[1] = row_data[1] + "(" + cols[3].a.get('href').split("'")[1] + ")"
        #horse_age = get_horse_data(horse_url)

        # insert data got into data in correct order
        horse_draw = row_data.pop(2)
        row_data.insert(6, horse_draw)
        horse_weight = row_data.pop(2)
        row_data.insert(4, horse_weight)
        # horse_age
        horse_age = horse_table_data[row_data[1]][6]
        row_data.insert(2, horse_age)

        row_data.insert(0, race_year)
        row_data.insert(1, race_month)
        row_data.insert(2, race_day)
        row_data.insert(3, race_no)
        row_data.insert(4, -1)
        row_data.append("time")
        row_data.append(odds[row_idx])

        # store data
        data.append(row_data)
    
    location_data.append([race_year, race_month, race_day, race_no, race_place, race_track, race_distance, race_going, race_class])
    return

def write_file(data_list, file_name, write_type):
    # open the file in the write mode
    print("1234", directory)
    try:
        f = open(directory + file_name, write_type, newline='', encoding="utf-8")
    except Exception as e:
        print(e)

    print("aaa")
    # create the csv writer
    writer = csv.writer(f)
    print("bbb")
    # write a row to the csv file
    data_len = len(data_list)
    print("ccc")
    print(data_len)
    for i in range(0, data_len):
        writer.writerow(data_list[i])

    # close the file
    f.close()

# write data got into all files
def write():
    global data
    global location_data
    print("a")
    write_file(data, 'future_race.csv', 'w')
    print("b")
    write_file(location_data, 'future_location.csv', 'w')
    print("c")

    data = []
    location_data = []

last_class = "footer"    # the last class in the webpage
date_place_class = "mtgInfoDV"
total_race_class = "racebg"
place_details_class = "content"
table_id = "horseTable"
total_races = "1"

def init():
    global directory
    directory = sys.path[1] + "future_data/"
    horse_url = "https://racing.hkjc.com/racing/information/chinese/Horse/HorseFormerName.aspx"
    get_horse_table(horse_url)

    url = "https://bet.hkjc.com/racing/index.aspx?lang=ch&raceno=" + total_races
    get_race_data(url, total_races)
    for i in range(2, int(total_races)+1):
        url = f"https://bet.hkjc.com/racing/index.aspx?lang=ch&raceno={i}"
        get_race_data(url, i)
    print("finished")
    write()

if __name__ == '__main__':
    init()