#!/usr/bin/fish
read json
set parent (echo $json | jq '.parent // empty')
set desc (echo $json | jq -r '.description // empty')

if test -n "$parent"
    and contains $desc $salat_names
    python3 ~/.task/hooks/ajrjihadi/add-ajr.py "$json"
else if contains $desc 'Fast' 'Sawm'
    python3 ~/.task/hooks/ajrjihadi/add-ajr.py "$json"
else
    echo $json
end

exit 0