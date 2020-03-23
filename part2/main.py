from fileFunction import isElasticServerConnected, createIndexType, isElasticServerConnected
from elasticsearch import Elasticsearch

host = 'http://127.0.0.1:9200'
es = Elasticsearch([host], verify_certs=True)
isElasticServerConnected()
# 4
createIndexType(es)

# 5
