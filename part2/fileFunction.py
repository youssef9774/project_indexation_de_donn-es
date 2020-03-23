from elasticsearch import Elasticsearch
import requests
from time import sleep
from bs4 import BeautifulSoup
import json
from pprint import pprint

def parse(u):
    title = '-'
    submit_by = '-'
    description = '-'
    calories = 0
    ingredients = []
    rec = {}
    
    headers = {
        'User-Agent': 'user linux Mac, Ubuntu 18.04',
        'Pragma': 'no-cache'
    }

    try:
        r = requests.get(u, headers=headers)
 
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            # title
            title_section = soup.select('.recipe-summary__h1')
            # submitter
            submitter_section = soup.select('.submitter__name')
            # description
            description_section = soup.select('.submitter__description')
            # ingredients
            ingredients_section = soup.select('.recipe-ingred_txt')
            # calories
            calories_section = soup.select('.calorie-count')
            if calories_section:
                calories = calories_section[0].text.replace('cals', '').strip()
 
            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if 'Add all ingredients to list' not in ingredient_text and ingredient_text != '':
                        ingredients.append({'step': ingredient.text.strip()})
 
            if description_section:
                description = description_section[0].text.strip().replace('"', '')
 
            if submitter_section:
                submit_by = submitter_section[0].text.strip()
 
            if title_section:
                title = title_section[0].text
 
            rec = {'title': title, 'submitter': submit_by, 'description': description, 'calories': calories,
                   'ingredients': ingredients}
    except Exception as ex:
        print('Exception while parsing')
        print(str(ex))
    finally:
        return json.dumps(rec)

def isElasticServerConnected():
    #"Greater than 2" if n > 2 else "Smaller than or equal to 2"
    try:
        r = requests.get('http://localhost:9200/_cluster/health', headers={'Content-type': 'application/json'})
        print('Vous n\'êtes pas connecté') if not r.json() else print('Vous êtes connecté')
    except:
        print('Vous n\'êtes pas connecté')
    return

def createIndexType(es, indexName='recipes'):    
    parameters = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings" : {
            "recipe" : {
                "dynamic" : "strict",
                "properties" : {
                    "calories" : {"type" : "integer"},
                    "description" : {"type" : "text"},
                    "submitter" : {"type" : "text"},
                    "title" : {"type" : "text"},
                    "ingredients" : {"type" : "nested", "properties" : {"step" : { "type" : "text"}}
                   }
                }
            }
        }
    }
    try :
        if not es.indices.exists(indexName):
            # es.indices.create(index=indexName, ignore=400, body=settings)
            es.indices.create(index=indexName, body=parameters)
            print('Index crée avec succès')
    except Exception as ex:
        print(str(ex))
    return

#5
def addRecord(es_object, indexName, record):
    try:
        es_object.index(index=indexName, doc_type='recipe', body=record)
    except Exception as ex:
        print('Error d\'indexation')
        print(str(ex))
    return
#6
def saladSearch(es, indexName='recipes', calorie=102, title='Awesome'):
    # Search salad clories = 102 && 
    search = {
            "query":{
                "bool": {
                "must": [
                    { "match": {"fields.calories": calorie}},
                    { "match": {"fields.title": title}},
                    { "match": {"fields.title": "S*"}}
                ]
            }
        }
    }
    res = es.search(index=indexName, body=search)
    return res


def scrapWebSite(url):
    return requests.get(url)