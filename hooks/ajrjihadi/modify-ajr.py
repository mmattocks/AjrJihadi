import sys
import json
import os.path

#User missed prayer params
track_missed=True
prayer_list=['Maghrib', 'Isha', 'Fajr', 'Dhuhr', 'Asr']
missed_start=1460

old_task = json.loads(sys.argv[1])
new_task = json.loads(sys.argv[2])

if track_missed and new_task['status'] == 'DELETED' and new_task['description'] in prayer_list:
    from tasklib import TaskWarrior

    db=TaskWarrior()
    p_task=db.tasks.get(uuid=new_task['parent'])
    found_missed = False
    for p_ann in p_task['annotations']:
        ann_split = p_ann.split(":")
        if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric():
            found_missed = True
            ann_split[1] += 1
            p_task.remove_annotation(p_ann)
            p_task.add_annotation(ann_split[1]+':'+ann_split[2])
    if not found_missed:
        p_task.add_annotation('MISSED:'+(missed_start+1))
    p_task.save()
else:
    print(json.dumps(new_task))
    
sys.exit(0)