from tasklib import TaskWarrior

prayer_list=['Maghrib', 'Isha', 'Fajr', 'Dhuhr', 'Asr']

db=TaskWarrior()

for prayer in prayer_list
    p_task=db.tasks.get(uuid=new_task['parent'])
    found_missed = False
    for p_ann in p_task['annotations']:
        ann_split = p_ann.split(":")
        if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric() and ann_split[1] > 0:
            found_missed = True
            print(prayer + " : " + str(ann_split[1]))
        else:
            print(prayer + " : " + "0")

