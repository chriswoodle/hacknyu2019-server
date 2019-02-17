#Tried another way, but no dice. 
import mysql.connector

server = '34.73.12.198'
db = 'rideable'
username = 'cara'
pw = 'xxxxx'
cnx = mysql.connector.connect(user=username, password=pw,
                              host=server,
                              database=db)

cursor = cnx.cursor()     # get the cursor

tables = cursor.execute("show tables")    # execute 'SHOW TABLES' (but data is not returned

for (table_name,) in cursor:
        print(table_name)