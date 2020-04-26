from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

class BookingForm(FlaskForm):
    room = SelectField('Room')
    first_name = StringField('First name', validators=[DataRequired()], render_kw={"placeholder": "Enter your first name"})
    last_name = StringField('Last name', validators=[DataRequired()], render_kw={"placeholder": "Enter your last name"})
    check_in = DateField('Check-in date', format='%Y-%m-%d')
    check_out = DateField('Check-out date', format='%Y-%m-%d')
    submit = SubmitField('Book the room')
