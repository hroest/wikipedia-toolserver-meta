

def create_data(db, year, month):
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
    print myfile
    f = open(myfile, 'w')
    cursor = db.cursor()
    cursor.execute( query )
    rows = cursor.fetchall()
    f.write( 'count(*)\tfr_user\n' )
    for r in rows:
        f.write( '%s\t%s\n' % (r[0], r[1]) )
    f.close()
