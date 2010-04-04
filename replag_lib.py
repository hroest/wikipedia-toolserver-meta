import time
import datetime

def execute_unreviewed_changes_query(db):
    query = """
        SELECT page_id,page_title,page_latest,fp_stable, rev_len, rev_timestamp
        FROM page,flaggedpages, revision
        WHERE fp_page_id=page_id 
        AND page_latest<>fp_stable AND page_namespace=0
        AND rev_id=page_latest
        ORDER BY rev_timestamp;
    """
    cursor = db.cursor()
    cursor.execute( 'use dewiki_p' )


    start = time.time()
    cursor.execute( query )
    end = time.time()
    query_time = end - start
    lines = cursor.fetchall()

    today = datetime.date.today()
    now = datetime.datetime.now()
    now_unix = time.mktime( now.timetuple()  )  

    timestamps = []
    ll = lines[0][-1]
    myHist = [0 for i in range(1000)]
    for l in lines:
        ll = l[-1]
        tuple = time.strptime(ll, "%Y%m%d%H%M%S")
        unix_lag = now_unix - time.mktime( tuple ) 
        myHist[ int(unix_lag) / (3600*24) ] += 1
        timestamps.append( unix_lag )

    #shorten myHist a bit so that there are fewer zeros
    i= 0
    for entry in reversed( myHist ):
        if entry != 0: break
        i += 1
    myHist = myHist[ : 1000-i]

    return myHist, timestamps, query_time

def create_plot(myHist):
    replag_data = 'replag_hist.csv' 
    plot_name = 'replag_plot' 
    pic_file =  '../tmp/pics/replag.png' 
    f = open( replag_data, 'w')
    for i, entry in enumerate( myHist):
        f.write('%s\t%s\n' % (i, entry) )

    f.close()

    graph_title = 'Verteilung des Alters der ungesichteten Aenderungen'
    gnuplot = """
    set terminal png enhanced #size 800,800
    set xlabel "Rueckstand in Tagen"
    set ylabel "Anzahl Artikel"
    set output "%(pic_file)s"
    set title "%(graph_title)s"
    set xrange[-1:%(max_lag)s]
    plot "replag_hist.csv"  notitle with boxes lt -1 lw 2
    """ % { 'pic_file' : pic_file, 'graph_title' : graph_title, 
           'max_lag' : len( myHist ) }

    f = open(plot_name, 'w')
    f.write( gnuplot)
    f.close()

    import os 
    os.system( "gnuplot %s" % plot_name )

    print '<br/>' * 2
    print "<img src=\"%s\">" % pic_file

    #cleanup
    os.system("rm %s" % plot_name)
    os.system("rm %s" % replag_data)

def never_reviewed_pages(db):

    query = """
    #select all articles that were never reviewed
    select count(*) from dewiki_p.page 
    #not flagged
    where page_id not in (select distinct fp_page_id from dewiki_p.flaggedpages)
    #not a redirection
    and page_id not in (select distinct rd_from from dewiki_p.redirect)
    #and in article namespace
    and page_namespace = 0;
    """ 
    c = db.cursor()
    c.execute( query )
    return c.fetchone()[0]

def insert_db(db):
    cursor = db.cursor()
    now = datetime.datetime.now()
    never_reviewed = never_reviewed_pages(db)
    myHist, timestamps, query_time = execute_unreviewed_changes_query(db)
    median = timestamps[ len(timestamps) / 2 ]
    P75 = timestamps[ len(timestamps) * 1 / 4 ]
    P95 = timestamps[ len(timestamps) * 1 / 20 ]
    mean = sum(timestamps) / len( timestamps )
    timestamp = time.mktime(now.timetuple())
    mydist = 'myHist = ' + str(myHist)
    #
    query = """
    insert into u_hroest.replag (
     r_timestamp,
     r_daily_distr,
     r_median,
     r_P75,
     r_P95,
     r_mean,
     r_unreviewed,
     r_neverreviewed
    ) VALUES (%s, '%s',  %s,%s,%s,%s,%s,%s)
    """ % ( int(timestamp) , mydist, median, 
           P75, P95, mean, 
           len( timestamps ), never_reviewed)
    #
    #f = open('tmp_mysql.query', 'w'); f.write( query ); f.close()
    cursor.execute( query )
    cursor.execute( 'commit;' )

