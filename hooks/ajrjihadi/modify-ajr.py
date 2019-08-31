import sys
import json
import os.path

#User missed prayer params
missed_path = 'missed.json'
init_missed_json = {'Maghrib':0,'Isha':0,'Fajr':0,'Dhuhr':0,'Asr':0}

old_task = json.loads(sys.argv[1])
new_task = json.loads(sys.argv[2])

#old_task = dict((key, deserialize(key, value)) for key, value in json.loads(sys.stdin.readline().strip()).items())
#new_task = dict((key, deserialize(key, value)) for key, value in json.loads(sys.stdin.readline().strip()).items())

if new_task['description'] in init_missed_json.keys() and new_task['status'] == 'DELETED':
    missed_prayer = new_task['description']
    if not os.path.exists(missed_path):
        init_missed_json[missed_prayer] += 1
        file = open(missed_path,'w+')
        json.dump(init_missed_json, file)        
    else:
        missed_json = json.loads(missed_path)
        missed_json[missed_prayer] += 1
        file = open(missed_path, 'w')
        json.dump(missed_json, file)


print(json.dumps(new_task))
sys.exit(0)