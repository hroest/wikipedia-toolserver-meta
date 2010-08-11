"""
This module is a python API to the toolserver database.
"""
import datetime, time
import MySQLdb

class UnFlagged():
    """Class to hold a page and its revision info"""
    def __init__(self): pass
    def initialize_with_db( self, l ):
        self.page_nr = l[0]
        self.page_title = l[1]
        self.latest = l[2]
        self.stable = l[3]
    def get_unflagged(self, c):
        all_revisions = get_all_revisions( c, self.page_nr) 
        unflagged = [ rev for rev in reversed( all_revisions ) if rev[0] > self.stable]
        self.first_unflagged = unflagged[-1]
        first_time  = self.first_unflagged[6]
        #now = datetime.datetime.now()
        self.first_time = datetime.datetime(*time.strptime(
             first_time, "%Y%m%d%H%M%S")[0:5])
        #difference = now - then

def get_all_revisions(c, page_nr, wiki="dewiki_p"):
    c.execute( "select * from %(wiki)s.revision where rev_page=%(page_id)s" % {
        'wiki': wiki, 'page_id' : page_nr})
    return c.fetchall()

def make_db_safe ( title ):
    title = title.strip()
    title = title.replace( " ", "_")
    title = title.replace( '"', '\"')
    return title

def db_get_articles_in_category( language , category, c , depth = 0 , 
    namespace = 0 , exclude = [], done_cats = [],
    no_redirects = False , limit = '' , project = 'wikipedia' , 
         only_redirects = False ):
    """Returns a list of all articles in a category. 
    As input, the language, category name and a db-cursor is provided.
    3x improvement when cursor is not regenerated in the fxn.
    """

    category = make_db_safe( category )
    if category in done_cats: return []
    if category in exclude: return []

    db = language + 'wiki_p' ;
    if limit != '':  limit = "LIMIT " + limit;

    ret = []
    subcats = []
    red = ''
    if no_redirects  : red =  ' AND page_is_redirect=0' 
    if only_redirects:  red = ' AND page_is_redirect=1' ;

    sql = """SELECT page_title,page_namespace FROM page,categorylinks 
        WHERE page_id=cl_from AND cl_to="%s" """ % category
    sql += red + limit 

    c.execute( "use " + db)
    tmp = c.execute( sql )
    result = c.fetchall()
    for o in result:
        page_title = o[0]
        page_namespace = o[1]
        if ( page_namespace == 14 and (depth > 0 or depth < -99)  ):
            subcats.append( o[0] )
        if page_namespace != namespace: continue

        if page_title in exclude: continue 
        ret.append( page_title )


    done_cats.append( category )
    for sc in subcats:
        ret2 = db_get_articles_in_category( language, sc, c, depth -1, 
            namespace, exclude, done_cats, no_redirects, limit, 
            project, only_redirects)
        for r in ret2: 
            if not r in ret: ret.append( r )

    return ret ;

class Page:
    def __init__(self): pass

def db_get_articles_in_category_object( language, category, c , depth = 0 , 
    namespace = 0 , exclude = [], done_cats = [],
    no_redirects = False , limit = '' , project = 'wikipedia' , 
    only_redirects = False ):

    non_unique_result = _db_get_articles_in_category_object( language,
        category, c, depth, namespace , exclude, done_cats,
        no_redirects, limit, project, only_redirects)

    result = []
    rids = {}
    for r in non_unique_result:
        if not r.id in rids:
            result.append( r)
            rids[r.id] = ''

    return result

def _db_get_articles_in_category_object( language , category, c , depth = 0 , 
    namespace = 0 , exclude = [], done_cats = [],
    no_redirects = False , limit = '' , project = 'wikipedia' , 
         only_redirects = False ):
    """Returns a list of all articles in a category. 
    As input, the language, category name and a db-cursor is provided.
    3x improvement when cursor is not regenerated in the fxn.
    """

    category = make_db_safe( category )
    if category in done_cats: return []
    if category in exclude: return []

    db = language + 'wiki_p' ;
    if limit != '':  limit = "LIMIT " + limit;

    ret = []
    subcats = []
    red = ''
    if no_redirects  : red =  ' AND page_is_redirect=0' 
    if only_redirects:  red = ' AND page_is_redirect=1' ;

    sql = """SELECT page_title,page_namespace, page_id
        FROM page,categorylinks 
        WHERE page_id=cl_from AND cl_to="%s" """ % category
    sql += red + limit 

    c.execute( "use " + db)
    tmp = c.execute( sql )
    result = c.fetchall()
    for o in result:
        page = Page()
        page.title = o[0]
        page.namespace = o[1]
        page.id = o[2]
        if ( page.namespace == 14 and (depth > 0 or depth < -99)  ):
            subcats.append( o[0] )
        if page.namespace != namespace: continue
        if page.title in exclude: continue 

        ret.append(page)

    done_cats.append( category )
    for sc in subcats:
        ret2 = db_get_articles_in_category_object( language, sc, c, depth -1, 
            namespace, exclude, done_cats, no_redirects, limit, 
            project, only_redirects)
        ret.extend( ret2 )

    return ret ;

