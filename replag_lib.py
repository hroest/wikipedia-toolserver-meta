import time
import datetime

def execute_unreviewed_changes_query_fromCache(db):
    cursor = db.cursor()
    cursor.execute( 
        'select * from u_hroest.replag order by r_timestamp desc limit 1')
    lines = cursor.fetchall()
    l = lines[0] #expect one result
    r = revlag( l )
    return r

class revlag:
    def __init__(self, line = None):
        if line: self.init_with_line( line )
    def init_with_line(self, l ):
        self.timestamp = l[1]
        self.dtime = datetime.datetime.fromtimestamp( self.timestamp )
        self.dstring = self.dtime.strftime('%Y-%m-%d-%H-%M' )
        exec( l[2] )
        self.myHist = myHist
        self.median =        l[3]
        self.P75 =           l[4]
        self.P95 =           l[5]
        self.mean =          l[6]
        self.unreviewed =     l[7]
        self.neverreviewed =     l[8]
        self.longest_delay = len( self.myHist)
        #self.myHist.extend( [0 for i in range(100)])
        #self.cumulative = [sum( myHist[:i]) for i in range(len(myHist))]

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

def revlag_color(db):
    plot_name = 'tmp_revlagcolor'
    data_file = 'tmp_revlagcolor_data'
    pic_file =  '../tmp/pics/tmp_revlagcolor_pic'


    cursor = db.cursor()
    cursor.execute( 'select * from u_hroest.replag' )
    lines = cursor.fetchall()

    #f = open('test.out.csv', 'w')
    f = open(data_file, 'w')
    for ii,l in enumerate(lines):
        timestamp = l[1]
        dtime = datetime.datetime.fromtimestamp( timestamp )
        dstring = dtime.strftime('%Y-%m-%d-%H-%M' )
        exec( l[2] )
        median =        l[3]
        P75 =           l[4]
        P95 =           l[5]
        mean =          l[6]
        unreviewed =     l[7]
        neverreviewed =     l[8]
        myHist.extend( [0 for i in range(100)])
        cumulative = [sum( myHist[:i]) for i in range(len(myHist))]
        myformatstr = '%s ' * 7 + '\n'
        f.write( myformatstr  % (dstring, 
        #f.write( myformatstr  % ( ii, 
                               unreviewed,
                               cumulative[10], 
                               cumulative[7], 
                               cumulative[5], 
                               cumulative[3], 
                               cumulative[1] 
                                ))

    f.close()

    gnuplot = \
    """
    set terminal png enhanced #size 800,800
    set xdata time
    set timefmt "%%Y-%%m-%%d-%%H-%%M"
    set format x "%%H:%%d.%%m.%%Y"
    set xtics scale 3,2 nomirror rotate
    set yrange[0:]
    set y2range[0:]
    set y2tics 0,1000
    set ytics 0,1000

    set xlabel "Datum (H:d-m-Y)"
    set ylabel "Anzahl Artikel"
    set key outside 
    set title "Verteilung des Alters der ungesichteten Aenderungen ueber Zeit"
    set output "%(pic_file)s"
    plot \
    "%(data_file)s" using 1:2 with filledcurve x1 title "total", \
    "%(data_file)s" using 1:3 with filledcurve x1 title "younger than 10 days",\
    "%(data_file)s" using 1:4 with filledcurve x1 title "younger than 7 days", \
    "%(data_file)s" using 1:5 with filledcurve x1 title "younger than 5 days", \
    "%(data_file)s" using 1:6 with filledcurve x1 title "younger than 3 days", \
    "%(data_file)s" using 1:7 with filledcurve x1 title "younger than 1 day" lt 7
    #"%(data_file)s" using 1:7 with filledcurve x1 title "younger than 1 day" lt -1
           # fs pattern 2 lc palette cb -45
            #fs pattern 2 lc rgb "#FF00FF"
    """ % { 'data_file' : data_file, 'pic_file' : pic_file}
    #here work: lt -1, 7 

    f = open(plot_name, 'w')
    f.write( gnuplot)
    f.close()

    import os 
    os.system( "gnuplot %s" % plot_name )

    print '<br/>' * 2
    print "<img src=\"%s\">" % pic_file

    #cleanup
    os.system("rm %s" % plot_name)
    os.system("rm %s" % data_file)

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

