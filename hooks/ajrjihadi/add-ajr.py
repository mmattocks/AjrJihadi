import time
import sys
import json
import ajrSalat
import usrconfig

task = json.loads(sys.argv[1])
if task['description'] in usrconfig.prayer_list:
    [wait, scheduled, due, until], descmod = ajrSalat.getSalatTime(task['description'],
                                                    task['due'],
                                                    usrconfig.coords,
                                                    ((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60),
                                                    asr=usrconfig.asrMethodName,
                                                    method=usrconfig.methodName,
                                                    dst=time.localtime().tm_isdst,
                                                    waitpad=usrconfig.salatWaitpad,
                                                    untilpad=usrconfig.salatUntilpad)

    task['wait'], task['scheduled'], task['due'], task['until'] = wait, scheduled, due, until

    if descmod != '': #if there's a modified description, assign it
        task['description'] = descmod
else:
    from datetime import datetime
    from tasklib import TaskWarrior
    from ajrSalat import tw_ISO8601_to_local_dt, dateTimeFormat
    db=TaskWarrior()
    parent_task=db.tasks.get(uuid=task['uuid'])
    parent_due=parent_task['due']; parent_wait=parent_task['wait']; parent_sched=parent_task['scheduled']; parent_until=parent_task['until']
    child_due=tw_ISO8601_to_local_dt(task['due'],((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60))
    task['wait']=(child_due+(parent_wait-parent_due)).isoformat()
    task['scheduled']=(child_due+(parent_sched-parent_due)).isoformat()
    task['until']=(child_due+(parent_until-parent_due)).isoformat()

print(json.dumps(task))
sys.exit(0)