#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="a43ff155",  # your password
                     db="NFL")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
cur.execute("""CREATE TABLE song ( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        Win varchar(50),
        )""")

# # Use all the SQL you like
# cur.execute("SELECT * FROM YOUR_TABLE_NAME")
#
# # print all the first cell of all the rows
# for row in cur.fetchall():
#     print row[0]

db.close()
