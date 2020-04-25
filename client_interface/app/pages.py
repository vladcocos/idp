from flask import render_template, flash, redirect, request, session
from app import app
from app.web_forms import *
import requests
import os
import json

SECRET_KEY = 'abcdef'
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

@app.route('/rooms', methods={'GET', 'POST'})
def rooms():
    rooms = get_rooms()
    return render_template('rooms.html', rooms=rooms)

@app.route('/booking', methods={'GET', 'POST'})
def booking():
    form = BookingForm()
    form.room.choices = get_room_ids()

    if request.args and 'room_id' in request.args:
        room_id = request.args.get('room_id')
        form.room.default = request.args['room_id']
        form.process()

    if form.validate_on_submit():
        room_id = form.room.data
        payload = {'room_id': form.room.data,
                   'first_name': form.first_name.data,
                   'last_name': form.last_name.data,
                   'check_in': form.check_in.data,
                   'check_out': form.check_out.data}
        header = {"Content-Type":"application/json"}
        r = session.post(DB_ADAPTER_URL + '/booking', headers=header, data=payload)

        booking_details = '%s between %s and %s' % (current_rooms[int(room_id)][1],
                                                    form.check_in.data.strftime('%d/%m/%Y'),
                                                    form.check_out.data.strftime('%d/%m/%Y'))
        status = 'has failed'
        reason = 'An error has occured.'
        
        if r.status_code == requests.codes.ok:
            status = r.json()['status']
            reason = r.json()['reason']
        
        return render_template('booking_result.html', booking_details=booking_details,
                               status=status, reason=reason)
    return render_template('booking.html', form=form)
