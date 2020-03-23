from time import sleep
import requests
from bs4 import BeautifulSoup
import logging
from elasticsearch import Elasticsearch
from fileFunction import parse

host = 'http://127.0.0.1:9200'
es = Elasticsearch([host], verify_certs=True)

headers = {
    'User-Agent': 'user linux Mac, Ubuntu 18.04',
    'Pragma': 'no-cache'
}

url = 'https://www.allrecipes.com/recipes/96/salad/'
r = requests.get(url, headers=headers)
if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select('.fixed-recipe-card__h3 a')
    for link in links:
        sleep(2)
        result = parse(link['href'])
        print(result)
        print('=================================')