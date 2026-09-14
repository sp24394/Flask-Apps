import sqlite3 as sql

conn = sql.connect("DBConnection/school_library.db")
print("Connected", conn)
conn.row_factory = sql.Row
cursor = conn.cursor()
print("Cursor:", cursor)

cursor.execute("""INSERT INTO books 

                  (title, author, genre, publication_year, pages, available_copies) 

                  VALUES (?, ?, ?, ?, ?, ?)""", 

               ("Aue", "Becky Manawatu", "Fiction", 2019, 344, 2)) 
print("Added") 
conn.commit()

conn.close()