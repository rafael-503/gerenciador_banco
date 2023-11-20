import MySQLdb

db = MySQLdb.connect(
 "localhost",
 "root",
 "123",
 "employees" )
 #asas

cursor = db.cursor()
cursor.execute("select * from departments")

data = cursor.fetchall()

for row in data:
    print(row)

db.close()