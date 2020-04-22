import sys
import json
import usrconfig
from tasklib import TaskWarrior

old_task = json.loads(sys.argv[1])
new_task = json.loads(sys.argv[2])

print(new_task,file=sys.stderr)

if (old_task['description'] in usrconfig.prayer_list and old_task['status']=='pending' and new_task['status']=='deleted') or (old_task['description']=='woo'):
    db=TaskWarrior()
    print("hoo!!",file=sys.stderr)
    p_task=db.tasks.get(uuid=old_task['parent'])
    print("woo!!",file=sys.stderr)
    found_missed=False
    if 'annotations' in p_task._data.keys():
        for ann in p_task['annotations']:
            ann_split = ann['description'].split(":")
            if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric():
                found_missed = True
                p_task.remove_annotation(ann)
                p_task.add_annotation('MISSED:'+str(int(ann_split[1]) + 1))
    if not found_missed:
        p_task.add_annotation('MISSED:'+str(usrconfig.missed_start + 1))
    p_task.save()

print(json.dumps(new_task))
sys.exit(0)
