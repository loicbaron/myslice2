#!/bin/bash

#service rethinkdb restart

# Path of the script
DIR=$(dirname "$0")

# As deamon 
$DIR/myslice/bin/myslice-server &

ps -aux | grep 'myslice'

echo 'netstat -apn'
netstat -apn
echo 'sleep 20s'
sleep 20

echo 'netstat -apn' 
netstat -apn
echo 'sleep 20s'
sleep 20

echo 'netstat -apn' 
netstat -apn

