#!/usr/bin/fish
read json
set parent (echo $json | jq '.parent // empty')
if test -n "$parent"
    python3 ~/.task/hooks/ajrjihadi/add-ajr.py "$json"
else
    echo $json
end

exit 0