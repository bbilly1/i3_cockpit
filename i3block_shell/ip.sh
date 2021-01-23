#!/bin/bash
# status bar ip lookup

# when offline
if [[ $(ip a | grep "state" | grep -Ev 'tun|lo' | grep "DOWN ") ]]; then
    printmain="down"
    printsmall="down"
    printcolor="#FF0000"
fi

# when connected
if [[ $(ip a | grep "state" | grep -Ev 'tun|lo' | grep "UP ") ]]; then
    printmain=$(ip -br addr show | grep -v 'lo' \
        | awk '{print $3}' | awk -F '/' {'print $1}' | tr '\n' ' ')
    printsmall=$(ip -br addr show | grep -v 'lo' \
        | awk '{print $3}' | awk -F '/' {'print $1}' | head -n 1)
    printcolor="#00FF00"
fi

# echo
echo "$printmain"
echo "$printsmall"
echo "$printcolor"

##
exit 0
