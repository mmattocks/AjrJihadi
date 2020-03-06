import sys
from tasklib import TaskWarrior

prayer_list=['Maghrib', 'Isha', 'Fajr', 'Dhuhr', 'Asr']
pstring=''
for prayer in prayer_list:
    pstring+=prayer + ' '

if len(sys.argv) == 1:
    sys.exit("Which prayer was made up? " + pstring)
elif len(sys.argv) > 3 or len(sys.argv) == 3 and not sys.argv[2].isnumeric():
    sys.exit("Bad arguments. use 'makeup <prayer>' or 'makeup <prayer> <integer>'")

num_madeup=1
prayer=sys.argv[1]
if len(sys.argv) == 3:
    num_madeup=sys.argv[2]

if prayer not in prayer_list:
    sys.exit(str(prayer) + ' not in prayer list: ' + pstring)
    
db=TaskWarrior()
try:
    p_task=db.tasks.get(description=prayer, project='Din.Salat', status='Recurring')
except:
    sys.exit("No task for this prayer, make one first.")

found_missed=False
for p_ann in p_task['annotations']:
    ann_split = p_ann['description'].split(":")
    if len(ann_split) == 2 and ann_split[0] == 'MISSED' and ann_split[1].isnumeric() and ann_split[1] > 0:
        found_missed = True
        ann_split[1] -= num_madeup
        p_task.remove_annotation(p_ann)
        p_task.add_annotation(ann_split[0]+':'+ann_split[1])
        print
if not found_missed:
    print("No missed prayers recorded for " + prayer)
p_task.save()    