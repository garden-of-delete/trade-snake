import redis

r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=0, password='insight')

file_map_region_ids = open("mapRegionIds.tsv",'r')
file_map_system_ids = open("mapSystemIds.tsv",'r')
file_type_ids = open("typeids.csv",'r')

print('Loading region ids and names from file... ')
for line in file_map_region_ids.readlines():
    line = line.strip().split('\t')
    r.set(int(line[0]), line[1])
file_map_region_ids.close()
print('done!')

print('Loading system ids and names from file... ')
for line in file_map_system_ids.readlines():
    line = line.strip().split('\t')
    r.set(int(line[0]), line[1])
file_map_system_ids.close()
print('done!')

print('Loading item ids and names from file... ')
for line in file_type_ids.readlines():
    line = line.strip().split(',')
    r.set(int(line[0]), line[1])
file_type_ids.close()
print('done!')
