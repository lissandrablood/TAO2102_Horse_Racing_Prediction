from re import A
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import BetSerializer
from .models import Bet
import model

import numpy as np
import tensorflow as tf
import pickle
import pandas as pd
import sklearn.preprocessing as preprocessing
import sklearn.model_selection as model_selection
import matplotlib.pyplot as plt
import csv
import json
import sys
sys.path.insert(1, sys.path[0].split("software")[0])

# Create your views here.
def main(request):
    return HttpResponse('Hello')

def getBets(request):
    bets = Bet.objects.all()
    serialized = BetSerializer(bets, many=True)
    return JsonResponse(serialized.data, safe=False)

def getPrediction(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    modeltype = body['bet']
    #win, place, quinella, quinella place, trio, forecast, tierce, first four, quartet
    print("typeBET:", modeltype)
    if(modeltype == 'win'):
        model = tf.keras.models.load_model('../../../data/win2-model')
    elif(modeltype == 'place'):
        model = tf.keras.models.load_model('../../../data/place-model')
    elif(modeltype == 'quinella'):
        model = tf.keras.models.load_model('../../../data/quinella-model')
    elif(modeltype == 'quinella place'):
        model = tf.keras.models.load_model('../../../data/quinellaplace-model')
    elif(modeltype == 'trio'):
        model = tf.keras.models.load_model('../../../data/trio-model')
    elif(modeltype == 'forecast'):
        model = tf.keras.models.load_model('../../../data/forecast-model')
    elif(modeltype == 'tierce'):
        model = tf.keras.models.load_model('../../../data/tierce-model')
    elif(modeltype == 'first four'):
        model = tf.keras.models.load_model('../../../data/firstfour-model')
    elif(modeltype == 'quartet'):
        model = tf.keras.models.load_model('../../../data/quartet-model')
    #model = tf.keras.models.load_model('../../../data/my-model')
    location_df = pd.read_csv('../../../future_data/future_location.csv')
    location_df = location_df[['races_id', 'venue', 'track','distance','going']] #item you need

    location_df['venue'] = location_df['venue'].replace(['沙田'], 0)
    location_df['venue'] = location_df['venue'].replace(['跑馬地'], 1)

    location_df['track'] = location_df['track'].replace(['全天候跑道'], 0.0)
    location_df['track'] = location_df['track'].replace(['草地 - A 賽道'], 1.0)
    location_df['track'] = location_df['track'].replace(['草地 - A+3 賽道'], 2.0)
    location_df['track'] = location_df['track'].replace(['草地 - B 賽道'], 3.0)
    location_df['track'] = location_df['track'].replace(['草地 - B+2 賽道'], 4.0)
    location_df['track'] = location_df['track'].replace(['草地 - C 賽道'], 5.0)
    location_df['track'] = location_df['track'].replace(['草地 - C+3 賽道'], 6.0)

    location_df['going'] = location_df['going'].replace(['好地'], 0.0)
    location_df['going'] = location_df['going'].replace(['好地至快地'], 1.0)
    location_df['going'] = location_df['going'].replace(['好地至黏地'], 2.0)
    location_df['going'] = location_df['going'].replace(['快地'], 3.0)
    location_df['going'] = location_df['going'].replace(['慢地'], 4.0)
    location_df['going'] = location_df['going'].replace(['濕快地'], 5.0)
    location_df['going'] = location_df['going'].replace(['濕慢地'], 6.0)
    location_df['going'] = location_df['going'].replace(['軟地'], 7.0)
    location_df['going'] = location_df['going'].replace(['黏地'], 8.0)
    location_df['going'] = location_df['going'].replace(['黏地至軟地'], 9.0)

    races_df = pd.read_csv('../../../future_data/future_race.csv')
    races_df = races_df.dropna()
    races_df = races_df[['races_id', 'horse_id', 'horse', 'age' ,'jockey' ,'trainer','horse_weight','actual_weight','draw','odd','result']]
    races_df = races_df.dropna()

    horse_df = pd.read_csv('../../../data/horse.csv')
    jockey_df = pd.read_csv('../../../data/jockey.csv')
    trainer_df = pd.read_csv('../../../data/trainer.csv')

    races_df = pd.merge(races_df, horse_df, on = ['horse'])
    races_df = pd.merge(races_df, jockey_df, on = ['jockey'])
    races_df = pd.merge(races_df, trainer_df, on = ['trainer'])
    races_df = races_df[['races_id', 'horse_id', 'horse_marks' ,'age' ,'jockey_marks' ,'trainer_marks','horse_weight','actual_weight','draw','odd','result']]

    def group_horse_and_result(element):
        if element[0] == 'result':
            return 100 + element[1] # to make sure results are put near the end
        else:
            return element[1]   

    races_df = races_df.pivot(index='races_id', columns='horse_id', values=races_df.columns[2:])
    rearranged_columns = sorted(list(races_df.columns.values), key=group_horse_and_result)
    races_df = races_df[rearranged_columns]


    races_df = races_df.fillna(0)
    races_df = races_df.astype('float') 
 
    data = location_df.join(races_df, on='races_id', how='right')
    X = data[data.columns[:-14]] 
    ss = preprocessing.StandardScaler()
    X = pd.DataFrame(ss.fit_transform(X),columns = X.columns)
    y = data[data.columns[-14:]]

    result = []
    table = []
    count = 0
    
    predictions = model.predict(X)
    #predictions = [['4', '6', '7', '1'], ['4', '3', '5', '8'], ['1', '8', '5', '3'], ['12', '8', '10', '4'], ['13', '2', '7', '10'], ['2', '9', '1', '12'], ['8', '11', '9', '7'], ['4', '7', '12', '5'], ['2', '3', '4', '9'], ['2', '9', '5', '4'], ['10', '9', '5', '12'], ['3', '8', '10', '12']]
    for prediction in predictions:
        result.append([])
        for x in range(4):
            result[count].append(str(np.argmax(prediction) + 1))
            prediction[int(str(np.argmax(prediction)))] = 0
        count = count + 1

    
    
    year = body['year']
    month = body['month']
    day = body['day']
    raceNo = body['raceNo']
    count = 0

    if(modeltype == 'win' or modeltype == 'place'):
        for x in range(1):
            table.append([])
            test1 = pd.read_csv('../../../future_data/future_race.csv')
            test1 = test1[test1['races_id'] == int(raceNo)]
            test1 = test1[test1['horse_id'] == float(result[int(raceNo)][x])]
            test1 = test1[['horse_id', 'horse','jockey']]
            table[count].append(int(test1.iat[0, 0]))
            table[count].append(test1.iat[0, 1])
            table[count].append(test1.iat[0, 2])
            count = count + 1
    

    elif(modeltype == 'quinella' or modeltype == 'quinella place' or modeltype == 'forecast'):
        for x in range(2):
            table.append([])
            test1 = pd.read_csv('../../../future_data/future_race.csv')
            test1 = test1[test1['races_id'] == int(raceNo)]
            test1 = test1[test1['horse_id'] == float(result[int(raceNo)][x])]
            test1 = test1[['horse_id', 'horse','jockey']]
            table[count].append(int(test1.iat[0, 0]))
            table[count].append(test1.iat[0, 1])
            table[count].append(test1.iat[0, 2])
            count = count + 1

    elif(modeltype == 'trio' or modeltype == 'tierce'):
        for x in range(3):
            table.append([])
            test1 = pd.read_csv('../../../future_data/future_race.csv')
            test1 = test1[test1['races_id'] == int(raceNo)]
            test1 = test1[test1['horse_id'] == float(result[int(raceNo)][x])]
            test1 = test1[['horse_id', 'horse','jockey']]
            table[count].append(int(test1.iat[0, 0]))
            table[count].append(test1.iat[0, 1])
            table[count].append(test1.iat[0, 2])
            count = count + 1

    elif(modeltype == 'quartet' or modeltype == 'first four'):
        for x in range(4):
            table.append([])
            test1 = pd.read_csv('../../../future_data/future_race.csv')
            test1 = test1[test1['races_id'] == int(raceNo)]
            test1 = test1[test1['horse_id'] == float(result[int(raceNo)][x])]
            test1 = test1[['horse_id', 'horse','jockey']]
            table[count].append(int(test1.iat[0, 0]))
            table[count].append(test1.iat[0, 1])
            table[count].append(test1.iat[0, 2])
            count = count + 1
    
    #for x in range(4):
    #    table.append([])
    #    test1 = pd.read_csv('../../../future_data/future_race.csv')
    #    test1 = test1[test1['races_id'] == int(raceNo)]
    #    test1 = test1[test1['horse_id'] == float(result[int(raceNo)][x])]
    #    test1 = test1[['horse_id', 'horse','jockey']]
    #    table[count].append(int(test1.iat[0, 0]))
    #    table[count].append(test1.iat[0, 1])
    #    table[count].append(test1.iat[0, 2])
    #    count = count + 1

    print(table)
    jsonResult = json.dumps(table, ensure_ascii=False)

    return JsonResponse(jsonResult, safe = False, json_dumps_params={'ensure_ascii':False})


def getHorseDetails(request):
    #request.body.xxx
    races_df = pd.read_csv('../../../future_data/future_race.csv')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    year = body['year']
    month = body['month']
    day = body['day']
    raceNo = body['raceNo']
    table = []
    count = 0
    

    test = races_df.loc[races_df['races_id'] == int(raceNo)]
    
    test = test[['year', 'month', 'day', 'races_id', 'horse_id', 'horse', 'jockey']]

    total = len(test.index)

    for x in range(total):
        table.append([])
        table[count].append(x + 1)
        table[count].append(test.iat[x, 5])
        table[count].append(test.iat[x, 6])
        count = count + 1

    
    jsonTable = json.dumps(table, ensure_ascii=False)

    return JsonResponse(jsonTable, safe = False, json_dumps_params={'ensure_ascii':False})

def getRaceDate(request):
    race_date, total_races, location = _getRaceDate()
    return JsonResponse({'raceDate': race_date, 'totalRaces': total_races, 'location': location})

def _getRaceDate():
    race_data = []  # store all race data (element is a race)
    inp = open(sys.path[1] + "future_data/" + 'future_location.csv', mode='r', encoding="utf-8")
    reader = csv.reader(inp)
    for row in reader:
        race_data.append(row)
    inp.close()
    race_date = '/'.join(race_data[-1][0:3])
    print(race_date)
    return (race_date, race_data[-1][3], race_data[-1][4])

def updateRace(request):
    from web_scraping.get_future_race import init
    
    try:
        init()
    except:
        return JsonResponse({'status':'false'})

    race_date, total_races, location = _getRaceDate()
    print(race_date)
    return JsonResponse({'status':'true', 'raceDate': race_date['raceDate'], 'totalRaces': total_races, 'location': location})