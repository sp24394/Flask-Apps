import sqlite3 as sql

conn = sql.connect("DBConnection/school_library.db")
print("Connected", conn)
conn.row_factory = sql.Row
cursor = conn.cursor()
print("Cursor:", cursor)

conn.close()