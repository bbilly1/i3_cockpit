#!/bin/bash
# get wifi info for i3blocks

# get interface
interface=$(ip link show up | grep -vi 'loopback' \
    | head -n 1 | awk '{print $2}' | sed 's/://g')

# read db value for interface
db=$(cat /proc/net/wireless | grep "$interface" \
    | awk -F '.  ' '{print $3}')
if [[ -n "$db" ]]; then
    printmain="$db db"
    printsmall="$db db"
else
    printmain=""
    printsmall=""
fi

# switch color
if [[ $db -le 60 ]]; then
    printcolor="#00FF00"
elif [[ $db -le 80 ]] && [[ $db -gt 60 ]]; then
    printcolor="#FFFF00"
else
    printcolor="#FF0000"
fi

# sent nmcli status on click
case $BLOCK_BUTTON in
    1) notify-send "$(nmcli device status)";;
esac

# echo three lines
echo "$printmain"
echo "$printsmall"
echo "$printcolor"

##
exit 0
