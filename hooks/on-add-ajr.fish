#!/usr/bin/fish
read json
set parent (echo $json | jq '.parent // empty')
if test -n $parent
    python3 ~/.task/hooks/ajrjihadi/add-ajr.py "$json"
    task sync
else
    echo $json
else
    python3 ~/.task/hooks/ajrjihadi/add-ajr.py "$json"
end

exit 0