 # -*- coding: utf-8  -*-

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
        self.id        = l[0]
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
        self.longest_delay = len( self.myHist) - 1
        #self.myHist.extend( [0 for i in range(100)])
        #self.cumulative = [sum( myHist[:i]) for i in range(len(myHist))]
    def get_extended(self, db):
        cursor = db.cursor()
        cursor.execute( 
            """select uncompress(r_timestamps) 
                from u_hroest.replagExtended 
                where r_replag_id = %s""" % self.id)
        lines = cursor.fetchall()
        l = lines[0] #expect one result
        exec( l[0] )
        self.timestamps = timestamps

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

    resolution_hrs = 24

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
        myHist[ int(unix_lag) / (3600* resolution_hrs ) ] += 1
        timestamps.append( unix_lag )

    #shorten myHist a bit so that there are fewer zeros
    i= 0
    for entry in reversed( myHist ):
        if entry != 0: break
        i += 1
    myHist = myHist[ : 1000-i]

    return lines, myHist, timestamps, query_time

def create_hist_from_timestamps( timestamps, resolution_hrs):

    bigNr = 10000
    myHist = [0 for i in range( bigNr )]
    for unix_lag in timestamps:
        myHist[ int(unix_lag) / (3600* resolution_hrs ) ] += 1

    #shorten myHist a bit so that there are fewer zeros
    i= 0
    for entry in reversed( myHist ):
        if entry != 0: break
        i += 1
    myHist = myHist[ :  bigNr - i]
    return myHist

def create_plot(myHist, name='regular', xlabel=None, plot_lines=False):
    if xlabel == None: xlabel = u"Rückstand in Tagen"
    replag_data = 'replag_hist.csv' 
    plot_name = 'replag_plot' 
    pic_file =  '../tmp/pics/replag%s.png' % name
    f = open( replag_data, 'w')
    for i, entry in enumerate( myHist):
        f.write('%s\t%s\n' % (i, entry) )

    f.close()

    my_lines = ""
    if plot_lines: my_lines = ",f(x) w l lw 2 lt 2, g(x) w l lw 2 lt 3"

    graph_title = u'Verteilung des Alters der ungesichteten Änderungen'
    gnuplot = """
    set terminal png enhanced #size 800,800
    set xlabel "%(xlabel)s"
    set ylabel "Anzahl Artikel"
    set output "%(pic_file)s"
    set title "%(graph_title)s"
    set xrange[-1:%(max_lag)s]
    set yrange[0:]
    set nokey
    f(x)=600
    g(x)=300
    plot "replag_hist.csv"  notitle with boxes lt -1 lw 2 %(my_lines)s
    """ % { 'pic_file' : pic_file, 'graph_title' : graph_title, 
           'max_lag' : len( myHist ), 'xlabel' : xlabel, 'my_lines' : my_lines}

    f = open(plot_name, 'w')
    f.write( gnuplot.encode( 'iso8859'))
    f.close()

    import os 
    os.system( "gnuplot %s" % plot_name )

    #print '<br/>' * 2
    print "<img src=\"%s\">" % pic_file

    #cleanup
    os.system("rm %s" % plot_name)
    os.system("rm %s" % replag_data)

def create_plot_kernel(myHist, name='regular', xlabel=None, h = 1.2):
    if xlabel == None: xlabel = "Rueckstand in Tagen"
    replag_data = 'replag_hist.csv' 
    plot_name = 'replag_plot' 
    pic_file =  '../tmp/pics/replag%s.png' % name

    def K(x):
        return (2*3.14)**(-0.5)*2.718**(-x*x*0.5)

    mysmooth = []
    for x,y in enumerate(myHist):
        s = 0.0
        for xi, yi in enumerate(myHist):
            s += 1/h * K( (x-xi) / h ) * yi
        mysmooth.append( s  )


    f = open( replag_data, 'w')
    for i, entry in enumerate( mysmooth ):
        f.write('%s\t%s\n' % (i, entry) )

    f.close()

    graph_title = u'Verteilung des Alters der ungesichteten Änderungen'
    gnuplot = """
    set terminal png enhanced #size 800,800
    set xlabel "%(xlabel)s"
    set ylabel "Anzahl Artikel"
    set output "%(pic_file)s"
    set title "%(graph_title)s"
    set xrange[-1:%(max_lag)s]
    plot "replag_hist.csv"  notitle with lines lt -1 lw 2
    """ % { 'pic_file' : pic_file, 'graph_title' : graph_title, 
           'max_lag' : len( myHist ), 'xlabel' : xlabel}

    f = open(plot_name, 'w')
    f.write( gnuplot.encode( 'iso8859'))
    f.close()

    import os 
    os.system( "gnuplot %s" % plot_name )

    #print '<br/>' * 2
    print "<img src=\"%s\">" % pic_file

    #cleanup
    #os.system("rm %s" % plot_name)
    #os.system("rm %s" % replag_data)

def revlag_color_cursor_month(db, year, month):
    cursor = db.cursor()
    next_month = month + 1 
    next_year = year
    if next_month == 13: next_year = year + 1; next_month = 1
    start = datetime.datetime( year, month, 1)
    end = datetime.datetime( next_year, next_month, 1)

    start_unix = time.mktime( start.timetuple() )  
    end_unix = time.mktime( end.timetuple() )  - 1 #the new month minus one sec
    cursor.execute( """ select * from u_hroest.replag 
                   where r_timestamp between %s and %s""" %
          (start_unix, end_unix )  )
    return cursor

def revlag_color_cursor_lastseconds(db, seconds = 3600):
    cursor = db.cursor()
    now = datetime.datetime.now()
    now_unix = time.mktime( now.timetuple() )  
    time_ago = now_unix - ( seconds )
    cursor.execute( 'select * from u_hroest.replag where r_timestamp > %s' %
                  time_ago )
    return cursor

def revlag_color_cursor_lastweek(db):
    cursor = db.cursor()
    now = datetime.datetime.now()
    now_unix = time.mktime( now.timetuple() )  
    time_ago = now_unix - (7 * 24 * 3600)
    cursor.execute( 'select * from u_hroest.replag where r_timestamp > %s' %
                  time_ago )
    return cursor

def revlag_color_cursor_last24h(db):
    cursor = db.cursor()
    now = datetime.datetime.now()
    now_unix = time.mktime( now.timetuple() )  
    time_ago = now_unix - (24 * 3600)
    cursor.execute( 'select * from u_hroest.replag where r_timestamp > %s' %
                  time_ago )
    return cursor

def revlag_color_cursor_all(db):
    cursor = db.cursor()
    cursor.execute( 'select * from u_hroest.replag' )
    return cursor

def revlag_color_lines_allXh(db, all_hours=6):
    all_replicates = int( all_hours * 4 )
    cursor = db.cursor()
    cursor.execute( 'select * from u_hroest.replag' )
    lines = cursor.fetchall()
    return lines[::all_replicates] 

def revlag_color_plot(cursor, plot_nr=0,plotsize=800):
    lines = cursor.fetchall()
    _revlag_color_plot(lines, plot_nr,plotsize)

def _revlag_color_plot(lines, plot_nr=0,plotsize=800):
    plot_name = 'tmp_revlagcolor%s' % plot_nr
    data_file = 'tmp_revlagcolor_data%s' % plot_nr
    pic_file =  '../tmp/pics/tmp_revlagcolor_pic%s' % plot_nr



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
    u"""
    set terminal png enhanced size %(size)s,%(size)s
    set xdata time
    set timefmt "%%Y-%%m-%%d-%%H-%%M"
    set format x "%%H:%%d.%%m.%%Y"
    set xtics scale 1,0 nomirror rotate
    set yrange[0:]
    set y2range[0:]
    set y2tics 0,1000
    set ytics 0,1000

    set xlabel "Datum (H:d-m-Y)"
    set ylabel "Anzahl Artikel"
    set key outside 
    set tics out
    set title "Verteilung des Alters der ungesichteten Änderungen über Zeit"
    set output "%(pic_file)s"
    plot \
    "%(data_file)s" using 1:2 with filledcurve x1 title "total", \
    "%(data_file)s" using 1:3 with filledcurve x1 title "jünger als 10 Tage",\
    "%(data_file)s" using 1:4 with filledcurve x1 title "jünger als 7 Tage", \
    "%(data_file)s" using 1:5 with filledcurve x1 title "jünger als 5 Tage", \
    "%(data_file)s" using 1:6 with filledcurve x1 title "jünger als 3 Tage", \
    "%(data_file)s" using 1:7 with filledcurve x1 title "jünger als 1 Tag" lt 7
    #"%(data_file)s" using 1:7 with filledcurve x1 title "younger than 1 day" lt -1
    """ % { 'data_file' : data_file, 'pic_file' : pic_file, 'size' : plotsize}
    #here work: lt -1, 7 

    f = open(plot_name, 'w')
    f.write( gnuplot.encode( 'iso8859'))
    f.close()

    import os 
    os.system( "gnuplot %s" % plot_name )

    print '<br/>' * 2
    print "<img src=\"%s\">" % pic_file

    #cleanup
    os.system("rm %s" % plot_name)
    os.system("rm %s" % data_file)

def never_reviewed_pages(db):
    """Get the number of never reviewed articles at the current timepoint from the db."""

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
    """This functions inserts the current lag distribution into the db.
    
    It will populate u_hroest.replag and u_hroest.replagExtended with 
    some summary statistics values and the compressed whole timestamps of 
    all unreviewed changes, from which the distribution can be recovered.
    """
    cursor = db.cursor()
    now = datetime.datetime.now()
    never_reviewed = never_reviewed_pages(db)
    lines, myHist, timestamps, query_time = execute_unreviewed_changes_query(db)
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
    last_id = db.insert_id()
    cursor.execute( 'commit;' )
    #
    mytime = 'timestamps = ' + str(timestamps)
    query = """
    insert into u_hroest.replagExtended (
     r_replag_id ,
     r_timestamps 
     )  VALUES (%s, compress('%s') )
     """ % ( last_id, mytime)
    cursor.execute( query )
    cursor.execute( 'commit;' )
    #select r_replag_id, uncompress(r_timestamps) from u_hroest.replagExtended;

###########################################################################
###########################################################################
###########################################################################

def quick_fix_db():
    cursor = replag_lib.revlag_color_cursor_all(db)
    lines = cursor.fetchall()
    import datetime
    for ii,l in enumerate(lines):
        timestamp = l[1]
        dtime = datetime.datetime.fromtimestamp( timestamp )
        dstring = dtime.strftime('%Y-%m-%d-%H-%M' )
        exec( l[2] )
        if timestamp > 1270978201: 
            newHist = []
            for i in range( 0, len( myHist), 8):
                mysum =  sum( myHist[i:i+8] )
                i, mysum
                newHist.append( mysum )
            myHist = newHist
        median =        l[3]
        P75 =           l[4]
        P95 =           l[5]
        mean =          l[6]
        unreviewed =     l[7]
        neverreviewed =     l[8]
        mydist = 'myHist = ' + str(myHist)
        query = """
        insert into u_hroest.replag(
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
               unreviewed, neverreviewed)
        cursor.execute( query) 
        cursor.execute( 'commit;' )
