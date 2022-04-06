import csv

#directory = 'C:/Users/s1155126103/Desktop/CSCI4998/'
directory = '../future_data/'

horse_dict_1920 = {}
jockey_dict_1920 = {}
trainer_dict_1920 = {}
horse_dict_2021 = {}
jockey_dict_2021 = {}
trainer_dict_2021 = {}

horse_dict_1921 = {}
jockey_dict_1921 = {}
trainer_dict_1921 = {}

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

def del_column_csv_file(file_name, cols_to_remove):
    cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first
    row_count = 0 # Current amount of rows processed

    d = read_csv_file(file_name)

    with open(directory + file_name, "w", newline='', encoding="utf-8") as result:
        writer = csv.writer(result)
        for row in d:
            row_count += 1
            print('\r{0}'.format(row_count), end='') # Print rows processed
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)

def batch_update_link(file_name, row_idx, value):
    new_data = read_csv_file(file_name)

    outp = open(directory + file_name, mode='w', newline='', encoding="utf-8")
    writer = csv.writer(outp)

    # write a row to the csv file
    for idx, row in enumerate(new_data):
        row[row_idx] = value[idx][1]
        writer.writerow(row)

    # close the file
    outp.close()

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

def read_csv_to_dict_file(file_name):
    inp = open(directory + file_name, mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    data_dict = {rows[0]:int(rows[1]) for rows in reader}
    inp.close()
    return data_dict

def compare_dict(dict_1, dict_2, new_dict):
    for key_dict_1 in dict_1:
        if key_dict_1 in dict_2:
            new_dict[key_dict_1] = dict_1[key_dict_1] + dict_2[key_dict_1] - 100
        else:
            new_dict[key_dict_1] = dict_1[key_dict_1]

def dict_to_list(dictionary, data_list):
    for k, v in dictionary.items():
        data_list.append([k, v])
    return data_list

def batch_update_age(file_name, out_file, row_idx, value):
    new_data = read_csv_file(file_name)

    outp = open(directory + out_file, mode='w', newline='', encoding="utf-8")
    writer = csv.writer(outp)

    # write a row to the csv file
    for idx, row in enumerate(new_data):
        row[row_idx] = value[idx]
        writer.writerow(row)

    # close the file
    outp.close()

if __name__ == '__main__':
    value = read_csv_file('future_location.csv')
    print('/'.join(value[-1][0:3]))
    exit()
    #del_column_csv_file('Data/1718/races.csv', [7])
    #batch_update_link('Data/1718/races.csv', 7, value)

    file_name = 'Data/1121/races_with_horse_link.csv'
    data = read_csv_file(file_name)

    age = []
    for row in data:
        link = row[7]
        start_year = link.split('_')[1]
        age.append(int(row[0])-int(start_year)+1)
    old_data = read_csv_file(file_name)
    print(age[:10])
    batch_update_age(file_name, 'Data/1121/races_with_age.csv', 7, age)

    #yyyy = '1718'
    #add = 4582
    #batch_edit_csv_file('Data/' + yyyy + '/location.csv', 3, add)
    #batch_edit_csv_file('Data/' + yyyy + '/races.csv', 3, add)

    """y1 = '1121'
    y2 = '1718'
    horse_dict_1920 = read_csv_to_dict_file('Data/' + y1 + '/horse.csv')
    jockey_dict_1920 =  read_csv_to_dict_file('Data/' + y1 + '/jockey.csv')
    trainer_dict_1920 = read_csv_to_dict_file('Data/' + y1 + '/trainer.csv')

    horse_dict_2021 = read_csv_to_dict_file('Data/' + y2 + '/horse.csv')
    jockey_dict_2021 =  read_csv_to_dict_file('Data/' + y2 + '/jockey.csv')
    trainer_dict_2021 = read_csv_to_dict_file('Data/' + y2 + '/trainer.csv')

    horse_dict_1921 = horse_dict_2021
    jockey_dict_1921 = jockey_dict_2021
    trainer_dict_1921 = trainer_dict_2021
    
    horse_data = []
    jockey_data = []
    trainer_data = []

    compare_dict(horse_dict_1920, horse_dict_2021, horse_dict_1921)
    compare_dict(jockey_dict_1920, jockey_dict_2021, jockey_dict_1921)
    compare_dict(trainer_dict_1920, trainer_dict_2021, trainer_dict_1921)

    horse_data = dict_to_list(horse_dict_1921, horse_data)
    jockey_data = dict_to_list(jockey_dict_1921, jockey_data)
    trainer_data = dict_to_list(trainer_dict_1921, trainer_data)
    
    write_csv_file(horse_data, 'Data/' + y1 + '/horse.csv', 'w')
    write_csv_file(jockey_data, 'Data/' + y1 + '/jockey.csv', 'w')
    write_csv_file(trainer_data, 'Data/' + y1 + '/trainer.csv', 'w')"""