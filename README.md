
#Log Analisyer Project

##Functionality


The code should answer three questions:

1. *What are the most popular three articles of all time?* 
2. *Who are the most popular article authors of all time?*
3. *On which days did more than 1% of requests lead to errors?*

The data was store into a PostgreSQL instance with three tables and views created by my myself,
to handle more easily the data. The code of the views you can se below: 


To execute the code I used a virtual machine, manage by vagrant to use the same 
environment you can download the virtual box and Vagrant files [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

#Running The code

Create the database running this command *psql -d news -f newsdata.sql* 
Create the view and run python main.py
 
#Dependencies
1. psycopg2 module to connect to the database.
2. The logging module is part of the standard Python library and provides tracking for events that occur while software runs. 
3. The datetime module supplies classes for manipulating dates and times in both simple and complex ways.


### *Create view* Statements:  

```CREATE CREATE VIEW view_name AS 
           SELECT To_char(TIME, 'DD-MON-YYYY') AS DATE, Count(*) AS get_error
                    FROM   log
                    WHERE  log.status = '404 NOT FOUND'
                    GROUP  BY DATE) AS table_error```                    