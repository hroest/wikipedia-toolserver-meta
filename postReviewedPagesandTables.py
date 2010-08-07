#!/usr/bin/python 
# -*- coding: utf-8  -*-

import sys
sys.path.append( '/home/hroest' )
sys.path.append( '/home/hroest/pywikipedia-folder/botpywikipedia/')
import h_lib_api
import general_lib

f = open('/home/hroest/process-started.txt', 'w' ) 
f.write( 'started')
f.close()

f = open('/home/hroest/public_html/cgi-bin/reviewed.dat' ) 
user = f.read().strip()
f.close()
h_lib_api.postReviewedPagesandTable( user.decode('utf-8') )

#here we release the lock -- assuming that it has been acquired before!
general_lib.release_pywiki_lock()
