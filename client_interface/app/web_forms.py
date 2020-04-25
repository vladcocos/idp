from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, MultipleFileField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email

class BookingForm(FlaskForm):
    room = SelectField('Room')
    first_name = StringField('First name', validators=[DataRequired()], render_kw={"placeholder": "Enter your first name"})
    last_name = StringField('Last name', validators=[DataRequired()], render_kw={"placeholder": "Enter your last name"})
    check_in = DateField('Check-in date', format='%Y-%m-%d')
    check_out = DateField('Check-out date', format='%Y-%m-%d')
    submit = SubmitField('Book the room')
