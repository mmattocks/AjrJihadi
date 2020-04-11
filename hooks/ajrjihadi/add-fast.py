import sys
import usrconfig
from datetime import datetime

dates=[]

if len(sys.argv) > 3 or len(sys.argv) < w:
    sys.exit("Bad arguments. use one (single day) or two (range of dates) date values")

if len(sys.argv) == 2:
    try:
        dates.append(datetime.strptime(sys.argv[1]))
    except:
        sys.exit("Bad date format on date argument " +str(i) + ", must be YYYY-MM-DD.")
else:
    try:
        date1 = datetime.strptime(sys.argv[1])
        date2 = datetime.strptime(sys.argv[2])
        if date2 <= date1:
            sys.exit("Bad arguments. Second date must be later than first")
        else:
            pushdate=date1
            while pushdate <= date2:
                dates.append(pushdate)
                pushdate+=timedelta(days=1)
    except:
        sys.exit("Bad date format on date argument " +str(i) + ", must be YYYY-MM-DD.")

import time
from tasklib import Task, TaskWarrior

db=TaskWarrior()

for date in dates:
    [wait, scheduled, due, until] = ajrSalat.getSawmTime(task['due'],
                                                    usrconfig.coords,
                                                    ((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60),
                                                    method=usrconfig.methodName,
                                                    dst=time.localtime().tm_isdst,
                                                    waitpad=usrconfig.sawmWaitpad,
                                                    untilpad=usrconfig.sawmUntilpad)

    sawm_task = Task(db, description=usrconfig.sawmDesc, wait=wait, scheduled=scheduled, due=due, until=until)
    sawm_task.save()