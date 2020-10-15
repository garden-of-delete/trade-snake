import redis
import json
import random
import sys

file_map_system_ids = open("../redis-config/mapSystemIds.tsv",'r')
file_type_ids = open("../redis-config/typeids.csv",'r')

r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=2, password='insight')

print('Loading system names from file... ')
system_names = []
for line in file_map_system_ids.readlines():
    system_names.append(line.strip().split('\t')[1])
file_map_system_ids.close()

print('Loading item names from file... ')
item_names = []
for line in file_type_ids.readlines():
    item_names = line.strip().split(',')[1]
file_type_ids.close()


def random_trade():
    trade = {'id': 0, 'source': random.choice(system_names), 'destination': random.choice(system_names),
             'total_value': random.randint(5000000, 1000000000), 'item_name': random.choice(item_names),
             'ppj': random.randint(1000, 1000000)}
    return trade


print('Generating ' + str(int(sys.argv[1])) + ' random trades...')
for i in range(int(sys.argv[1])):
    trade = random_trade()
    trade['id'] = i
    r.set(trade['id'], json.dumps(trade))
print('done!')
