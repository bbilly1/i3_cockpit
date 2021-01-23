#!/bin/bash
# print out the date for i3blocks

printmain=$(date '+%a, %d.%m.%Y')
printsmall=$(date '+%d.%m.%Y')
printcolor="#ffffff"

case $BLOCK_BUTTON in
    1) notify-send "today: $(date)" "$(cal -3)" ;;
esac

echo "$printmain"
echo "$printsmall"
echo "$printcolor"

##
exit 0
