#!/usr/bin/python 
import datetime
import time 
import MySQLdb

import sys
sys.path.append( '/home/hroest/')
sys.path.append( '/home/hroest/scripts/')
import create_flagged_data
import os

today = datetime.date.today()
now = datetime.datetime.now()
this_year = today.year
this_month = today.month
this_day = today.day


###########################################################################
logfile = open('/home/hroest/nightly.log', 'a')
logfile.write( '\nrun started:\n')
logfile.write( '\tstart time %s\n' % now)

os.system("sh /home/hroest/pywikipedia-folder/botpywikipedia/sichteroptin.sh")
now = datetime.datetime.now()
logfile.write( '\tfinished sichter: %s\n' % str(now) )

#we create the new data for this month
db = MySQLdb.connect(read_default_file="/home/hroest/.my.cnf")
create_flagged_data.create_data_monthly( db, this_year, this_month )
logfile.write( '\tupdated flagged files for %s%s\n' % (this_year, this_month) )

#do the stats for yesterday
create_flagged_data.create_data_daily( db, this_year, this_month, this_day -1 )
logfile.write( '\tupdated flagged files for %s%s%s\n' % (this_year, 
                                         this_month, this_day -1) )

latest_file = '/home/hroest/flagged_data/latest_actualisation' 
f = open(latest_file , 'w'); 
f.write( str( now ) + '\n'  ) 
f.close() 


#every new month we need to do the old month for good
if today.day < 3: 
    old_month = this_month -1 
    old_year = this_year
    if old_month == 0:
        old_month = 12
        old_year = this_year - 1
    create_flagged_data.create_data_monthly( db, old_year, old_month )
    logfile.write( '\tupdated flagged files for %s%s\n' % (old_year, old_month))

now = datetime.datetime.now()
logfile.write( '\tend time %s\n' % now)
logfile.close()
