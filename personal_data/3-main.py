#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
# cursor.execute("""CREATE TABLE users (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(256),
#     email VARCHAR(256),
#     password VARCHAR(256),
#     ssn VARCHAR(256),
#     phone VARCHAR(256)  
# );""")

# insert

cursor.execute("SELECT * FROM users;")

for row in cursor:
    print(row)
cursor.close()
db.close()
