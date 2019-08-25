import sys
import json
import os.path

#User missed prayer params
missed_path = 'missed.json'
init_missed_json = {'Maghrib':0,'Isha':0,'Fajr':0,'Dhuhr':0,'Asr':0}

task = json.loads(sys.argv[1])
if task['description'] in init_missed_json.keys() and task['status'] == 'DELETED':
    missed_prayer = task['description']
    if not os.path.exists(missed_path):
        init_missed_json[missed_prayer] += 1
        file = open(missed_path,'w+')
        json.dump(init_missed_json, file)        
    else:
        missed_json = json.loads(missed_path)
        missed_json[missed_prayer] += 1
        file = open(missed_path, 'w')
        json.dump(missed_json, file)


print(json.dumps(task))
sys.exit(0)