#!/usr/bin/fish
while read json
set tstatus (echo $json | jq -r '.status // empty')
set parent (echo $json | jq '.parent // empty')
if test -n "$parent"
	and test $tstatus = 'deleted'
		python3 ~/.task/hooks/ajrjihadi/missed-ajr.py
	echo 'Accounting for missed ajr..'
end

exit 0
