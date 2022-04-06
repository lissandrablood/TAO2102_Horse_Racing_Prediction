import csv

c_to_e = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10'}
course = [
    ['沙田', 'ST'],
    ['跑馬地', 'HV']
]
year = 2020

#directory = 'C:/Users/s1155126103/Desktop/CSCI4998/Data/'
directory = 'C:/Users/chang/Downloads/CSCI4998/Data/'

def chi_to_eng(char):
    if len(char) == 1:
        return c_to_e[char]
    elif len(char) == 2:
        if char[0] == '十':
            return '1' + c_to_e[char[1]]
        elif char[1] == '十':
            return c_to_e[char[0]] + '0'
    elif len(char) == 3:
        return c_to_e[char[0]] + c_to_e[char[2]]

def read_csv_file(file_name):
    global year
    dates = []
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    for row in reader:
        if row[1] == '' and row[2] == '':
            if row[0] == '':
                continue
            else:
                year = year + 1
                continue
        else:
            print(row)
            temp = row[0].split('月')
            month = chi_to_eng(temp[0])
            day = chi_to_eng(temp[1].split('日')[0])

            if course[0][0] in row[2]:
                location = course[0][1]
            elif course[1][0] in row[2]:
                location = course[1][1]
            
            dates.append([year, month, day, location])
    inp.close()
    return dates

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

if __name__ == '__main__':
    dates = read_csv_file('2122.csv')
    write_file(dates, '2122_racing_dates.csv', 'w')
    print(dates)