#!/bin/bash

#service rethinkdb restart

# Path of the script
DIR=$(dirname "$0")

# As deamon 
$DIR/myslice/bin/myslice-router.py &
$DIR/myslice/bin/myslice-server >> /var/log/myslice/server-stdout-stderr.log 2>1 &
# As deamon 
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

