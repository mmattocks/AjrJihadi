import sys
from tasklib import TaskWarrior

prayer_list=['Maghrib', 'Isha', 'Fajr', 'Dhuhr', 'Asr']
prayer=sys.argv[1]

if prayer in prayer_list:
    db=TaskWarrior()
    p_task=db.tasks.get(description=prayer, project='Din.Salat', status='Recurring')
    found_missed=False
    for p_ann in p_task['annotations']
        ann_split = p_ann.split(":")
        if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric() and ann_split[1] > 0:
            found_missed = True
            ann_split[1] -= 1
            p_task.remove_annotation(p_ann)
            p_task.add_annotation(ann_split[0]+':'+ann_split[1])
    if not found_missed:
        print("No missed prayers recorded for " + prayer)
    p_task.save()    
else:
    print(prayer + ' not in prayer list.')