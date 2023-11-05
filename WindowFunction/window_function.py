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

# run SQL query with ORDER BY, PARTITION BY and ROWS, RANGE, GROUPS for time_frame  
cols = ['city', 'id','sold','month',"total_rows",'count_rows','total_range','count_range','total_groups','count_groups']
cmd3 = """
SELECT city,id,sold,month,
SUM(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[4]+""",
COUNT(sold) OVER (
    PARTITION BY city
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[5]+""",
SUM(sold) OVER (
    PARTITION BY city
    ORDER BY month
    RANGE BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[6]+""",
COUNT(sold) OVER (
    PARTITION BY city
    ORDER BY month
    RANGE BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[7]+""",
SUM(sold) OVER (
    PARTITION BY city
    ORDER BY month
    GROUPS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[8]+""",
COUNT(sold) OVER (
    PARTITION BY city
    ORDER BY month
    GROUPS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[9]+"""
FROM tb
ORDER BY city,month
"""
# print (cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))

# run SQL query with ORDER BY and ROWS, RANGE, GROUPS for time_frame  
cols = ['city', 'id','sold','month',"total_rows",'count_rows','total_range','count_range','total_groups','count_groups']
cmd3 = """
SELECT city,id,sold,month,
SUM(sold) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[4]+""",
COUNT(sold) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[5]+""",
SUM(sold) OVER (
    ORDER BY month
    RANGE BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[6]+""",
COUNT(sold) OVER (
    ORDER BY month
    RANGE BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[7]+""",
SUM(sold) OVER (
    ORDER BY month
    GROUPS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[8]+""",
COUNT(sold) OVER (
    ORDER BY month
    GROUPS BETWEEN 1 PRECEDING AND 2 FOLLOWING)""" +cols[9]+"""
FROM tb
ORDER BY month
"""
# print(cmd3)
with sqlite3.connect(db_path) as con:
    re=con.execute(cmd3)
print(tabulate(re, headers=cols, tablefmt='psql'))