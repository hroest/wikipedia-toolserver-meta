#!/usr/bin/python 
# -*- coding: utf-8  -*-

import datetime
import time 
import MySQLdb
import os, sys

#print('I exit from quarter hourly!!!')
#sys.exit()

import sys
sys.path.append( '/home/hroest/')
sys.path.append( '/home/hroest/scripts/')
sys.path.append( '/data/project/hroest/meta' )
sys.path.append( '/data/project/hroest/bot/pywikibot-compat/' )
import create_flagged_data
import replag_lib
import general_lib
import flagged_lib

today = datetime.date.today()
now = datetime.datetime.now()
this_year = today.year
this_month = today.month
db = MySQLdb.connect(read_default_file=general_lib.mysql_config_file, host=general_lib.mysql_host)

###########################################################################
logfile = open('%s/logs/quarter-hourly.log' % general_lib.root, 'a')
logfile.write( '\nrun started:\n')
logfile.write( '\tstart time %s\n' % now)

## 1. Calculate current replication lag
replag_lib.insert_db(db, logfile)
logfile.write( '\tinserted row into db\n' )

## 2. Delete old picture and release older lock
os.system( 'touch %s/public_html/tmp/pics/tmp_mytmptmp' % general_lib.root)
os.system( 'rm %s/public_html/tmp/pics/tmp*' % general_lib.root)
logfile.write( '\tdeleted all pics like tmp/pics/tmp*\n' )
#get rid of a lock that is older than an hour
general_lib.release_pywiki_lock_if_older_than(3600)

## 3. Compute lagging users 
flagged_lib.create_lagging_user(db)
now = datetime.datetime.now()
logfile.write( '\tcreated lagging user table %s\n' % now )
now = datetime.datetime.now()
flagged_lib.create_never_reviewed(db)
logfile.write( '\tcreated unflagged pages table %s\n' % now )

## 4. Done
now = datetime.datetime.now()
logfile.write( '\tend time %s\n' % now)
logfile.close()

