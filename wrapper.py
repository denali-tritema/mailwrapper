#!/usr/bin/python

import string
import email
import sys
import os
import time
import hashlib

"""
mail wrapper for php mail() function.
author: info@denali.london
"""

FILELOG="phpmailerlogger.log"
WORKDIR="/var/log/phpmailer/"
## default maximum email is 1000
MAXEMAIL=1000
EMAILPAUSE=3
MAILERTOWRAP = "/usr/sbin/sendmail -t -i"

try:
  emaillimit=int(sys.argv[1])
except:
  emaillimit=MAXEMAIL



## ------ functions start

def md5sum(s):
        return hashlib.md5(s).hexdigest()

def readcount(filetowrite):
        try:
                fp = open(WORKDIR + filetowrite, 'r')
                valore=fp.read()
                fp.close()
                valore= valore.strip()
        except:
                valore=1
        return int(valore)

def writecount(filetowrite,nuovo):
        nuovoval=str(nuovo)
        fp = open(WORKDIR + filetowrite, 'w')
        fp.write(nuovoval)
        fp.close()
        return nuovoval

def logger(miastringa):
        fp = open(WORKDIR + FILELOG, 'a')
        fp.write(miastringa+"\n")
        fp.close()

## ------ functions end

## get environment
thishost = os.environ.get('HOSTNAME')
mypwd = os.environ.get('PWD')
md5pwd = md5sum(mypwd)

## get data from incoming message
msg = email.message_from_file(sys.stdin)

if msg.get('From') != "":
  myfrom=msg.get('From')
else:
  myfrom=""

if msg.get('Subject') != "":
  mySubject=msg.get('Subject')
else:
  mySubject=""

if msg.get('To') != "":
  myto=msg.get('To')
else:
  myto=""

## convert message in string
mess = msg.as_string()

## read counter and increment
startval=readcount(md5pwd+".cnt")
endval=writecount(md5pwd+".cnt",startval+1)

if int(endval) == emaillimit:
        ## send alert email to supervisor
        allerta = "Counter=" + str(endval) + " BLOCKED" + "\nPwd=" + str(mypwd) + "\nCounter file=" + str(md5pwd) + "\nMessge From="+ str(myfrom) + "\nMessage to=" + str(myto) + "\nMessage subject=" + str(mySubject) + "\nMessage md5=" + str(md5sum( mess) )
        sendmail = os.system('echo "' + str(allerta) + '" | mail -s "phpmailer - Alert - ' + str(thishost) + '" tech@tritema.ch' )

if int(endval) <= emaillimit:
        ## let's send the mail
        time.sleep(EMAILPAUSE)
        p = os.popen (MAILERTOWRAP, "w")
        p.write(mess)
        exitcode = p.close()
        #LOGGER: contatore | pwd | md5pwd | from | to | oggetto | md5 messaggio
        logger ( str(endval) + "|"+"PASSED"+"|" + str(mypwd) + "|"+ str(md5pwd) + "|"+ str(myfrom) + "|"+ str(myto) + "|" + str(mySubject) + "|" + str(md5sum (mess)) )
else:
        ## dont send the email and log
        logger ( str(endval) + "|"+ "BLOCKED"+"|" + str(mypwd) + "|"+ str(md5pwd) + "|"+ str(myfrom) + "|"+ str(myto) + "|" + str(mySubject) + "|" + str(md5sum (mess)) )
        exit
