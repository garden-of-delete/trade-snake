import requests
import pulsar
import time
from pulsar.schema import *
import json
import time

SLEEP_TIME = 0
broker_url = "pulsar://ec2-13-52-145-55.us-west-1.compute.amazonaws.com:6650"

client = pulsar.Client(broker_url)
producer = client.create_producer(topic='raw-orders', producer_name='market-producer', schema=StringSchema())
market_stats_producer = client.create_producer(topic='market-stats', producer_name='market-stats-producer', schema=StringSchema())

region_ids = requests.get("https://esi.evetech.net/latest/universe/regions/?datasource=tranquility")
region_ids = region_ids.text[1:-1].split(',')
region_ids = [x for x in map(int,region_ids) if x < 11000000]

while(True):
    current_market_stats = {'market_pull_index': 0, 'n_orders': 0, 'pull_time': time.time()}
    payload = {'datasource':'tranquility','ordertype':'all','page':'1'}
    for region in region_ids:
        page = 1
        n_pages = 2
        while page < n_pages + 1:
            payload['page'] = str(page)
            r = requests.get("https://esi.evetech.net/latest/markets/" + repr(region) + "/orders/", payload)
            n_pages = int(r.headers['x-pages'])
            for k in r.json():
                #print(json.dumps(k))
                producer.send(json.dumps(k))
                current_market_stats['n_orders'] += 1
            page += 1
    current_market_stats['market_pull_index'] += 1
    current_market_stats['pull_time'] = time.time() - current_market_stats['pull_time']
    market_stats_producer.send(json.dumps(current_market_stats))
    time.sleep(SLEEP_TIME)

