#!/usr/bin/fish
while read json
	set parent (echo $json | jq '.parent // empty')
	if test -n "$parent"
		set tstatus (echo $json | jq -r '.status // empty')
		if test $tstatus = 'deleted'
			python3 ~/.task/hooks/ajrjihadi/missed-ajr.py $json
		end
	end
end

exit 0
