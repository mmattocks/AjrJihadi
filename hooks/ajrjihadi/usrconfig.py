#User ajrJihadi params
#Handled prayer strings
prayer_list=['Maghrib', 'Isha', 'Fajr', 'Dhuhr', 'Asr']
#Prayer calculation setup
coords = (43.6532,-79.3832,75.0) #lat/long/(elev in m) tuple
methodName = 'ISNA' #check ajrSalat.py for available calculation methods
asrMethodName = 'Hanafi' #'Standard' or 'Hanafi'

#Task display timing setup
salatWaitpad = 1.0 #waitpad hr before time is scheduled/calculated to begin/enter, begin displaying prayer task (TW wait:)
salatUntilpad = 24.0 #untilpad hr after time is scheduled/calculated to end/exit, remove prayer task (TW until:)
#User ajrSalat sawm/fast params
sawmDesc = "Fast"
sawmProject = "Din.Sawm"
sawmTags = ["next", "@home", "@out", "@computer"]
sawmWaitpad = 10.0 #display fasting tasks this many hours before sunrise
sawmUntilpad = 4.0 #delete fasting tasks this many hours after sunset

#Missed prayer setup
track_missed=True
missed_start=1500 #the number of missed prayers to begin with

# Calculation Methods
methods = {
    'MWL': {
        'name': 'Muslim World League',
        'params': {'fajr': 18, 'isha': 17, 'maghrib': 0.0, 'midnight': 'Standard'}},
    'ISNA': {
        'name': 'Islamic Society of North America (ISNA)',
        'params': {'fajr': 15, 'isha': 15, 'maghrib': 0.0, 'midnight': 'Standard'}},
    'Egypt': {
        'name': 'Egyptian General Authority of Survey',
        'params': {'fajr': 19.5, 'isha': 17.5, 'maghrib': 0.0, 'midnight': 'Standard'}},
    'Makkah': {
        'name': 'Umm Al-Qura University, Makkah',
        'params': {'fajr': 18.5, 'isha': '90 min', 'maghrib': 0.0, 'midnight': 'Standard'}}, # fajr was 19 degrees before 1430 hijri
    'Karachi': {
        'name': 'University of Islamic Sciences, Karachi',
        'params': {'fajr': 18, 'isha': 18, 'maghrib': 0.0, 'midnight': 'Standard'}},
    'Tehran': {
        'name': 'Institute of Geophysics, University of Tehran',
        'params': {'fajr': 17.7, 'isha': 14, 'maghrib': 4.5, 'midnight': 'Jafari'}},
    # isha is not explicitly specified in this method
    'Jafari': {
        'name': 'Shia Ithna-Ashari, Leva Institute, Qum',
        'params': {'fajr': 16, 'isha': 14, 'maghrib': 4, 'midnight': 'Jafari'}}
}

#"until" timedeltas in days- wait this long after due to cull children of non-salat recurring tasks of the given recur periods, if enabled
recur_cull = True
until_tds={'daily':1,'weekly':2,'biweekly':4,'monthly':7,'bimonthly':14,'quarterly':28,'yearly':60}