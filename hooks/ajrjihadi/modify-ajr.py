import sys
import json
import usrconfig

old_task = json.loads(sys.argv[1])
new_task = json.loads(sys.argv[2])

if old_task['description'] in usrconfig.prayer_list:
    missed=0

    if 'mask' in old_task.keys() and 'mask' in new_task.keys():
        missed = new_task['mask'].count('X') - old_task['mask'].count('X')

    if missed > 0:
        found_missed=False
        if 'annotations' in new_task.keys():
            for ann in new_task['annotations']:
                ann_split = ann['description'].split(":")
                if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric():
                    found_missed = True
                    ann['description'] = 'MISSED:'+str(int(ann_split[1]) + missed)
        if not found_missed:
            from datetime import datetime
            if 'annotations' in new_task.keys():
                new_task['annotations'].append({'entry': datetime.now().isoformat(), 'description': 'MISSED:'+str(usrconfig.missed_start+missed)})
            else:
                new_task['annotations']=[{'entry': datetime.now().isoformat(), 'description': 'MISSED:'+str(usrconfig.missed_start+missed)}]

print(json.dumps(new_task))
sys.exit(0)
