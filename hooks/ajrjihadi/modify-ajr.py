import sys
import json
import os.path
import usrconfig

new_task = json.loads(sys.argv[1])

if usrconfig.track_missed and new_task['status'] == 'deleted' and new_task['description'] in usrconfig.prayer_list:
    from tasklib import TaskWarrior

    db=TaskWarrior()
    p_task=db.tasks.get(uuid=new_task['parent'])
    found_missed = False
    for p_ann in p_task['annotations']:
        ann_split = p_ann['description'].split(":")
        if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric():
            found_missed = True
            new_missed = int(ann_split[1]) + 1
            p_task.remove_annotation(p_ann)
            p_task.add_annotation(ann_split[0]+':'+str(new_missed))
    if not found_missed:
        p_task.add_annotation('MISSED:'+str(usrconfig.missed_start+1))
    p_task.save()
else:
    print(json.dumps(new_task))
    
sys.exit(0)