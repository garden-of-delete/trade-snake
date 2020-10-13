from pulsar.functions.function import Function
import json
import redis


class PfCacheBuyOrders(Function):

    def __init__(self):
        self.r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=1, password='insight')

    def process(self, item, context):
        json_msg = json.loads(item.decode('utf-8'))
        self.r.set(json_msg['order_id'], json.dumps(json_msg))