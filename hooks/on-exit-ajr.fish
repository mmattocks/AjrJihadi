#!/usr/bin/fish
set sync false
for json in $argv
    set parent (echo $json | jq '.parent // empty')
    if test -n $parent
        sync=true
    end
end
if sync
    task sync
end

exit 0