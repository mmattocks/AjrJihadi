import sys
import json
import usrconfig
from tasklib import TaskWarrior

task = json.loads(sys.argv[1])

if task['description'] in usrconfig.prayer_list and task['status']=='deleted':
    db=TaskWarrior()
    p_task=db.tasks.get(uuid=task['parent'])
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

sys.exit(0)
