#!/bin/bash

touch /var/log/myslice/myslice-web.log

## How to start the script and redirect stdout to logfile
# ./start.sh > /var/log/myslice/myslice-web.log

#service rethinkdb restart

# Path of the script
DIR=$(dirname "$0")

# As deamon 
$DIR/myslice/bin/myslice-server &
#As deamon
$DIR/myslice/bin/myslice-web &
#As deamon 
$DIR/myslice/bin/myslice-live &
#As deamon 
$DIR/myslice/bin/myslice-monitor &

ps -aux | grep 'myslice'

echo 'netstat -apn'
netstat -apn
echo 'sleep 30s'
sleep 30

echo 'netstat -apn' 
netstat -apn
echo 'sleep 30s'
sleep 30

echo 'netstat -apn' 
netstat -apn

