#!/usr/bin/env python

import getopt,sys,time,socket,os
from subprocess import *

def updateLastRun(file):
        fp = open(file,"w")
        now = int(time.time())
        fp.write("%s" % now)
        fp.close()
        return(now)

def time_delta_check(timediff, fle):
        oldtime = 0
        try:
                fp = open(fle,"r")
                line=fp.readline()
                oldtime = float(line)
                fp.close()
        except IOError:
                if _verbose > 1:
                        print ("[ERROR] IOerror: %s may not exist." % (fle))
                        print ("[INFO] File %s will be created" % (fle))
        except ValueError:
                if _verbose > 1:
                        print ("[ERROR] ValueError: \"%s\" is not a valid timestamp." % (line))
                        print ("[INFO] Please check the contents of %s or delete the file" % (fle))
        except:
                if _verbose > 1:
                        print ("[ERROR] Some error occured while reading timestamp from file.")
        now = int(time.time())
        
        if oldtime > 0:
                timeTillAction = (int(oldtime) + timediff) - now
                if _verbose > 0: print ("[INFO] lastbackup was on %s, next valid time would be in %s seconds." % (time.ctime(oldtime),timeTillAction))
        else:
                timeTillAction = 0
                if _verbose > 0:
                        print ("[INFO] Last run is unknown, executing command now if other requirements are met.")

        return(timeTillAction)

def service_connect_check(host, port):
        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
                if _verbose > 2:print("[ERROR] Socketerror" % ())
                return(False)
 
        try:
                sock.connect((host, port))
        except socket.error:
                if _verbose > 2: print("[ERROR] Socketerror" )
                return(False)

        if _verbose > 0: print ("[INFO] connection to port %s on host %s is established." % (port,host))
        return(True)
 
                        
def usage():
        print ("RTFS: Read the fukcin source!")
        sys.exit(0)

def main(argv):
        file="./lastrun.log"
        global _verbose
        _verbose = 0
        timediff = 0
        time_check = False
        service_check = False
        service_port = 22
        ping_check = False
        ping_host = ''
        command = 'echo "dry run! Use -x or --execute to execute a command!"'
        
        try:
                optlist, list = getopt.getopt(argv, "hf:D:H:M:v:s:p:x:", \
                        ["help","file=","days=","hours=","minutes=","verbose=","service=","port=","execute="])

        except (getopt.GetoptError, err):
                print (str(err))
                usage()
                sys.exit(2)
        for opt in optlist:
                if opt[0] in ("-h", "--help"):
                        usage()
                elif opt[0] in ("-v", "--verbose"):
                        _verbose = _verbose + 1
                elif opt[0] in ("-f", "--file"):
                        file = opt[1]
                elif opt[0] in ("-M", "--minutes"):
                        minutes = opt[1]
                        timediff = timediff + (int(minutes) * 60)
                        time_check = True
                elif opt[0] in ("-H", "--hours"):
                        hours = opt[1]
                        timediff = timediff + (int(hours) * 3600)
                        time_check = True
                elif opt[0] in ("-D", "--days"):
                        days = opt[1]
                        timediff = timediff + (int(days) * 24 * 3600)
                        time_check = True
                elif opt[0] in ("-s","--service"):
                        service_host = opt[1]
                        service_check = True
                elif opt[0] in ("-p","--port"):
                        service_host = opt[1]
                elif opt[0] in ("-x", "--execute"):
                        command = opt[1]

        if time_check:
                timeTillAction = time_delta_check(timediff, file)
                if (time_check and timeTillAction > 0):
                        if _verbose > 0: print ("[INFO] Not running: %s more seconds to wait." % timeTillAction)
                        exit(1)


        if service_check:
                service_online = service_connect_check(service_host, service_port)
                if (service_check and not service_online):
                        if _verbose > 0: print ("[INFO] Not running: Service %s on port %s not online." % (service_host,service_port))
                        exit(1)
        
        if _verbose > 0: print ("[INFO] Executing '%s'" % command)
        p = Popen(command, shell=True)
        sts = os.waitpid(p.pid, 0)

        # last thing to do is put timestamp in $file
        updateLastRun(file)
         
if __name__ == "__main__":
        main(sys.argv[1:])
        
