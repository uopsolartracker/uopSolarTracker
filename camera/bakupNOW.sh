#!/bin/bash
clear
echo "Backups ALL files and folder from CURRENT location to /mnt/usb/"
 tar --exclude='*.png' --exclude='*.PNG' --exclude='*.jpg' --exclude='*.JPG' --exclude='*.tif' --exclude='*.TIF' --exclude='./OLD_*' \
     -zcvf /mnt/usb/zwoBackup-$(date +%Y.%m.%d-%H.%M.%S).tar ./

 tar -zcvf /mnt/usb/capture-$(date +%Y.%m.%d-%H.%M.%S).tar ./capture.cpp

echo ""
echo "Listing TAR files in backup location /mnt/usb/"
echo ""
ls -l /mnt/usb/*.tar
