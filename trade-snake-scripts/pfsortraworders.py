from pulsar.functions.function import Function
import json
import redis


class PfSortRawOrders(Function):

    def __init__(self):
        self.r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=1)
        self.buy_topic = '/public/default/buy-orders'
        self.sell_topic = '/public/default/sell-orders'

    def process(self, item, context):
        json_msg = json.loads(item)
        # translate ids
        json_msg["system_id_name"] = self.r.get(int(json_msg["system_id"])).decode('utf-8')
        json_msg["type_id_name"] = self.r.get(int(json_msg["type_id"])).decode('utf-8')
        # r.set("type_id_name",r.get(int(json_msg["type_id"])))
        # r.set("system_id_name", r.get(int(json_msg["system_id"])))
        # route message
        if json_msg["is_buy_order"]:
            context.publish(self.buy_topic, item)
        else:
            context.publish(self.sell_topic, item)
