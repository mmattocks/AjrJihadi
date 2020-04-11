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

print(json.dumps(task))
sys.exit(0)