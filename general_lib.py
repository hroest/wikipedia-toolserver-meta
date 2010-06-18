#!/usr/bin/python
# -*- coding: utf-8  -*-

pywiki_lock_location = '/home/hroest/locks/pywikilock'
import os.path
import datetime
import time


def acquire_pywiki_lock():
    if os.path.isfile( pywiki_lock_location ): return False
    now = datetime.datetime.now()
    now_unix = time.mktime( now.timetuple()  )  
    f = open( pywiki_lock_location, 'w')
    f.write( str(now_unix ) )
    f.close()
    return True

def get_lock_value():
    if not os.path.isfile( pywiki_lock_location ): return False
    f = open( pywiki_lock_location, 'r')
    return f.read()

def get_lock_age():
    if not os.path.isfile( pywiki_lock_location ): return False
    f = open( pywiki_lock_location, 'r')
    age = f.read()
    now = datetime.datetime.now()
    now_unix = time.mktime( now.timetuple()  )  
    return now_unix - int( float(age) )

def release_pywiki_lock():
    if not os.path.isfile( pywiki_lock_location ): return False
    os.system( 'rm %s'  % pywiki_lock_location )
    return True

def release_pywiki_lock_if_older_than(age=1800):
    if not os.path.isfile( pywiki_lock_location ): return False
    if get_lock_age() > age:
        os.system( 'rm %s'  % pywiki_lock_location )
        return True
    return False
