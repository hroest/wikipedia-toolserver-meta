#!/usr/bin/python 
#$ -N hroest_nightly
#$ -l sqlprocs-s1=1

#command to submit:
#qsub -l sqlprocs-s2=1 nightly.py 


import datetime
import time 
import MySQLdb
import os

import sys
sys.path.append( '/home/hroest/')
sys.path.append( '/home/hroest/scripts/')
import create_flagged_data
import general_lib

today = datetime.date.today()
now = datetime.datetime.now()
this_year = today.year
this_month = today.month
this_day = today.day


###########################################################################
logfile = open('/home/hroest/nightly.log', 'a')
logfile.write( '\nrun started:\n')
logfile.write( '\tstart time %s\n' % now)

got_lock = general_lib.acquire_pywiki_lock()
os.system("sh /home/hroest/pywikipedia-folder/botpywikipedia/sichteroptin.sh")
now = datetime.datetime.now()
logfile.write( '\tfinished sichter: %s with lock %s\n' % (str(now), got_lock) )
if got_lock: general_lib.release_pywiki_lock()

#we create the new data for this month
db = MySQLdb.connect(read_default_file="/home/hroest/.my.cnf")
create_flagged_data.create_data_monthly( db, this_year, this_month )
logfile.write( '\tupdated flagged files for %s%s\n' % (this_year, this_month) )

#do the stats for yesterday
#create_flagged_data.create_data_daily( db, this_year, this_month, this_day -1 )
#logfile.write( '\tupdated flagged files for %s%s%s\n' % (this_year, 
#                                         this_month, this_day -1) )

latest_file = '/home/hroest/flagged_data/latest_actualisation' 
f = open(latest_file , 'w'); 
f.write( str( now ) + '\n'  ) 
f.close() 

#every new month we need to do the old month for good
if today.day < 3: 
#if True:
    old_month = this_month -1 
    old_year = this_year
    if old_month == 0:
        old_month = 12
        old_year = this_year - 1
    create_flagged_data.create_data_monthly( db, old_year, old_month )
    logfile.write( '\tupdated flagged files for %s%s\n' % (old_year, old_month))
    #Person is too big
    cats = ['Schweiz', 'Chemie', 'Musik', 'Informatik', 'Religion', ] 
    for cat in cats:
        create_flagged_data.create_cat_tables( db, cat)
        logfile.write( '\tcategory done for %s\n' % cat)
        try: create_flagged_data.create_data_monthly_cat( db, old_year, old_month, cat)
        except Exception:
            logfile.write( '\tAborted: \n' % (cat))
            print '\tAborted: \n' % cat
    logfile.write( '\tupdated flagged files for Schweiz %s%s\n' % (old_year, old_month))
    create_flagged_data.create_data_all_year(db, old_year, slow_ok = True)
    create_flagged_data.create_data_all_time(db, slow_ok = True)
    logfile.write( '\tupdated flagged files all time and year %s\n' % (old_year))

now = datetime.datetime.now()
logfile.write( '\tend time %s\n' % now)
logfile.close()

