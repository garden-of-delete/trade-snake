import pulsar
from pulsar.schema import *
import json
import redis

broker_url = 'pulsar://ec2-13-52-145-55.us-west-1.compute.amazonaws.com:6650'
r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=0)

client = pulsar.Client(broker_url)
consumer = client.subscribe('raw-orders','sort-raw-orders')
buy_producer = client.create_producer(topic='buy-orders',producer_name='buy-order-producer',schema=StringSchema())
sell_producer = client.create_producer(topic='sell-orders',producer_name='sell-order-producer',schema=StringSchema())

while True:
    msg = consumer.receive()
    try:
        json_msg = json.loads(msg.data())
        # translate ids
        json_msg["system_id_name"] = r.get(int(json_msg["system_id"])).decode('utf-8')
        json_msg["type_id_name"] = r.get(int(json_msg["type_id"])).decode('utf-8')
        # r.set("type_id_name",r.get(int(json_msg["type_id"])))
        # r.set("system_id_name", r.get(int(json_msg["system_id"])))
        # route message
        if json_msg["is_buy_order"]:
            buy_producer.send(json.dumps(json_msg))
        else:
            sell_producer.send(json.dumps(json_msg))
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)

    except Exception as inst:
        print(type(inst))  # the exception instance
        print(inst.args)  # arguments stored in .args
        print(inst)
        # Message failed to be processed
        print("Error: Message processing failed")
        consumer.negative_acknowledge(msg)
