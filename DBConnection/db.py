import sqlite3 as sql

conn = sql.connect("DBConnection/school_library.db")
print("Connected", conn)
cursor = conn.cursor()
print("Cursor:", cursor)

cursor.execute("select * from books")
books = cursor.fetchall()

conn.close()