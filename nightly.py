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
logfile = open('/home/hroest/nightly.log', 'a')
logfile.write( '\nrun started:\n')
logfile.write( '\tstart time %s\n' % now)

#we create the new data for this month
db = MySQLdb.connect(read_default_file="/home/hroest/.my.cnf")
create_flagged_data.create_data( db, this_year, this_month )
logfile.write( '\tupdated files for %s%s\n' % (this_year, this_month) )

#every new month we need to do the old month for good
if today.day < 3: 
    old_month = this_month -1 
    old_year = this_year
    if old_month == 0:
        old_month = 12
        old_year = this_year - 1
    create_flagged_data.create_data( db, old_year, old_month )
    logfile.write( '\tupdated files for %s%s\n' % (old_year, old_month) )

logfile.write( '\tend time %s\n' % now)
logfile.close()
