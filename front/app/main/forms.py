from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, \
		IntegerField, DecimalField, BooleanField, FloatField, SelectMultipleField,TextAreaField
from wtforms.validators import Required, Email, EqualTo, Length, Regexp, Optional, NumberRange
from wtforms.validators import StopValidation
from datetime import datetime
import copy

TELEPHONE_FORMAT = r'((8|\+7)-?)?\(?\d{3}\)?-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}'

class ClientRegisterForm(Form):
	name = StringField('Name', validators=[Required()])
	email = StringField('Email', validators=[Email()])
	password = PasswordField('Password', validators=[Required(), EqualTo('password_confirm', message='Password must match'), \
				Length(min=6,max=64)])
	password_confirm = PasswordField('Password confirmation')
	telephone = StringField('Telephone', validators=[Regexp(TELEPHONE_FORMAT)])
	#submit = SubmitField('Register')

class ClientEditForm(Form):
	name = StringField('Name', validators=[Required()])
	email = StringField('Email', validators=[Email()])
	telephone = StringField('Telephone', validators=[Regexp(TELEPHONE_FORMAT)])

class UserPasswordEditForm(Form):
	password = PasswordField('Password', validators=[Required()])
	new_password = PasswordField('New password', validators=[Required(), EqualTo('password_confirm', message='Password must match'), \
				Length(min=6,max=64)])
	password_confirm = PasswordField('Password confirmation')

class AddressForm(Form):
	city = SelectField('City', coerce=unicode)
	street = StringField('Street', validators=[Required()])
	station = StringField('Underground Station',validators=[Optional()])
	entrance = IntegerField('Entrance', validators=[Optional(), ])
	floor = IntegerField('Floor', validators=[Optional()])
	passcode = StringField('Passcode', validators=[Optional()])
	telephone = StringField('Telephone', validators=[Optional(), Regexp(TELEPHONE_FORMAT)])

class RestaurantRegisterForm(Form):
	name = StringField('Restaurant Name', validators=[Required()])
	email = StringField('Email', validators=[Email()])
	password = PasswordField('Password', validators=[Required(), EqualTo('password_confirm', message='Password must match'), \
				Length(min=6,max=64)])
	password_confirm = PasswordField('Password confirmation')
	cuisines = SelectMultipleField('Cuisines', coerce=int)
	monday = BooleanField('Mon.', default=True)
	tuesday = BooleanField('Tue.', default=True)
	wednesday = BooleanField('Wed.', default=True)
	thursday = BooleanField('Thu.', default=True)
	friday = BooleanField('Fri.', default=True)
	saturday = BooleanField('Sat.', default=True)
	sunday =  BooleanField('Sun.', default=True)
	openfrom_h = SelectField('', coerce=unicode, \
			choices=[( str(x)+':', '0'+str(x)) if x <= 9 else ( str(x)+':', str(x)) for x in range(0, 24)])
	openfrom_m = SelectField('', coerce=unicode, \
			choices=[( str(x), '0'+str(x)) if x < 10 else ( str(x), str(x)) for x in range(0, 60, 5)])
	opento_h = SelectField('', coerce=unicode, \
			choices=[( str(x)+':', '0'+str(x)) if x <= 9 else ( str(x)+':', str(x)) for x in range(0, 24)])
	opento_m = SelectField('', coerce=unicode, \
			choices=[( str(x), '0'+str(x)) if x < 10 else ( str(x), str(x)) for x in range(0, 60, 5)])

	min_price = FloatField('Minimum order cost', validators=[NumberRange(min=0)], default=0)
	delivery_payment = FloatField('Delivery cost', validators=[NumberRange(min=0)], default=0)
	delivery_time = SelectField('Average delivery time', coerce=unicode, \
			choices=[(str(x), str(x)+' min.') for x in range(30, 100, 5)] + \
				[('2','2 h.'), ('4','4 h.'),('6', '6 h.'),('12','12 h.'),('24', '24 h.') ])
	online_payment = BooleanField('Online payment')
	city = SelectField('City', coerce=unicode)
	street = StringField('Street', validators=[Required()])
	telephone = StringField('Telephone', validators=[Regexp(TELEPHONE_FORMAT)])

	official_name = StringField('Official name', validators=[Required()])
	official_email = StringField('Official email', validators=[Email()])
	official_telephone = StringField('Official contact telephone', validators=[Regexp(TELEPHONE_FORMAT)])
	order_email = StringField('Email for orders', validators=[Email()])
	info = TextAreaField('Additional information', validators=[Optional(), Length(max=256)])

class RestaurantEditForm(Form):
	name = StringField('Restaurant Name', validators=[Required()])
	email = StringField('Email', validators=[Email()])
	telephone = StringField('Telephone', validators=[Regexp(TELEPHONE_FORMAT)])
	order_email = StringField('Email for orders', validators=[Email()])

class OfficialForm(Form):
	name = StringField('Official name', validators=[Required()])
	email = StringField('Official email', validators=[Email()])
	telephone = StringField('Official contact telephone', validators=[Regexp(TELEPHONE_FORMAT)])
	info = TextAreaField('Additional information', validators=[Optional(), Length(max=256)])

class AttributesForm(Form):
	cuisines = SelectMultipleField('Cuisines', coerce=int)
	cuisines_current = SelectMultipleField('Current cuisines', coerce=int)
	monday = BooleanField('Mon.', default=True)
	tuesday = BooleanField('Tue.', default=True)
	wednesday = BooleanField('Wed.', default=True)
	thursday = BooleanField('Thu.', default=True)
	friday = BooleanField('Fri.', default=True)
	saturday = BooleanField('Sat.', default=True)
	sunday =  BooleanField('Sun.', default=True)
	openfrom_h = SelectField('', coerce=unicode, \
			choices=[( str(x), '0'+str(x)) if x <= 9 else ( str(x), str(x)) for x in range(0, 24)])
	openfrom_m = SelectField('', coerce=unicode, \
			choices=[( str(x), '0'+str(x)) if x < 10 else ( str(x), str(x)) for x in range(0, 60, 5)])
	opento_h = SelectField('', coerce=unicode, \
			choices=[( str(x), '0'+str(x)) if x <= 9 else ( str(x), str(x)) for x in range(0, 24)])
	opento_m = SelectField('', coerce=unicode, \
			choices=[( str(x), '0'+str(x)) if x < 10 else ( str(x), str(x)) for x in range(0, 60, 5)])

	min_price = FloatField('Minimum order cost', validators=[NumberRange(min=0)], default=0)
	delivery_payment = FloatField('Delivery cost', validators=[NumberRange(min=0)], default=0)
	delivery_time = SelectField('Average delivery time', coerce=unicode, \
			choices=[(str(x), str(x)+' min.') for x in range(30, 100, 5)] + \
				[('2','2 h.'), ('4','4 h.'),('6', '6 h.'),('12','12 h.'),('24', '24 h.') ])
	online_payment = BooleanField('Online payment')

class MenuItemForm(Form):
	title = StringField('Title', validators=[Required(), Length(max=64)])
	price = FloatField('Price', validators=[NumberRange(min=0)])
	info = TextAreaField('Comments', validators=[Optional(), Length(max=256)])
	bonus = BooleanField('Bonus', default=False)

class OrderCity(Form):
	cities = SelectField('', coerce=unicode)
	
class OrderAttributes(Form):
	#cuisines = SelectMultipleField('Cuisines', coerce=int)
	min_payment = FloatField('Minimum order cost', validators=[Optional(), NumberRange(min=0)])
	online_payment = BooleanField('Online payment')
	#bonuses = BooleanField('Bonuses')
	opened = BooleanField('Opened now')
	delivery_time = SelectField('Average delivery time', coerce=unicode, default=24,\
			choices=[(str(x), str(x)+' min.') for x in range(30, 120, 30)] + \
				[(str(2*60),'2 h.'), (str(4*60), '4 h.'), (str(12*60), '12 h.'),(str(24*60), '24 h.') ])


class OrderExecution(Form):
	name = StringField('Name', validators=[Required()])
	telephone = StringField('Telephone', validators=[Regexp(TELEPHONE_FORMAT)])
	street = StringField('Street', validators=[Required()])
	station = StringField('Underground Station',validators=[Optional()])
	entrance = IntegerField('Entrance', validators=[Optional(), ])
	floor = IntegerField('Floor', validators=[Optional()])
	passcode = StringField('Passcode', validators=[Optional(), ])
	

class HistoryType(Form):
	status = SelectField('Order status type', coerce=unicode, default=None, choices=[('all', 'All'), ('confirmed', 'Confirmed'),\
				('not confirmed', 'Not confirmed'), ('canceled', 'Canceled')])


class RestaurantStatus(Form):
	status = SelectField('Activation status', coerce=unicode, choices=[('activated', 'Activated'), ('not activated', 'Not activated')])

class AdditionalSettings(Form):
	cuisines = SelectMultipleField('Choose cuisines to delete', coerce=int)
	new_cuisine = StringField('New cuisine', validators=[Optional()])
	cities = SelectMultipleField('Choose cities to delete', coerce=unicode)
	new_city = StringField('New city', validators=[Optional()])










