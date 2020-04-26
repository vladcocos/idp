from flask import render_template, flash, redirect, request, session
from app import app
from app.web_forms import *
from datetime import date
import requests
import os
import json

DB_ADAPTER_URL = 'http://0.0.0.0:32500'

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
    
def get_rooms():
    r = requests.get(DB_ADAPTER_URL + '/rooms')
    rooms = r.json()['rooms']
    for room in rooms:
        room[3] = get_bool_string_from_int(room[3])
        room[4] = get_bool_string_from_int(room[4])
        room[-1] = '%d lei' % room[-1]
        current_rooms[room[0]] = room
    return rooms
    
def get_room_ids():
    rooms = get_rooms()
    result = [('0', 'Select a room')]
    for room in rooms:
        room_id = room[0]
        room_type = room[1]
        room_price = room[-1]
        result.append((str(room_id), room_type + ' (' + str(room_id) + ') - ' + str(room_price)))
    return result

def correct_dates(check_in, check_out):
    today = date.today()
    if check_in >= check_out or check_in < today or check_out < today:
        return False
    return True

@app.route('/rooms', methods={'GET', 'POST'})
def rooms():
    rooms = get_rooms()
    return render_template('rooms.html', rooms=rooms)

@app.route('/book_room', methods={'GET', 'POST'})
def book_room():
    form = BookingForm()
    form.room.choices = get_room_ids()

    if form.validate_on_submit() and correct_dates(form.check_in.data, form.check_out.data):
        room_id = form.room.data
        payload = {'room_id': form.room.data,
                   'first_name': form.first_name.data,
                   'last_name': form.last_name.data,
                   'check_in': form.check_in.data,
                   'check_out': form.check_out.data}
        header = {"Content-Type":"application/json"}
        r = session.post(DB_ADAPTER_URL + '/book_room', headers=header, data=payload)

        title = 'Booking result'
        description = 'Your booking for %s between %s and %s' % (current_rooms[int(room_id)][1],
                                                    form.check_in.data.strftime('%d %b %Y'),
                                                    form.check_out.data.strftime('%d %b %Y'))
        status = r.json()['status']
        reason = r.json()['reason']

        return render_template('result.html', title=title,
                               description=description,
                               status=status, reason=reason)
    return render_template('book_room.html', form=form)
