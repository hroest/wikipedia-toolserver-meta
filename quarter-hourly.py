#!/usr/bin/python 
import datetime
import time 
import MySQLdb

import sys
sys.path.append( '/home/hroest/')
sys.path.append( '/home/hroest/scripts/')
import create_flagged_data

today = datetime.date.today()
now = datetime.datetime.now()
this_year = today.year
this_month = today.month

###########################################################################
logfile = open('/home/hroest/quarter-hourly.log', 'a')
logfile.write( '\nrun started:\n')
logfile.write( '\tstart time %s\n' % now)



now = datetime.datetime.now()
logfile.write( '\tend time %s\n' % now)
logfile.close()
