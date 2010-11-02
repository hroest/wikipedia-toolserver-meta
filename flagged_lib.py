 # -*- coding: utf-8  -*-

import time
import datetime 
import create_flagged_data

def create_lagging_user(db):
    """This functions creates a table with users sorted by unflagged changes.
    
    It will populate u_hroest.replag and u_hroest.replagExtended with 
    some summary statistics values and the compressed whole timestamps of 
    all unreviewed changes, from which the distribution can be recovered.
    """
    cursor = db.cursor()
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())
    #
    cursor.execute('drop table if exists u_hroest.replag_users ')
    query = """
    create table u_hroest.replag_users as 
    select count(*), fp_page_id, fp_stable, rev_id, rev_user,
    rev_user_text, rev_timestamp, %s as updated_at
    from dewiki_p.flaggedpages fp 
    inner join dewiki_p.revision r on fp.fp_page_id = r.rev_page 
    #inner join dewiki_p.page p on p.page_id = fp.fp_page_id
    where fp_reviewed=0 and r.rev_id > fp.fp_stable group by fp_page_id, rev_user_text
    %s
    """ %  (int(timestamp) , create_flagged_data.slow_ok_text[True])
    #
    #f = open('tmp_mysql.query', 'w'); f.write( query ); f.close()
    cursor.execute( query )
    cursor.execute( 'commit;' )

