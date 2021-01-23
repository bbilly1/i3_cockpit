#!/bin/bash
# script for i3block pending updates

amount=$(wc -l $HOME/Dokumente/status/updates | awk '{print $1}')

if [[ $amount -eq 0 ]]; then
    printmain=""
    printsmall=""
    printcolor=""
fi

if [[ $amount -gt 0 ]] && [[ $amount -le 30 ]]; then
    printmain=" $amount"
    printsmall=""
    printcolor="#FFFFFF"
fi

if [[ $amount -gt 30 ]] && [[ $amount -le 100 ]]; then
    printmain=" $amount"
    printsmall=""
    printcolor="#FFFF00"
fi

if [[ $amount -gt 100 ]]; then
    printmain=" $amount"
    printsmall=""
    printcolor="#FF0000"
fi

case $BLOCK_BUTTON in
    1) notify-send "pending updates:" "$(cat ~/Dokumente/status/updates)" ;;
    3) notify-send "looking for updates..." && notify-send \
    "$($HOME/sync/system/arch/script/checkupd.sh)" ;;
esac

echo "$printmain"
echo "$printsmall"
echo "$printcolor"

##
exit 0
