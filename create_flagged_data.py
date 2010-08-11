"""
This module allows to create statistical data about flagged revisions.

It will store all data in the specified path. The data can be separated by 
month and day (total) or by month (catogory-wise). It will produce a tab
separated file with number of active revisions (not passive ones that you get
by changing an article and the user id over the specified time periond and
articles).

create_data_daily           Daily revision data for all articles  
create_data_monthly         Monthly revision data for all articles 
create_data_monthly_cat     Monthly revision data for all articles in category 
                            tree. It needs a table pages_catname which contains
                            the ids of all pages in question. This table can be 
                            generated using create_cat_tables

Variables:
    path  -- where to store the files
    slow_ok_text -- text to put into the query when slow queries are allowed
"""
import db_api

#import MySQLdb, create_flagged_data
#db = MySQLdb.connect(read_default_file="/home/hroest/.my.cnf")
##create_flagged_data.create_cat_tables( db, 'Chemie' )
#create_flagged_data.create_data_monthly_cat( db, 2010, 5, 'Chemie' )

path = '/home/hroest/flagged_data/'
slow_ok_text = { True : " /* SLOW_OK */ " , False : "" }

def create_data_daily(db, year, month, day, slow_ok = True):
    """Creates the files with the per-month data in it. """

    query = \
    """
    select count(*),fr_user from dewiki_p.flaggedrevs 
    where 
    fr_flags = 'dynamic'
    and fr_timestamp like '%s%02d%02d%%'
    group by fr_user
    order by count(*)
    %s
    """ % (year, month, day, slow_ok_text[slow_ok] )

    myfile = path + 'all_month_day%s%02d%02d'% (year, month, day )
    f = open(myfile + '_tmp', 'w')
    print "writing into " , f.name
    cursor = db.cursor()
    cursor.execute( query )
    rows = cursor.fetchall()
    f.write( 'count(*)\tfr_user\n' )
    for r in rows:
        f.write( '%s\t%s\n' % (r[0], r[1]) )
    f.close()

    #after closing we move the tmp file to the real location
    import os
    print 'moving now'
    cmd  = 'mv %s %s' % (myfile + '_tmp', myfile )
    print cmd
    os.system( cmd )

def create_data_monthly(db, year, month, slow_ok = True):
    """Creates the files with the per-month data in it. """

    query = \
    """
    select count(*),fr_user from dewiki_p.flaggedrevs 
    where 
    fr_flags = 'dynamic'
    and fr_timestamp like '%s%02d%%'
    group by fr_user
    order by count(*)
    %s
    """ % (year, month, slow_ok_text[slow_ok])

    myfile = path + 'all_month_users_%s%02d'% (year, month )
    f = open(myfile + '_tmp', 'w')
    print "writing into " , f.name
    cursor = db.cursor()
    cursor.execute( query )
    rows = cursor.fetchall()
    f.write( 'count(*)\tfr_user\n' )
    for r in rows:
        f.write( '%s\t%s\n' % (r[0], r[1]) )
    f.close()

    #after closing we move the tmp file to the real location
    import os
    print 'moving now'
    cmd  = 'mv %s %s' % (myfile + '_tmp', myfile )
    print cmd
    os.system( cmd )

def create_data_monthly_cat(db, year, month, cat, slow_ok = True):
    """Creates the files with the per-month data in it. Restricted to one cat"""

    query = \
    """
    select count(*),fr_user from dewiki_p.flaggedrevs 
    where 
    fr_flags = 'dynamic'
    and fr_timestamp like '%s%02d%%'
    and fr_page_id in (select * from %s)
    group by fr_user
    order by count(*)
    %s
    """ % (year, month, "u_hroest.pages_" + cat, slow_ok_text[slow_ok])

    myfile = path + 'all_month_users_%s%02d%s'% (year, month, cat)
    f = open(myfile + '_tmp', 'w')
    print "writing into " , f.name
    cursor = db.cursor()
    cursor.execute( query )
    rows = cursor.fetchall()
    f.write( 'count(*)\tfr_user\n' )
    for r in rows:
        f.write( '%s\t%s\n' % (r[0], r[1]) )
    f.close()

    #after closing we move the tmp file to the real location
    import os
    print 'moving now'
    cmd  = 'mv %s %s' % (myfile + '_tmp', myfile )
    print cmd
    os.system( cmd )

def create_cat_tables(db, name):
    #db = MySQLdb.connect(read_default_file="/home/hroest/.my.cnf")
    c = db.cursor()
    c.execute( 'drop table if exists u_hroest.pages_%s' % name)
    c.execute( "create table u_hroest.pages_%s( id_page INT)" % name)
    result = db_api.db_get_articles_in_category_object( 'de' , name,  c, depth = -100 )
    ids = [page.id for page in result]
    prepared = "insert into u_hroest.pages_%s" % name
    c.executemany( prepared + " (id_page) values (%s)", ids)

