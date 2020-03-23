
import pandas as pd 
import json
from collections import OrderedDict

def menuProgam():
    print('1. Charger donner dans un dataframe \n')
    print('2. Convertir le fichier csv en json \n')
    print('3. Indexer le fichier json dans ElasticSearch')

def chargerData(urlToCsv):
    df=pd.read_csv(urlToCsv, sep=',', encoding='latin-1',header=0)
    return df
    
def convertCsvJson(df) :
    data = []
    index_line = { "index" : { "_index" : "series", "_type" : "serie" } }
    for i in range(0, len(df)):
        document = OrderedDict()
        document["Title"] = df.iloc[i]['title']
        document["Rating"] = df.iloc[i]['rating']
        document["RatingLevel"] = df.iloc[i]['ratingLevel']
        document["ratingDescription"] = int(df.iloc[i]['ratingDescription'])
        document["release year"] = int(df.iloc[i]['release year'])
        document["user rating score"] = df.iloc[i]['user rating score']
        document["user rating size"] = int(df.iloc[i]['user rating size'])
        data.append(document)

    with open('netflix_shows.json', 'w') as f:
        for d in data:
            json.dump(index_line, f)
            f.write("\n")
            json.dump(d, f)
            f.write("\n")
    return