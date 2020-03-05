CREATE DATABASE IF NOT EXISTS hotel_booking_db;
use hotel_booking_db;

CREATE TABLE rooms(
    room_id INT(6) UNSIGNED NOT NULL PRIMARY KEY,
    room_type VARCHAR(32),
    capacity INT(6),
    bathroom BOOLEAN,
    balcony BOOLEAN,
    price INT(6)
);

CREATE TABLE bookings(
    booking_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    booked_room_id INT(6) UNSIGNED NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    check_in DATE,
    check_out DATE,
    FOREIGN KEY (booked_room_id) REFERENCES rooms(room_id)
);

INSERT INTO rooms VALUES (1, "Apartament", 4, True, False, 120);