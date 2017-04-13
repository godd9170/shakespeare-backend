#!/bin/bash

SWAPFILE=/var/swapfile
SWAP_MEGABYTES=2048

if [ -f $SWAPFILE ]; then
	echo "Swapfile $SWAPFILE found, assuming already setup"
	/usr/bin/curl -X POST -d "place=insideif" http://requestb.in/pdl449pd
	exit;
fi

/usr/bin/curl -X POST -d "place=outsideif" http://requestb.in/pdl449pd

/bin/dd if=/dev/zero of=$SWAPFILE bs=1M count=$SWAP_MEGABYTES
/bin/chmod 600 $SWAPFILE
/sbin/mkswap $SWAPFILE
/sbin/swapon $SWAPFILE