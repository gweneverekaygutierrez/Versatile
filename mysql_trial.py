import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="745965", db="pythonspot")

# Create a Cursor object to execute queries.
cur = db.cursor()

# Select data from table using SQL query.
cur.execute("SELECT * FROM examples")

# print the first and second columns
for row in cur.fetchall():
	print(row[0], " ", row[1])

db.close()