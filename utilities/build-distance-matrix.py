import sys
import requests
import json
import asyncio


def encode_key(origin, destination):
    return origin + ':' + destination


def decode_key(key):
    return key.split(':')


file_map_system_ids = open("../redis-config/mapSystemIds.tsv",'r')
output_file = open("pairwise_distances.tsv",'w')
system_names = []

for line in file_map_system_ids.readlines():
    line = line.strip().split('\t')
    system_names.append(line[1])

keys = []
for i in range(len(system_names)):
    for j in range(i, len(system_names)):
        keys.append(encode_key(system_names[i], system_names[j]))

async def get_distance(output_file, key):
    origin, destination = decode_key(key)
    distance_json = requests.get("https://everest.kaelspencer.com/jump/" + origin + '/' + destination + '/')
    if distance_json.status_code == 200:
        distance = json.loads(distance_json.text)
        distance = distance['jumps']
        print(key + '\t' + str(distance) + '\n')
        output_file.write(key + '\t' + str(distance) + '\n')
        sys.stdout.write('\r' + key)
        sys.stdout.flush()


file_map_system_ids = open("../redis-config/mapSystemIds.tsv",'r')
output_file = open("pairwise_distances.tsv",'w')
system_names = []

for line in file_map_system_ids.readlines():
    line = line.strip().split('\t')
    system_names.append(line[1])

keys = []
for i in range(len(system_names)):
    for j in range(i, len(system_names)):
        keys.append(encode_key(system_names[i], system_names[j]))

loop = asyncio.get_event_loop()
tasks = [get_distance(output_file, key) for key in keys]
print("Here we go!")
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
'''
