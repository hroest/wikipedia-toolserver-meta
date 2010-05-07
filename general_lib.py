#!/usr/bin/python
# -*- coding: utf-8  -*-

pywiki_lock_location = '/home/hroest/locks/pywikilock'
import os.path
import datetime



def acquire_pywiki_lock():
    if os.path.isfile( pywiki_lock_location ): return False
    now = datetime.datetime.now()
    f = open( pywiki_lock_location, 'w')
    f.write( str(now ) )
    f.close()
    return True

def get_lock_value():
    if not os.path.isfile( pywiki_lock_location ): return False
    f = open( pywiki_lock_location, 'r')
    return f.read()

def release_pywiki_lock():
    if not os.path.isfile( pywiki_lock_location ): return False
    os.system( 'rm %s'  % pywiki_lock_location )
    return True

