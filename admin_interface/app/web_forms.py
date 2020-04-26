from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

class NewRoomForm(FlaskForm):
    room_type = StringField('Room type', validators=[DataRequired()], render_kw={"placeholder": "Enter the room type"})
    capacity = StringField('Capacity', validators=[DataRequired()], render_kw={"placeholder": "Enter the room capacity"})
    bathroom = BooleanField('Room has bathroom')
    balcony = BooleanField('Room has balcony')
    price = StringField('Price per night', validators=[DataRequired()], render_kw={"placeholder": "Enter the room price per night"})
    submit = SubmitField('Add room')

class DeleteRoomForm(FlaskForm):
    room = SelectField('Room')
    submit = SubmitField('Delete room')

class DeleteBookingForm(FlaskForm):
    booking = SelectField('Booking')
    submit = SubmitField('Delete booking')