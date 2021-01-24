#!/bin/bash
# print temp for i3 blocks
# reads output from sensors command

all_sensors=$(sensors | grep -E "Core [0-9]" | awk '{print $3}' \
    | cut -d'.' -f 1 | sed 's/+//g')

# build array
sensors_arr=()
while IFS= read -r line; do
    sensors_arr+=("$line")
done <<< "$all_sensors"

# calc average
cores="${#sensors_arr[@]}"
sum_cores=$(IFS=+; echo "$((${sensors_arr[*]}))")
temp=$(( sum_cores / cores ))

# split based on temp
if [[ $temp -le 60 ]]; then
    printmain="  $temp°C"
    printsmall=""
    printcolor=""
elif [[ $temp -gt 60 ]] && [[ $temp -lt 75 ]]; then
    printmain="  $temp°C"
    printsmall=""
    printcolor="#FFFF00"
elif [[ $temp -ge 75 ]]; then
    printmain="  $temp°C"
    printsmall=""
    printcolor="#FF0000"
else
    printcolor=""
fi

echo "$printmain"
echo "$printsmall"
echo "$printcolor"

##
exit 0
