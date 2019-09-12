#!/usr/bin/fish
read --line json1 json2
set parent (echo $json1 | jq '.parent // empty')
if [ "" = "$parent" ]
    echo $json2
else
    python3 ~/.task/hooks/ajrjihadi/modify-ajr.py "$json1" "$json2"
end

exit 0
