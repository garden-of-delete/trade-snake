import requests
import pulsar
import time
from pulsar.schema import *
import json

SLEEP_TIME = 1
broker_url = "pulsar://ec2-13-52-145-55.us-west-1.compute.amazonaws.com:6650"

client = pulsar.Client(broker_url)
#producer = client.create_producer(topic='raw-orders',producer_name='market-producer',schema=StringSchema())

region_ids = requests.get("https://esi.evetech.net/latest/universe/regions/?datasource=tranquility")
region_ids = region_ids.text[1:-1].split(',')
region_ids = [x for x in map(int,region_ids) if x < 11000000] #filter out wh region ids

market_pull_index = 0
while(True):
    payload = {'datasource':'tranquility','ordertype':'all','page':'1'}
    for i in region_ids:
        j = 1
        n_pages = 2
        while j < n_pages + 1:
            payload['page'] = str(j)
            r = requests.get("https://esi.evetech.net/latest/markets/" + repr(i) + "/orders/", payload)
            n_pages = int(r.headers['x-pages'])
            for k in r.json():
                print(json.dumps(k))
                #producer.send(json.dumps(k))
            j += 1
    market_pull_index += 1
    time.sleep(SLEEP_TIME)

