from datetime import datetime, timedelta
import math
import re
import usrconfig

#------------------------ Constant handling --------------------------
def assembleParams(method, asrMethod):
    m_params = usrconfig.methods[method]['params']
    params = [10.0, m_params['fajr'], 0.0, 0.0, asrMethod, m_params['maghrib'], m_params['isha'], 0.0, m_params['midnight']]
    return params

#-------------------- Interface Functions --------------------
def getSalatTime(prayer, ISOdatetime, coords, timezone, method='MWL', asr='Standard', dst=0, waitpad=1.0, untilpad=24.0):
    lat = coords[0]
    lng = coords[1]
    elv = coords[2] if len(coords) > 2 else 0
    curr_dt = tw_ISO8601_to_local_dt(ISOdatetime,timezone)
    date = (curr_dt.year, curr_dt.month, curr_dt.day)
    timeZone = timezone + (1.0 if dst else 0.0)
    jDate = julian(date[0], date[1], date[2]) - lng / (15 * 24.0)
    params = assembleParams(method, asr)
    modified_desc = ''
    if prayer == 'Dhuhr' and curr_dt.isoweekday() == 5: #if it's friday and the prayertime is dhuhr
        modified_desc = 'Jumuah'
    wait, scheduled, due, until = computeTime(prayer, params, jDate, lat, lng, elv, timeZone, waitpad, untilpad)
    return dateTimeFormat(date, [wait, scheduled, due, until]), modified_desc

def getSawmTime(dt, coords, timezone, method='MWL', dst=0, waitpad=10.0, untilpad=1.0):
    lat = coords[0]
    lng = coords[1]
    elv = coords[2] if len(coords) > 2 else 0
    date = (dt.year, dt.month, dt.day)
    timeZone = timezone + (1.0 if dst else 0.0)
    jDate = julian(date[0], date[1], date[2]) - lng / (15 * 24.0)
    params = assembleParams(method, 'Standard')
    wait, scheduled, d, u = computeTime('Fajr', params, jDate, lat, lng, elv, timeZone, waitpad, untilpad)
    w, s, due, until = computeTime('Asr', params, jDate, lat, lng, elv, timeZone, waitpad, untilpad)
    return dateTimeFormat(date, [wait, scheduled, due, until])

# FORMATTING FUNCTIONS

def tw_ISO8601_to_local_dt(dt,tz):  #TW formatted JSON ISO 8601 zulu datetime string to local datetime object
    return datetime.strptime(dt,"%Y%m%dT%H%M%S%z") + timedelta(hours=tz)

def dateTimeFormat(date, times):
    day_start = datetime(date[0],date[1],date[2])
    dts = []
    for time in times:
        delta = timedelta(hours=time)
        dt = day_start + delta
        dts.append(dt.isoformat())
    return dts

#---------------------- Calculation Functions -----------------------
def computeTime(prayer, params, jDate, lat, lng, elv, timeZone, waitpad, untilpad):
    times = {
        'imsak': 5, 'fajr': 5, 'sunrise': 6, 'dhuhr': 12,
        'asr': 13, 'sunset': 18, 'maghrib': 18, 'isha': 18
    }
    times = dayPortion(times)
    scheduled,due = 0,0
    if prayer == 'Fajr':
        scheduled = sunAngleTime(lat, jDate, params[1], times['fajr'], "CCW") + (timeZone - lng/ 15)#fajr
        due = sunAngleTime(lat, jDate, riseSetAngle(elv),times['sunrise'], "CCW") + (timeZone - lng/ 15) #sunrise
    elif prayer == 'Dhuhr': 
        scheduled = midDay(jDate, times['dhuhr']) + (timeZone - lng/ 15)
        scheduled = scheduled + (params[3] / 60)  #dhuhr
        due = asrTime(params[4], lat, jDate, times['asr']) + (timeZone - lng/ 15) #asr
    elif prayer == "Asr":
        scheduled = asrTime(params[4], lat, jDate, times['asr']) + (timeZone - lng/ 15) #asr
        due = sunAngleTime(lat, jDate, riseSetAngle(elv), times['sunset'],"CW") + (timeZone - lng/ 15) #sunset
    elif prayer == "Maghrib":
        scheduled = sunAngleTime(lat, jDate, riseSetAngle(elv), times['maghrib'],"CW") + (timeZone - lng/ 15) 
        scheduled = scheduled + params[5] / 60.0 #maghrib
        due = sunAngleTime(lat, jDate, params[6], times['isha'],"CW") + (timeZone - lng/ 15) #isha
    elif prayer == "Isha":
        scheduled = sunAngleTime(lat, jDate, params[6], times['isha'],"CW") + (timeZone - lng/ 15) #isha
        due = sunAngleTime(lat, jDate+1, params[1], times['fajr'], "CCW") + (timeZone - lng/ 15) + 24 #next day fajr
    else:
        raise ValueError('Unrecognised prayer string!')
    wait = scheduled - waitpad
    until = due + untilpad
    
    return wait, scheduled, due, until

# compute mid-day time
def midDay(jDate, time):
    eqt = sunPosition(jDate + time)[1]
    return fixhour(12 - eqt)

# compute the time at which sun reaches a specific angle below horizon
def sunAngleTime(lat, jDate, angle, time, direction=None):
    try:
        decl = sunPosition(jDate + time)[0]
        noon = midDay(jDate, time)
        t = 1 / 15.0 * arccos((-sin(angle) - sin(decl) * sin(lat)) /
                                    (cos(decl) * cos(lat)))
        return noon + (-t if direction == 'CCW' else t)
    except ValueError:
        return float('nan')

# compute asr time
def asrTime(method, lat, jDate, time):
    factor = 1
    if method == 'Hanafi':
        factor = 2
    decl = sunPosition(jDate + time)[0]
    angle = -arccot(factor + tan(abs(lat - decl)))
    return sunAngleTime(lat, jDate, angle, time, 'CW')

# compute declination angle of sun and equation of time
# Ref: http://aa.usno.navy.mil/faq/docs/SunApprox.php
def sunPosition(jd):
    D = jd - 2451545.0
    g = fixangle(357.529 + 0.98560028 * D)
    q = fixangle(280.459 + 0.98564736 * D)
    L = fixangle(q + 1.915 * sin(g) + 0.020 * sin(2 * g))
    R = 1.00014 - 0.01671 * cos(g) - 0.00014 * cos(2 * g)
    e = 23.439 - 0.00000036 * D
    RA = arctan2(cos(e) * sin(L), cos(L)) / 15.0
    eqt = q / 15.0 - fixhour(RA)
    decl = arcsin(sin(e) * sin(L))
    return (decl, eqt)

# convert Gregorian date to Julian day
# Ref: Astronomical Algorithms by Jean Meeus
def julian(year, month, day):
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5

# return sun angle for sunset/sunrise
def riseSetAngle(elevation=0):
    elevation = 0 if elevation == None else elevation
    return 0.833 + 0.0347 * math.sqrt(elevation) # an approximation

# adjust a time for higher latitudes
def adjustHLTime(time, base, angle, night, method, direction=None):
    portion = nightPortion(angle, night, method)
    diff = timeDiff(time, base) if direction == 'ccw' else timeDiff(base, time)
    if math.isnan(time) or diff > portion:
        time = base + (-portion if direction == 'ccw' else portion)
    return time

# the night portion used for adjusting times in higher latitudes
def nightPortion(angle, night, method):
    portion = 1 / 2.0  # midnight
    if method == 'AngleBased':
        portion = 1 / 60.0 * angle
    if method == 'OneSeventh':
        portion = 1 / 7.0
    return portion * night

# convert hours to day portions
def dayPortion(times):
    for i in times:
        times[i] /= 24.0
    return times

#---------------------- Misc Functions -----------------------
# compute the difference between two times
def timeDiff(time1, time2):
    return fixhour(time2 - time1)

# convert given string into a number
def eval(st):
    val = re.split('[^0-9.+-]', str(st), 1)[0]
    return float(val) if val else 0

# detect if input contains 'min'
def isMin(arg):
    return isinstance(arg, str) and arg.find('min') > -1

#----------------- Degree-Based Math Functions -------------------
def sin(d): return math.sin(math.radians(d))

def cos(d): return math.cos(math.radians(d))

def tan(d): return math.tan(math.radians(d))

def arcsin(x): return math.degrees(math.asin(x))

def arccos(x): return math.degrees(math.acos(x))

def arctan(x): return math.degrees(math.atan(x))

def arccot(x): return math.degrees(math.atan(1.0 / x))

def arctan2(y, x): return math.degrees(math.atan2(y, x))

def fixangle(angle): return fix(angle, 360.0)

def fixhour(hour): return fix(hour, 24.0)

def fix(a, mode):
    if math.isnan(a):
        return a
    a = a - mode * (math.floor(a / mode))
    return a + mode if a < 0 else a

'''
Code modified (de-OOPed and reduced to specific prayers) for AjrJihadi from the corrected gist of Khabib Murtuzaaliev(skeeph). May God give all those mentioned in this comment Jannat al Firdaus

ORIGINAL CODE COPYRIGHT:

--------------------- Copyright Block ----------------------

praytimes.py: Prayer Times Calculator (ver 2.3)
Copyright (C) 2007-2011 PrayTimes.org

Python Code: Saleem Shafi, Hamid Zarrabi-Zadeh
Original js Code: Hamid Zarrabi-Zadeh

License: GNU LGPL v3.0

TERMS OF USE:
Permission is granted to use this code, with or
without modification, in any website or application
provided that credit is given to the original work
with a link back to PrayTimes.org.

This program is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY.

PLEASE DO NOT REMOVE THIS COPYRIGHT BLOCK.
'''