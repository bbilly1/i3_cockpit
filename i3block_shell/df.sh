#!/bin/bash
# run df on root partition for i3blocks

freemem=$(df -h  | grep '/$' | awk '{print $5}' | sed 's/%//g')

if [[ $freemem -lt 80 ]]; then
    printmain="$freemem"%
    printsmall="$freemem"%
    printcolor="#ffffff"
elif [[ $freemem -ge 80 ]] && [[ $freemem -le 90 ]]; then
    printmain="$freemem"%
    printsmall="$freemem"%
    printcolor="#ffff00"
elif [[ $freemem -gt 90 ]] && [[ $freemem -le 100 ]]; then
    printmain="$freemem"%
    printsmall="$freemem"%
    printcolor="#ff0000"
fi

case $BLOCK_BUTTON in
    1) notify-send "$(notify-send "disk free:" \
    "$(df -h | grep -v tmpfs | grep -v loop | grep -v udev | sort)")" ;;
esac

echo "$printmain"
echo "$printmain"
echo "$printcolor"

##
exit 0
