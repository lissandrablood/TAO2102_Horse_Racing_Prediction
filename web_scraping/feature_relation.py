import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

sns.set_theme(style="darkgrid")

#directory = 'C:/Users/s1155126103/Desktop/CSCI4998/'
directory = 'C:/Users/chang/Downloads/CSCI4998/'

feature_relation_dict = {}

# store csv into list
def read_csv_file(file_name):
    cnt = 1
    race_data = []  # store all race data (element is a race)
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    for row in reader:
        race_data.append(row)
    inp.close()
    return race_data

def batch_edit_csv_file(file_name, row_idx, add_value):
    new_data = read_csv_file(file_name)

    outp = open(directory + file_name, mode='w', newline='', encoding="utf-8")
    writer = csv.writer(outp)

    # write a row to the csv file
    for row in new_data:
        row[row_idx] = int(row[row_idx]) + add_value
        writer.writerow(row)

    # close the file
    outp.close()

# store all the races into a 3D list
def read_3d_csv_file(file_name):
    cnt = 1
    race_data = []  # store all race data (element is a race)
    record_data = []    # store all record in a race (element is a horse data in a race)
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    for row in reader:
        #print(row)
        #print(row[3], cnt, int(row[3]) != int(cnt))
        #input()
        if int(row[3]) != int(cnt):
            cnt = row[3]
            race_data.append(record_data)
            record_data = []
        record_data.append(row)
    race_data.append(record_data)
    inp.close()
    return race_data

def write_csv_file(data_list, file_name, write_type):
    # open the file in the write mode
    f = open(directory + file_name, write_type, newline='', encoding="utf-8")

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    for ele in data_list:
        writer.writerow(ele)

    # close the file
    f.close()

if __name__ == '__main__':
    #batch_edit_csv_file('2021/races_with_horse_link.csv', 3, 800)
    race_data = read_3d_csv_file('Data/1121/races_with_age.csv')
    #race_data = read_csv_file('Data/1121/trainer.csv')
    #print(race_data)

    no_of_races = len(race_data)
    x_name = 'Win Odd'  #x-axis name
    #y_name = 'win%'
    y_name = 'Win Percentage'
    for ele in race_data:
        #print(ele)
        #exit()
        #input()
        feature = round(float(ele[0][-1]))    # feature in which column of the 3d race_data
        if feature == '':
            continue
        #feature = ele[-1]    # feature in which column of the 2d race_data
        if feature in feature_relation_dict:
            feature_relation_dict[feature] = feature_relation_dict[feature] + 1
        else:
            feature_relation_dict[feature] = 1
    print(feature_relation_dict)

    feature_relation = []
    cnt = 0
    for ele in feature_relation_dict.items():
        value = [ele[0], float(ele[1])/7757]
        cnt = cnt + value[1]
        feature_relation.append(value)
    feature_relation = np.array(feature_relation)
    print(feature_relation)
    print('cnt', cnt)
    write_csv_file(feature_relation, 'feature_relation/' + x_name + '.csv', 'w')

    df = pd.DataFrame(feature_relation, columns =[x_name, y_name], dtype=float)
    sns.relplot(x=x_name, y=y_name, data=df)
    plt.savefig(directory + 'feature_relation/' + x_name + '.jpg')
    plt.show()