from tasklib import TaskWarrior
import usrconfig

db=TaskWarrior()

for prayer in usrconfig.prayer_list:
    try:
        p_task=db.tasks.get(description=prayer, project='Din.Salat', status='Recurring')
        found_missed = False
        if len(p_task['annotations'])>=1:
            for p_ann in p_task['annotations']:
                ann_split = p_ann.split(":")
                if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric() and ann_split[1] > 0:
                    found_missed = True
                    print(prayer + " : " + str(ann_split[1]))
        if not found_missed:
            p_task.add_annotation('MISSED:'+str(usrconfig.missed_start+1))
            p_task.save()
            print(prayer + " : " + str(usrconfig.missedstart))
    except:
        print (prayer + " : " + "-")
    


