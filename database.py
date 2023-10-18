# Link de documentacion para el uso en terminal: https://www.sqlitetutorial.net/sqlite-commands/

import sqlite3

def initDatabase():
    # Step 1: Import the SQLite library
    # Step 2: Connect to the database (or create a new one if it doesn't exist)
    conn = sqlite3.connect('hotel.db')

    # Step 3: Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Step 4: Create a table called 'rooms' with columns 'id', 'description', 'capacity', and 'nigth_price'
    # and table called 'reserves' with columns 'id',  
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms
                    (
                        id INTEGER PRIMARY KEY,
                        description TEXT,
                        capacity INT,
                        night_price INT)''')
    conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS reserves
                    (
                        id INTEGER PRIMARY KEY,
                        customer_full_name TEXT,
                        customer_email TEXT,
                        date_entry DATETIME,
                        date_out DATETIME,
                        room_id INT,
                        amount INT
                        )''')
    conn.commit()
    conn.close()
# Step 5: Insert a new employee into the 'employees' table
# cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", ('John Doe', 'Software Engineer', 80000))
# conn.commit()

# Step 6: Query data from the 'employees' table
# cursor.execute("SELECT * FROM employees")
# rows = cursor.fetchall()

# Print the rows
# for row in rows:
#     print(row)

# Step 7: Update the salary of the employee with id 1
# cursor.execute("UPDATE employees SET salary = ? WHERE id = ?", (90000, 1))
# conn.commit()

# Step 8: Delete the employee with id 1
# cursor.execute("DELETE FROM employees WHERE id = ?", (1,))
# conn.commit()

# Step 9: Close the connection when you're done
