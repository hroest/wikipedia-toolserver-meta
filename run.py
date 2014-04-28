#!/usr/bin/python 
import datetime
import time 
import MySQLdb
import sys
sys.path.append( '/home/hroest/' )
import replag_lib
today = datetime.date.today()
now = datetime.datetime.now()
this_year = today.year
this_month = today.month


###########################################################################

db = MySQLdb.connect(read_default_file="/home/hroest/.my.cnf")
cursor = db.cursor()
#cursor.execute( 'use u_hroest')

insert_db( db )





"""

create database s51801__hroest;

drop table s51801__hroest.replag;
create table s51801__hroest.replag (
 r_id int auto_increment primary key,
 r_timestamp int,
 r_daily_distr text,
 r_median double,
 r_P75 double, 
 r_P95 double, 
 r_mean double,
 r_unreviewed int,
 r_neverreviewed int
);

alter table u_hroest.replag add index(r_timestamp);


create table s51801__hroest.replagExtended (
 r_replag_id int primary key,
 r_timestamps text
);

"""
