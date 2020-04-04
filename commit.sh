date

# Git: add and commit changes
cd /root/gravity_housekeeper && /usr/bin/git add --all && /usr/bin/git commit -m "cron push `date +%d-%B-%Y%t%H:%M:%S`"

# send data to Git server
cd /root/gravity_housekeeper && /usr/bin/git push origin master
