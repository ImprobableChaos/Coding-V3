import sqlite3

id = 1

conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""SELECT role from users WHERE id = ?""", (id,))

role = cursor.fetchone()[0]

print(role)

conn.close()
