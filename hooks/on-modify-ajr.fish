#!/usr/bin/fish
read --line json1 json2
set tstatus (echo $json1 | jq -r '.status // empty')
set desc (echo $json1 | jq -r '.description // empty')
if test $tstatus = 'recurring'
    and contains $desc $salat_names
    python3 ~/.task/hooks/ajrjihadi/modify-ajr.py "$json1" "$json2"
else
    echo $json2
end

exit 0