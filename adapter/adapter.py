import datetime
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

class db_connection():
    def __init__(self):
        self.db = mysql.connector.connect(
            host = "db",
            port = "3306",
            user = "root",
            passwd = "root",
            database = "hotel_booking_db",
            autocommit = True
        )
        self.db_cursor = self.db.cursor()

    def check_room_exists(self, room_id):
        query = (f"SELECT * FROM rooms WHERE room_id={room_id}")
        args = (int(room_id))
        self.db_cursor.execute(query, args)
        result = self.db_cursor.fetchall()
        if not result:
            return False, 'Room does not exist'
        return True, 'Room exists already'
        
    def add_room(self, room_id, room_type, capacity, bathroom, balcony, price):
        ret, err = self.check_room_exists(room_id)
        if ret == True:
            return False, err

        if bathroom == 'True':
            bathroom = True
        else:
            bathroom = False

        if balcony == 'True':
            balcony = True
        else:
            balcony = False

        query = ("INSERT INTO rooms (room_id, room_type, capacity, bathroom, balcony, price) VALUES (%s, %s, %s, %s, %s, %s)")
        args = (int(room_id), room_type, int(capacity), bathroom, balcony, int(price))
        self.db_cursor.execute(query, args)
        return True, 'Room added successfully'

    def book(self, room_id, first_name, last_name, check_in, check_out):
        ret, err = self.check_room_exists(room_id)
        if ret == False:
            return False, err

        check_in = check_in.split('/')
        for i in range(len(check_in)):
            check_in[i] = int(check_in[i])

        check_out = check_out.split('/')
        for i in range(len(check_out)):
            check_out[i] = int(check_out[i])

        query = ("INSERT INTO bookings (room_id, first_name, last_name, check_in, check_out) VALUES (%s, %s, %s, %s, %s)")
        args = (int(room_id), first_name, last_name, datetime.date(check_in[2], check_in[1], check_in[0]), datetime.date(check_out[2], check_out[1], check_out[0]))
        self.db_cursor.execute(query, args)
        return True, 'Room was booked successfully'
    
def init():
    db = mysql.connector.connect(
        host = "db",
        port = "3306",
        user = "root",
        passwd = "root",
        database = "hotel_booking_db",
        autocommit = True
    )

    db_cursor = db.cursor()

    results = db_cursor.execute(
        """
        CREATE DATABASE IF NOT EXISTS hotel_booking_db;
        use hotel_booking_db;
        DROP TABLE IF EXISTS bookings;
        DROP TABLE IF EXISTS rooms;

        CREATE TABLE IF NOT EXISTS rooms(
            room_id INT(6) UNSIGNED NOT NULL PRIMARY KEY,
            room_type VARCHAR(32),
            capacity INT(6),
            bathroom BOOLEAN,
            balcony BOOLEAN,
            price INT(6)
        );

        CREATE TABLE IF NOT EXISTS bookings(
            booking_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            room_id INT(6) UNSIGNED NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            check_in DATE,
            check_out DATE,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        );

        INSERT INTO rooms (room_id, room_type, capacity, bathroom, balcony, price) VALUES (1, "Apartament", 4, True, False, 210);
        INSERT INTO rooms (room_id, room_type, capacity, bathroom, balcony, price) VALUES (2, "Double room", 2, True, False, 100);
        commit;
        """,
        multi = True)
        
    for result in results:
        if result.with_rows:
            print("Rows produced by statement '{}':".format(result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))

    db_cursor.close()
    db.close()

db_connection = db_connection()

@app.route("/admin", methods=["POST"])
def add_room():
    room_id = request.json['room_id']
    room_type = request.json['room_type']
    capacity = request.json['capacity']
    bathroom = request.json['bathroom']
    balcony = request.json['balcony']
    price = request.json['price']

    ret, err = db_connection.add_room(room_id, room_type, capacity, bathroom, balcony, price)
    if ret == True:
        status = 'Success'
    else:
        status = 'Failed'

    return jsonify({
        'status' : status,
        'reason' : err,
    })

@app.route("/booking", methods=["POST"])
def book():
    room_id = request.json['room_id']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    check_in = request.json['check_in']
    check_out = request.json['check_out']

    ret, err = db_connection.book(room_id, first_name, last_name, check_in, check_out)
    if ret == True:
        status = 'Success'
    else:
        status = 'Failed'

    return jsonify({
        'status' : status,
        'reason' : err,
    })

if __name__ == "__main__":
    init()
    app.run(host = '0.0.0.0', port = 32500, debug = True)

