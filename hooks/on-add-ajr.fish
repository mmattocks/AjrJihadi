#!/usr/bin/fish
read json
set parent (echo $json | jq '.parent // empty')
set desc (echo $json | jq -r '.description // empty')

if test -n "$parent"
    python3 ~/.task/hooks/ajrjihadi/add-ajr.py "$json"
else
    echo $json
end

exit 0