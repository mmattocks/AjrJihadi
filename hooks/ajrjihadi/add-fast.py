import sys
import ajrSalat
import usrconfig
from datetime import datetime, timedelta

dates=[]

if len(sys.argv) > 3 or len(sys.argv) < 2:
    sys.exit("Bad arguments. use one (single day), one comma separated list (list of dates), or two (range of dates) date values")

if len(sys.argv) == 2:
    argdates=sys.argv[1].split(',')
    if len(argdates) == 1:
        try:
            dates.append(datetime.strptime(sys.argv[1], '%Y-%m-%d'))
        except:
            sys.exit("Bad date format on date argument, must be YYYY-MM-DD.")
    else:
        for date in argdates:
            try:
                dates.append(datetime.strptime(date, '%Y-%m-%d'))
            except:
                sys.exit("Bad date format on date argument " + date + ", must be YYYY-MM-DD.")
else:
    try:
        date1 = datetime.strptime(sys.argv[1], '%Y-%m-%d')
        date2 = datetime.strptime(sys.argv[2], '%Y-%m-%d')
        if date2 <= date1:
            sys.exit("Bad arguments. Second date must be later than first")
        else:
            pushdate=date1
            while pushdate < date2:
                dates.append(pushdate)
                pushdate+=timedelta(days=1)
    except:
        sys.exit("Bad date format on date arguments, must be YYYY-MM-DD.")

import time
from tasklib import Task, TaskWarrior

db=TaskWarrior()

for date in dates:
    [wait, scheduled, due, until] = ajrSalat.getSawmTime(date,
                                                    usrconfig.coords,
                                                    ((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60),
                                                    method=usrconfig.methodName,
                                                    dst=time.localtime().tm_isdst,
                                                    waitpad=usrconfig.sawmWaitpad,
                                                    untilpad=usrconfig.sawmUntilpad)

    sawm_task = Task(db, description=usrconfig.sawmDesc, project=usrconfig.sawmProject, wait=wait[0:19], scheduled=scheduled[0:19], due=due[0:19], until=until[0:19], priority='H', tags=usrconfig.sawmTags)
    #[0:19] index for tasklib as it cannot process fractional seconds by way of the taskwarrior calc function
    sawm_task.save()