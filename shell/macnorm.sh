#!/usr/bin/env sh
 
mac="$1"
len="${#mac}"

#check to see if input is empty also if the input is less than 17 (mac.lenght + \n) it's ok

if ! [[ -n "$mac" || "$len" -gt "17" ]]
    then
        echo "Please enter a MAC address."
        exit
else 
    # echo the input, strip out dot(.), strip out colon(:), strip out dash(-)
    # add colon(:) every two chars, remove last colon(:)
    # awk to lowercase characters [EDIT: updated the sed for . seps and escape]
    echo $mac | sed -e 's/\.//g' -e 's/\://g' -e 's/\-//g' -e 's/../&:/g' -e 's/:$//g' \
| awk '{print tolower($0)}'
fi
