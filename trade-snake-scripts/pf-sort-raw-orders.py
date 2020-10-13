from pulsar.functions.function import Function
import json
import redis


class PfSortRawOrders(Function):

    def __init__(self):
        self.r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=0, password='insight')
        self.buy_topic = "persistent://public/default/buy-orders"
        self.sell_topic = "persistent://public/default/sell-orders"

    def process(self, item, context):
        json_msg = json.loads(item)
        # translate ids
        try:
            json_msg["system_id_name"] = self.r.get(int(json_msg["system_id"])).decode('utf-8')
            json_msg["type_id_name"] = self.r.get(int(json_msg["type_id"])).decode('utf-8')
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)
            # Message failed to be processed
            print("Error: Message processing failed")
        # route message
        if json_msg["is_buy_order"]:
            context.publish(self.buy_topic, json.dumps(json_msg).encode('utf-8'))
        else:
            context.publish(self.sell_topic, json.dump(json_msg).encode('utf-8'))
