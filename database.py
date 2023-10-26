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

def getAllReservesForMail(email):
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = f"""
        SELECT *
        FROM reserves
        JOIN rooms ON rooms.id = reserves.room_id
        WHERE customer_email = '{email}';
        """

    cursor.execute(query)
    rows = cursor.fetchall()

    dictionaryRecords = []
    for item in rows:
        dictionaryRecords.append({k: item[k] for k in item.keys()})

    conn.commit()
    conn.close()

    return dictionaryRecords

def removeReservation(reservationId):
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    delete_query = f"DELETE FROM reserves WHERE id = {reservationId}"
    cursor.execute(delete_query)

    conn.commit()
    conn.close()

    return True

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

    cursor.execute("INSERT INTO reserves (customer_full_name, customer_email, date_entry, date_out, room_id, amount) VALUES ('Cliente 1', 'cliente1@correo.com', '2023-11-05 11:00:00', '2023-10-25 12:00:00', 1, 200), ('Cliente 2', 'cliente2@correo.com', '2023-11-05 11:00:00', '2023-10-26 13:00:00', 2, 250), ('Cliente 3', 'cliente3@correo.com', '2023-11-05 11:00:00', '2023-10-27 14:00:00', 3, 300);")

    conn.commit()
    conn.close()

    return True

def insertDummyRooms():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    cursor.executemany("INSERT INTO rooms (description, capacity, night_price) VALUES (?, ?, ?)", [
        ('Habitación 101', 2, 150),
        ('Habitación 102', 3, 200),
        ('Habitación 103', 4, 250)
    ])

    conn.commit()
    conn.close()

    return True

def searchAvailableRooms(dateEntry, dateOut):
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    query = """
    SELECT rooms.id, rooms.description, rooms.capacity, rooms.night_price
    FROM rooms
    LEFT JOIN reserves ON rooms.id = reserves.room_id
    WHERE reserves.id IS NULL OR (reserves.date_out < ? OR reserves.date_entry > ?);
    """
    cursor.execute(query, (dateEntry, dateOut))
    rows = cursor.fetchall()

    conn.commit()
    conn.close()

    return rows
