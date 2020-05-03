from flask import render_template, flash, redirect, request, session
from app import app
from app.web_forms import *
import requests
import os
import json

DB_ADAPTER_URL = 'http://adapter:32500'

current_rooms = {}
session = requests.Session()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

def get_bool_string_from_int(s):
    if s:
        return 'Yes'
    return 'No'
   
def get_bookings():
    r = requests.get(DB_ADAPTER_URL + '/bookings')
    bookings = r.json()['bookings']
    for booking in bookings:
        booking[4] = ' '.join(booking[4].split()[1:4])
        booking[5] = ' '.join(booking[5].split()[1:4])
    return bookings
    
def get_rooms():
    r = requests.get(DB_ADAPTER_URL + '/rooms')
    rooms = r.json()['rooms']
    for room in rooms:
        room[3] = get_bool_string_from_int(room[3])
        room[4] = get_bool_string_from_int(room[4])
        room[-1] = '%d lei' % room[-1]
        current_rooms[room[0]] = room
    return rooms
    
def get_booking_ids():
    bookings = get_bookings()
    result = [('0', 'Select a booking')]
    for booking in bookings:
        booking_id = booking[0]
        first_name = booking[2]
        last_name = booking[3]
        check_in = booking[4]
        check_out = booking[5]
        result.append((str(booking_id), 'Booking nr. %d for %s %s between %s and %s' %
                       (booking_id, first_name, last_name, check_in, check_out)))
    return result
    
def get_room_ids():
    rooms = get_rooms()
    result = [('0', 'Select a room')]
    for room in rooms:
        room_id = room[0]
        room_type = room[1]
        room_price = room[-1]
        result.append((str(room_id), '%s (%d) - %s' % (room_type, room_id, room_price)))
    return result
   
@app.route('/add_room', methods={'GET', 'POST'})
def add_room():
    form = NewRoomForm()

    if form.validate_on_submit():
        payload = {'room_type': form.room_type.data,
                   'capacity': form.capacity.data,
                   'bathroom': form.bathroom.data,
                   'balcony': form.balcony.data,
                   'price': form.price.data}
        header = {"Content-Type":"application/json"}
        r = session.post(DB_ADAPTER_URL + '/add_room', headers=header, json=payload)

        title = 'Operation result'
        description = '%s for %s people - %s lei per night' % (form.room_type.data,
                                                    form.capacity.data,
                                                    form.price.data)

        status = r.json()['status']
        reason = r.json()['reason']

        return render_template('result.html', title=title,
                               description=description,
                               status=status, reason=reason)
    return render_template('form.html', form=form, title='Add a room')

@app.route('/delete_booking', methods={'GET', 'POST'})
def delete_booking():
    form = DeleteBookingForm()
    form.booking.choices = get_booking_ids()

    if form.validate_on_submit():
        booking_id = form.booking.data
        payload = {'booking_id': booking_id}
        header = {"Content-Type":"application/json"}
        r = session.post(DB_ADAPTER_URL + '/delete_booking', headers=header, json=payload)

        title = 'Operation result'
        description = 'Delete booking %s' % (booking_id)
        status = r.json()['status']
        reason = r.json()['reason']
        
        return render_template('result.html', title=title,
                               description=description,
                               status=status, reason=reason)
    return render_template('form.html', form=form, title='Delete a booking')

@app.route('/delete_room', methods={'GET', 'POST'})
def delete_room():
    form = DeleteRoomForm()
    form.room.choices = get_room_ids()

    if form.validate_on_submit():
        room_id = form.room.data
        payload = {'room_id': room_id}
        header = {"Content-Type":"application/json"}
        r = session.post(DB_ADAPTER_URL + '/delete_room', headers=header, json=payload)

        title = 'Operation result'
        description = 'Delete room %s' % (room_id)
        status = r.json()['status']
        reason = r.json()['reason']
        
        return render_template('result.html', title=title,
                               description=description,
                               status=status, reason=reason)
    return render_template('form.html', form=form, title='Delete a room')

@app.route('/rooms', methods={'GET', 'POST'})
def rooms():
    rooms = get_rooms()
    return render_template('rooms.html', rooms=rooms)

@app.route('/bookings', methods={'GET', 'POST'})
def bookings():
    bookings = get_bookings()
    return render_template('bookings.html', bookings=bookings)
