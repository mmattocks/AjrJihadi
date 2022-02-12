import time
import sys
import json
import ajrSalat
import usrconfig

task = json.loads(sys.argv[1])
if task['description'] in usrconfig.prayer_list:
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
    db=TaskWarrior()
    p_task=db.tasks.get(uuid=task['parent'])
    due_shift = task['due'] - p_task['due']

    time_attributes = ('wait', 'scheduled', 'until')
    for att in time_attributes:
        if p_task[attr]:
            task[attr] = p_task[attr] + due_shift

elif usrconfig.recur_cull:
    from datetime import datetime, timedelta
    from ajrSalat import tw_ISO8601_to_local_dt, dateTimeFormat
    task['until'] = (tw_ISO8601_to_local_dt(task['due'],((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60)) + timedelta(days=usrconfig.until_tds[task['recur']])).isoformat()

print(json.dumps(task))
sys.exit(0)