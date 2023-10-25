# Link de documentacion para el uso en terminal: https://www.sqlitetutorial.net/sqlite-commands/
# Step 1: Import the SQLite library
import sqlite3

def initDatabase():
    # Step 2: Connect to the database (or create a new one if it doesn't exist)
    conn = sqlite3.connect('hotel.db')

    # Step 3: Create a cursor object to interact with the database
    cursor = conn.cursor()

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

def getAllRooms():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM rooms")
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return rows

def getAllReserves():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reserves")
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return rows

def insertReservations(params):
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    sql = "INSERT INTO reserves (customer_full_name, customer_email, date_entry, date_out, room_id, amount) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (
        params['customer_full_name'],
        params['customer_email'],
        params['date_entry'],
        params['date_out'],
        params['room_id'],
        params['amount']
    ))

    conn.commit()
    conn.close()

    return True

def insertDummyreservations():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO reserves (customer_full_name, customer_email, date_entry, date_out, room_id, amount) VALUES ('Cliente 1', 'cliente1@correo.com', '2023-10-23 10:00:00', '2023-10-25 12:00:00', 101, 200), ('Cliente 2', 'cliente2@correo.com', '2023-10-24 11:00:00', '2023-10-26 13:00:00', 102, 250), ('Cliente 3', 'cliente3@correo.com', '2023-10-25 12:00:00', '2023-10-27 14:00:00', 103, 300);")

    conn.commit()
    conn.close()

    return True

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
