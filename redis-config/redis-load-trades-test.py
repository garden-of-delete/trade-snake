import redis
import json
import random
import sys

SOURCE_LIST = ['Jita','Amarr','Isanamo','Obe','Hakonen']
DESTINATION_LIST = SOURCE_LIST
ITEM_LIST = ['Iron Charge S', 'Energized Adaptive Nano Membrane I', '250mm Railgun I', 'Revelation']

r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=2, password='insight')


def random_trade():
    trade = {'id': 0, 'source': random.choice(SOURCE_LIST), 'destination': random.choice(DESTINATION_LIST),
             'total_value': random.randint(100000, 5000000000), 'item_name': random.choice(ITEM_LIST),
             'ppj': random.randint(1000, 1000000)}
    return trade


print('Generating ' + str(int(sys.argv[1])) + ' random trades...')
for i in range(int(sys.argv[1])):
    trade = random_trade()
    trade['id'] = i
    r.set(trade['id'], json.dumps(trade))
print('done!')
