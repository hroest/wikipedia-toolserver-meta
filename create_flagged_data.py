

def create_data_daily(db, year, month, day):
    """Creates the files with the per-month data in it. """

    query = \
    """
    select count(*),fr_user from dewiki_p.flaggedrevs 
    where 
    fr_flags = 'dynamic'
    and fr_timestamp like '%s%02d%02d%%'
    group by fr_user
    order by count(*);
    """ % (year, month, day)

    myfile = '/home/hroest/flagged_data/all_month_day%s%02d%02d'% (year, month, day )
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

def create_data_monthly(db, year, month):
    """Creates the files with the per-month data in it. """

    query = \
    """
    select count(*),fr_user from dewiki_p.flaggedrevs 
    where 
    fr_flags = 'dynamic'
    and fr_timestamp like '%s%02d%%'
    group by fr_user
    order by count(*);
    """ % (year, month)

    myfile = '/home/hroest/flagged_data/all_month_users_%s%02d'% (year, month )
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

