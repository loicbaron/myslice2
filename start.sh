#!/bin/bash
#service rethinkdb restart
#As deamon 
/root/myslice/myslice/bin/myslice-live &
#As deamon 
/root/myslice/myslice/bin/myslice-monitor &
# As deamon 
/root/myslice/myslice/bin/myslice-server &
#As deamon
/root/myslice/myslice/bin/myslice-web &
