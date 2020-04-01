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