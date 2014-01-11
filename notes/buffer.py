
    SELECT page_id,page_title,page_latest,fp_stable, rev_len
    FROM page,flaggedpages, revision
    WHERE fp_page_id=page_id 
    AND page_latest<>fp_stable AND page_namespace=0
    AND rev_id=page_latest;


#select all articles that were never reviewed
select * from page 
#not flagged
where page_id not in (select distinct fp_page_id from flaggedpages) 
#not a redirection
and page_id not in (select distinct rd_from from redirect)
#and in article namespace
and page_namespace = 0;

2010-04-04-22-46 6729 6729 6149 5242 3977 2346 

set xdata time
set timefmt "%Y-%m-%d-%H-%M"
set format x "%m.%Y"
set xtics scale 3,2 nomirror rotate
set yrange[0:]
set key outside 
plot \
"test.out.csv" using 1:2 with filledcurve x1 title "total", \
"test.out.csv" using 1:3 with filledcurve x1 title "younger than 10 days", \
"test.out.csv" using 1:4 with filledcurve x1 title "younger than 7 days", \
"test.out.csv" using 1:5 with filledcurve x1 title "younger than 5 days", \
"test.out.csv" using 1:6 with filledcurve x1 title "younger than 3 days", \
"test.out.csv" using 1:7 with filledcurve x1 title "younger than 1 day" 




set yrange[0:]
set key outside 
plot \
"test.out.csv" using 1:2 with filledcurve x1 title "older than 10 days", \
"test.out.csv" using 1:3 with filledcurve x1 title "older than 9 days", \
"test.out.csv" using 1:4 with filledcurve x1 title "older than 8 days", \
"test.out.csv" using 1:5 with filledcurve x1 title "older than 7 days", \
"test.out.csv" using 1:6 with filledcurve x1 title "older than 6 days", \
"test.out.csv" using 1:7 with filledcurve x1 title "older than 5 days", \
"test.out.csv" using 1:8 with filledcurve x1 title "older than 4 days", \
"test.out.csv" using 1:9 with filledcurve x1 title "older than 3 days", \
"test.out.csv" using 1:10 with filledcurve x1 title "older than 2 days", \
"test.out.csv" using 1:11 with filledcurve x1 title "older than 1 day" 
set key outside 
plot \
"test.out.csv" using 1:2 with filledcurve x1 title "older than 10 days", \
"test.out.csv" using 1:3 with filledcurve x1 title "older than 9 days", \
"test.out.csv" using 1:4 with filledcurve x1 title "older than 8 days", \
"test.out.csv" using 1:5 with filledcurve x1 title "older than 7 days", \
"test.out.csv" using 1:6 with filledcurve x1 title "older than 6 days", \
"test.out.csv" using 1:7 with filledcurve x1 title "older than 5 days", \
"test.out.csv" using 1:8 with filledcurve x1 title "older than 4 days", \
"test.out.csv" using 1:9 with filledcurve x1 title "older than 3 days", \
"test.out.csv" using 1:10 with filledcurve x1 title "older than 2 days", \
"test.out.csv" using 1:11 with filledcurve x1 title "older than 1 day" 


select * from revision 
inner join flaggedrevs on fr_rev_id = rev_id
where rev_id = 50283796;

select rev_timestamp, fr_timestamp 
from flaggedrevs 
inner join revision on fr_page_id = rev_page
#where fr_rev_id = 50283796;
where fr_page_id = 305
and fr_rev_id = 45423139
and rev_timestamp < fr_timestamp
#limit 1
;

reload( db_api )




result[0].id

for i in range(1, 4):
    create_flagged_data.create_data_monthly_cat( db, 2010, i, 'schweiz' )

 


#may have multiple per time interval
create table u_hroest.test_tmp2 as 
select rev_timestamp, fr_timestamp from revision 
inner join flaggedrevs on fr_page_id = rev_page
where rev_timestamp <> fr_timestamp
and fr_timestamp like '20100128%' ;

20080902183739
20080902183739

#create table u_hroest.flaggedrevs_hr as select * from flaggedrevs where fr_user = 352933;


desc u_hroest.flaggedrevs_hr;

select count(*), fr_flags from u_hroest.flaggedrevs_hr
where fr_timestamp like '2009%'
group by fr_flags;


select *

select fr_timestamp, fr_tags, fr_flags, page_title
from u_hroest.flaggedrevs_hr
inner join page on page_id = fr_page_id
where fr_timestamp like '200805%'
#and fr_flags = 'utf-8,dynamic'
order by fr_timestamp desc
;

select count(*) 
from u_hroest.flaggedrevs_hr
inner join page on page_id = fr_page_id
where 
#fr_flags not like 'dynamic,auto'
fr_timestamp like '200805%'
;







create temporary table altered_pages as 
select distinct rev_page
from dewiki_p.flaggedrevs 
inner join dewiki_p.revision on rev_id = fr_rev_id
where fr_flags = 'dynamic' 
limit 10;
alter table altered_pages add index( rev_page );


select rev_id, rev_page, rev_user, rev_timestamp, fr_timestamp, fr_flags
from dewiki_p.revision 
left join dewiki_p.flaggedrevs on rev_id = fr_rev_id
#where revision.rev_page in (select * from altered_pages)
where revision.rev_page = 1
limit 10;






create temporary table altered_revs as 
select rev_id, rev_page, rev_user, rev_timestamp
from dewiki_p.revision 
#where revision.rev_page in (select * from altered_pages)
where revision.rev_page = 1
limit 10;
alter table altered_revs add index( rev_id );



select * from altered_revs
inner join dewiki_p.flaggedrevs on rev_id = fr_rev_id;

select * from dewiki_p.flaggedrevs where fr_rev_id = 199798;
