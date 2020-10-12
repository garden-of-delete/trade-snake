import pulsar
from pulsar.schema import *
import json
import redis

broker_url = 'pulsar://ec2-13-52-145-55.us-west-1.compute.amazonaws.com:6650'
r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=0)

client = pulsar.Client(broker_url)
consumer = client.subscribe('buy-orders', 'store-buy-orders')

