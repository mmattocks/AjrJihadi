[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

# AjrJihadi 0.2
Muslim prayer and fasting time calculation, missed prayer tracking, etc. for TaskWarrior

Depends on:
fish shell
jq (command line json tool)
functioning python3 environment
tasklib

Installation: 
1. copy or link contents of /hooks to ~/.task/hooks on the primary machine (if more than one are to be used)
2. copy or link fast.fish, makeup.fish, missed.fish to ~/.config/fish/functions as desired
3. configure your prayer time calculation settings and other options in !.task/hooks/ajrjihadi/usrconfig.py
4. if multiple clients are to be used with a taskserver, set recurrence=no in all client .taskrc to prevent the generation of duplicate tasks

Usage:
1. create recurring tasks for prayers you wish to track, eg:

task add +next project:Din.Salat recur:daily due:eod Fajr

child tasks of this recurring task will be:
a. waiting until the time of prayer entry minus a usrconfig.py-specified time delta (ie one can choose how long before the time of prayer the task should appear in lists)
b. scheduled at the start time of that prayer
c. due at the end time of that prayer
d. persistent until the end time of the prayer plus a usrconfig.py-specified time delta (ie one can choose how long after the time of prayer has exited to delete the task if not )

2. if track_missed = True in usrconfig.py, the recurring task parent will be annotated with a string "MISSED: X" either upon the first missed (deleted) prayer, or upon executing missed.fish to check how many prayers have been missed. The initial value may set in usrconfig.py. Additional missed prayers will increment the number in the MISSED annotation, enabling persistent tracking of missed prayers

3. decrement MISSED prayer counts with makeup.fish
eg. 'makeup Fajr' to decrement missed Fajr prayers by 1, 'makeup Dhuhr 10' to record 10 Dhuhr makeups

4. to create fasting tasks with appropriately calculated times, use fast.fish, supplied with one YYYY-MM-DD date for a single fasting date, a single comma separated list of such dates, or two dates separated by a space for a range of dates (eg. Ramadan)

Todo:
1. remove vestigial values from calculation parameters array and refactor
2. bash-compatible script equivalents
3. implement high-latitudes prayer time calculation functions
4. add hijri date calculation for autopopulation of holidays and fasts