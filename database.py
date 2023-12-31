# Link de documentacion para el uso en terminal: https://www.sqlitetutorial.net/sqlite-commands/
import sqlite3

def initDatabase():
    conn = sqlite3.connect('hotel.db')

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

def insertRoom(description, capacity, night_price):
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Inserta un nuevo registro en la tabla 'rooms'
    cursor.execute("INSERT INTO rooms (description, capacity, night_price) VALUES (?, ?, ?)", (description, capacity, night_price))
    conn.commit()
    conn.close()

def deleteRoom(description, capacity, night_price):
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Elimina el registro de la tabla 'rooms' basado en description, capacity, y night_price
    cursor.execute("DELETE FROM rooms WHERE description=? AND capacity=? AND night_price=?", (description, capacity, night_price))

    conn.commit()
    conn.close()

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

    cursor.execute("INSERT INTO reserves (customer_full_name, customer_email, date_entry, date_out, room_id, amount) VALUES ('Cliente 1', 'cliente1@correo.com', '2023-11-05 11:00:00', '2023-11-25 12:00:00', 1, 3000),('Cliente 1', 'cliente1@correo.com', '2023-10-05 11:00:00', '2023-10-25 12:00:00', 1, 3000), ('Cliente 1', 'cliente1@correo.com', '2023-09-05 11:00:00', '2023-09-25 12:00:00', 2, 4000), ('Cliente 2', 'cliente2@correo.com', '2023-11-05 11:00:00', '2023-11-26 13:00:00', 2, 250), ('Cliente 3', 'cliente3@correo.com', '2023-11-15 11:00:00', '2023-11-27 14:00:00', 3, 300);")

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

def updateRoomById(room_id, description, capacity, price):
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE rooms SET description=?, capacity=?, night_price=? WHERE id=?", (description, capacity, price, room_id))

    conn.commit()
    conn.close()
