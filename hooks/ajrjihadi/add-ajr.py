import sys
import json

task = json.loads(sys.argv[1])
if task['description'] in usrconfig.prayer_list:
    import time
    import ajrSalat
    import usrconfig


    [task['wait'], task['scheduled'], task['due'], task['until']], descmod = ajrSalat.getSalatTime(task['description'],
                                                    task['due'],
                                                    usrconfig.coords,
                                                    ((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60),
                                                    asr=usrconfig.asrMethodName,
                                                    method=usrconfig.methodName,
                                                    dst=time.localtime().tm_isdst,
                                                    waitpad=usrconfig.salatWaitpad,
                                                    untilpad=usrconfig.salatUntilpad)

    if descmod != '': #if there's a modified description, assign it
        task['description'] = descmod

else:
    from tasklib import TaskWarrior
    from datetime import datetime
    db=TaskWarrior()
    db.overrides.update(dict(recurrence="no", hooks="no"))
    
    fmt = "%Y%m%dT%H%M%S%z"
    p_task=db.tasks.get(uuid=task['parent'])
    due_shift = datetime.strptime(task['due'],fmt) - p_task['due']

    time_attributes = ('wait', 'scheduled', 'until')
    for attr in time_attributes:
        if p_task[attr]:
            attrtime = p_task[attr] + due_shift
            task[attr] = datetime.strftime(attrtime,fmt)

print(json.dumps(task))
sys.exit(0)
