Interval Online.py
=================


Problem: I wanted to do rsync backups to a remote server from my laptop. my laptop ain't always online so cron ain't an option.
I've developed a simple python script that runs command X when:
1. atleast N time has passed by since last run
2. an internet connection is available to $HOST

The result is interval\_online.v01.py.

iPhone:~/files mobile$ ./test.py -M 1 --service=idefense.nl -vv -x 'rsync -ave ssh ~/files/ xychix@idefense.nl:~/iphone/' 
[INFO] lastbackup was on Mon May 25 21:33:03 2009, next valid time would be in -1 seconds.
[INFO] connection to port 22 on host idefense.nl is establishedi.
[INFO] Executing 'rsync -ave ssh ~/files/ xychix@idefense.nl:~/iphone/'
Enter passphrase for key '/var/mobile/.ssh/id_rsa': 
building file list ... done
lastrun.log

sent 228 bytes  received 48 bytes  61.33 bytes/sec
total size is 205172  speedup is 743.38
iPhone:~/files mobile$ 

YES it also run's on the iphone

For normal users
crontab:

*/10 * * * * /home/xychix/bin/interval_online.v01.py -H 8 --service=backup.server.nl -x /home/xychix/bin/rsync_remote.sh -f /home/xychix/bin/lastrun.log

rsync_remote.sh:

/bin/date > /Users/xychix/Documents/live/date.txt
rsync -ax --delete -e 'ssh -i /home/xychix/.ssh/id_rsa_nopasswd' ~/Documents/live backupuser@backup.server.nl:/home/backupuser/backup/test/Documents/
#rsync -ax --delete -e 'ssh -i /Users/xychix/.ssh/id_rsa_nopasswd' backupuser@backup.server.nl:/home/backupuser/backup/test/Documents/ ~/Documents/

TODO:
- write a usage function
- implement a timeout on the service connection function
- test filehandling with corrupted / unreadable / protected files

