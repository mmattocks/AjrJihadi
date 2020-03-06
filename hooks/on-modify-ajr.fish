#!/usr/bin/fish
read --line json1 json2
set parent (echo $json2 | jq '.parent // empty')
if test -n "$parent"
    python3 ~/.task/hooks/ajrjihadi/modify-ajr.py "$json2"
else
    echo $json2
end

exit 0
