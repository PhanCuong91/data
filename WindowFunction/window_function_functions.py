import sqlite3
import pandas as pd
from tabulate import tabulate

# create a sqlite database with name test_sqlite.db
db_path = "data/db_test.db"

# path of spreadsheet file
excel_file = 'data/test_data.xlsx'
# read spreadsheet data and put to dataframe
test_data = pd.read_excel(excel_file, sheet_name='test', header=0)
table_test = """
    CREATE TABLE test (city TEXT, id INTEGER, sold INTEGER, month INTEGER)
    """

with sqlite3.connect(db_path) as con:
    # delete the table if it exist
    con.execute( "DROP TABLE IF EXISTS test;")
    # execute these commands to create database tables
    con.execute(table_test)
    test_data.to_sql('test', con=con, if_exists='append',index=False)


# Aggregate functions 
cols = ['city', 'id','sold','month',"min_rows",'max_rows','count_rows','sum_rows','average_rows']
cmd3 = """
SELECT city,id,sold,month,
MIN(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[4]+""",
MAX(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[5]+""",
COUNT(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[6]+""",
SUM(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[7]+""",
AVG(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[8]+"""
FROM tb
ORDER BY city,month
"""
# print (cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))


# Ranking functions
cols = ['city', 'id','sold','month',"min_rows",'max_rows','count_rows','sum_rows','average_rows']
cmd3 = """
SELECT city,id,sold,month,
MIN(sold) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[4]+""",
MAX(sold) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[5]+""",
COUNT(sold) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[6]+""",
SUM(sold) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[7]+""",
AVG(sold) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[8]+"""
FROM tb
ORDER BY month
"""
# print (cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))

# Distribution Functions
cols = ['city', 'id','sold','month',"percent_rank",'cume_dist']
cmd3 = """
SELECT city,id,sold,month,
PERCENT_RANK() OVER (
    ORDER BY sold) AS """ +cols[4]+""",
CUME_DIST() OVER (
    ORDER BY sold) AS """ +cols[5]+"""
FROM tb
ORDER BY sold
"""
# print (cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))

# Analytic Fucntions
# Lead and Lag functions
cols = ['city', 'id','month','sold',"lead",'lag']
cmd3 = """
SELECT city,id,month,sold,
LEAD(sold,2,0) OVER (
    ORDER BY month) AS """ +cols[4]+""",
LAG(sold,2,0) OVER (
    ORDER BY month) AS """ +cols[5]+"""
FROM tb
ORDER BY month
"""
print (cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))

# NTILE function
cols = ['city', 'id','month','sold',"ntile_3","ntile_7"]
cmd3 = """
SELECT city,id,month,sold,
NTILE(4) OVER (
    ORDER BY month) AS """ +cols[4]+""",
NTILE(7) OVER (
    ORDER BY month) AS """ +cols[5]+"""
FROM tb
ORDER BY month
"""

print (cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))

# First value, Last value and Nth value functions
cols = ['city', 'id','month','sold',"first_value","last_value","second_value"]
cmd3 = """
SELECT city,id,month,sold,
FIRST_VALUE(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING) AS """ +cols[4]+""",
LAST_VALUE(sold) OVER (
    PARTITION BY city
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING) AS """ +cols[5]+""",
NTH_VALUE(sold,2) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING) AS """ +cols[6]+"""
FROM tb
ORDER BY city,month
"""
# print (cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))