#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python Version
#Python 2.7.12

#Imports

import connection
import logging
import datetime

#Change The severity level, the message format, and destination of logs

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/vagrant/logAnalysis/report.log',
                    filemode='w')
#function top article: extraction the most popular article in PostgreSQL DB
def pop_article():
    conn = connection.ps_connection()
    logging.debug('Executing query article')
    conn.execute('''select articles.title, count(log.id) as views 
                        from articles, log 
                    where log.path = CONCAT('/article/', articles.slug)
                    and log.status ='200 OK' 
                    group by articles.title 
                    order by views desc 
                    limit 3;''')
    result = conn.fetchall()
    logging.debug('Query Article Executed')
    return result



#function top author: extraction the most popular author in PostgreSQL DB
def pop_author():
    conn = connection.ps_connection()
    logging.debug('Executing query author')
    conn.execute('''select authors.name, count(log.id) as views 
                        from articles, authors,log 
                        where articles.author = authors.id 
                        and log.path = CONCAT('/article/', articles.slug) 
                        and log.status ='200 OK' 
                        group by authors.name
                        order by views desc;''')
    result = conn.fetchall()
    logging.debug('Query Author Executed')
    return result

#function get_logs: extraction requests lead to errors in PostgreSQL DB
def get_logs():
    conn = connection.ps_connection()
    logging.debug('Executing query log')
    conn.execute('''SELECT *
FROM  (SELECT table_get.DATE,
              Cast(Round((table_error.get_error * 100.00 ) / table_get.getrequest, 2) AS
                   numeric
                     ) AS PERCENT
       FROM   (SELECT To_char(TIME, 'DD-MON-YYYY') AS DATE,
                      Count(*)                     AS getrequest
               FROM   log
               GROUP  BY DATE) AS table_get
              JOIN table_error
                ON table_get.DATE = table_error.DATE) AS res
WHERE  percent > 1''')
    result = conn.fetchall()
    logging.debug('Query Log Executed')
    return result

#Date variable to show date in the screen
date = datetime.datetime.now()

#function out_put: receive the set of data and some other arguments in order to format the output.
def out_put(query, *args):
    adorn = (40 * '*')
    print("{0} {1} {0} \n").format(adorn, args[0])
    print("DATE: " + date.strftime("%c") + args[2])
    for row in query:
        print(80 * '-')
        print('\t' + str(row[0]) + ' - ' + str(row[1]) + args[1])

    return " "

#variables to define a title to each report
title_article ='''
 What are the most popular three articles of all time?
'''
title_author ='''
Who are the most popular article authors of all time?
'''

title_log ='''
On which days did more than 1% of requests lead to errors?
'''

#Call functions
logging.debug('call function top_article')
print(out_put(pop_article(), 'Article Report', ' - views', title_article))

logging.debug('call function top_author')
print(out_put(pop_author(), 'Author Report', ' - views', title_author))

logging.debug('call function get_logs')
print(out_put(get_logs(), 'Log Report', '% Error', title_log))

#Finished the Script!
logging.debug('Finish Script')