# question 4
from elasticsearch import Elasticsearch
from fileFunction import createIndexType

es = Elasticsearch(['http://127.0.0.1:9200'], verify_certs=True)
# ignore 400 cause by IndexAlreadyExistsException when creating an index
index = 'recipes'
createIndexType(es, index)
