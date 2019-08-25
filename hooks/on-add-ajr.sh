json=$(cat)
if [ "null" = "$(echo $json | jq .parent)" ]
then
    echo $json
else
    python ~/.task/hooks/ajrjihadi/add-ajr.py "$json"
fi

exit 0