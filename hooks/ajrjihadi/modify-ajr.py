import sys
import json
import usrconfig
from tasklib import TaskWarrior

old_task = json.loads(sys.argv[1])
new_task = json.loads(sys.argv[2])

if old_task['description'] in usrconfig.prayer_list and old_task['status']=='pending' and new_task['status']=='deleted':
    db=TaskWarrior()
    p_task=db.tasks.get(uuid=old_task['parent'])
    found_missed=False
    if 'annotations' in p_task.keys():
        for ann in p_task['annotations']:
            ann_split = ann['description'].split(":")
            if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric():
                found_missed = True
                ann['description'] = 'MISSED:'+str(int(ann_split[1]) + missed)
    if not found_missed:
        from datetime import datetime
        if 'annotations' in new_task.keys():
            p_task['annotations'].append({'entry': datetime.now().isoformat(), 'description': 'MISSED:'+str(usrconfig.missed_start+missed)})
        else:
            p_task['annotations']=[{'entry': datetime.now().isoformat(), 'description': 'MISSED:'+str(usrconfig.missed_start+missed)}]

    p_task.save()

print(json.dumps(new_task))
sys.exit(0)
