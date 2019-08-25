import time
import sys
import json
import ajrSalat

#User ajrSalat params
salatWaitpad = 1.0 #waitpad hr before time is scheduled/calculated to begin/enter, begin displaying prayer task (TW wait:)
salatUntilpad = 24.0 #until pad hr after time is scheduled/calculated to end/exit, remove prayer task (TW until:)
coords = (43.6532,-79.3832,75.0) #lat/long/elev in m tuple
methodName = 'ISNA' #check ajrSalat.py for available calculation methods
asrMethodName = 'Hanafi' #'Standard' or 'Hanafi'

#User ajrSalat sawm/fast params
sawmWaitpad = 10.0 #display fasting tasks this many hours before sunrise
sawmUntilpad = 2.0 #delete fasting tasks this many hours after sunset

task = json.loads(sys.argv[1])
if task['description'] in ajrSalat.prayer_list:
    [wait, scheduled, due, until], descmod = ajrSalat.getSalatTime(task['description'],
                                                    task['due'],
                                                    coords,
                                                    ((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60),
                                                    asr=asrMethodName,
                                                    method=methodName,
                                                    dst=time.localtime().tm_isdst,
                                                    waitpad=salatWaitpad,
                                                    untilpad=salatUntilpad)

    task['wait'], task['scheduled'], task['due'], task['until'] = wait, scheduled, due, until

    if descmod != '': #if there's a modified description, assign it
        task['description'] = descmod
elif task['description'] in ['Sawm','Fast']:
    [wait, scheduled, due, until] = ajrSalat.getSawmTime(task['due'],
                                                    coords,
                                                    ((time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 60 / 60),
                                                    method=methodName,
                                                    dst=time.localtime().tm_isdst,
                                                    waitpad=sawmWaitpad,
                                                    untilpad=sawmUntilpad)  
    task['wait'], task['scheduled'], task['due'], task['until'] = wait, scheduled, due, until

print(json.dumps(task))
sys.exit(0)