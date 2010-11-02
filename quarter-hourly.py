#!/usr/bin/python 
import datetime
import time 
import MySQLdb
import os, sys

#print('I exit from quarter hourly!!!')
#sys.exit()

import sys
sys.path.append( '/home/hroest/')
sys.path.append( '/home/hroest/scripts/')
import create_flagged_data
import replag_lib
import general_lib
import flagged_lib

today = datetime.date.today()
now = datetime.datetime.now()
this_year = today.year
this_month = today.month

db = MySQLdb.connect(read_default_file="/home/hroest/.my.cnf")

###########################################################################
logfile = open('/home/hroest/quarter-hourly.log', 'a')
logfile.write( '\nrun started:\n')
logfile.write( '\tstart time %s\n' % now)

replag_lib.insert_db( db )
logfile.write( '\tinserted row into db\n' )

os.system( 'touch /home/hroest/public_html/tmp/pics/tmp_mytmptmp')
os.system( 'rm /home/hroest/public_html/tmp/pics/tmp*')
logfile.write( '\tdeleted all pics like tmp/pics/tmp*\n' )
#get rid of a lock that is older than an hour
general_lib.release_pywiki_lock_if_older_than(3600)

flagged_lib.create_lagging_user(db);
logfile.write( '\tcreated lagging user table\n' )

now = datetime.datetime.now()
logfile.write( '\tend time %s\n' % now)
logfile.close()
