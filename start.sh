#!/bin/bash
#service rethinkdb restart

# Path of the script
DIR=$(dirname "$0")

# As deamon 
$DIR/myslice/bin/myslice-server &
#As deamon 
$DIR/myslice/bin/myslice-live &
#As deamon 
$DIR/myslice/bin/myslice-monitor &
#As deamon
$DIR/myslice/bin/myslice-web &
