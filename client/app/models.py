from . import db
from datetime import datetime
from sqlalchemy.orm import validates
import re

class ClientConfig:
	NAME_MIN_LENGTH = 1	
	TELEPHONE_FORMAT = r'((8|\+7)-?)?\(?\d{3}\)?-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}'

class Client(db.Model):
	__tablename__ = 'clients'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False, unique=True)
	name = db.Column(db.String(64), nullable=False)
	telephone = db.Column(db.String(32), nullable=False)	
	member_since = db.Column(db.DateTime(), default=datetime.utcnow())
	points = db.Column(db.Integer, default=0)
	address = db.relationship('Address', cascade='all,delete', backref='client')
	history = db.relationship('History', cascade='all,delete', backref='client')


	@staticmethod
	def get_clients():
		clients = Client.query.all()
		result = []
		for client in clients:
			if client:
				result.append({'user_id':client.user_id, 'name':client.name, 'telephone':client.telephone,\
					'member_since':client.member_since, 'points':client.points})
		return result

	def __init__(self, name, telephone, user_id):
		self.name = name
		self.telephone = telephone
		self.user_id = user_id

	def update_points(self, points):
		value = self.points + points
		if value >= 0:
			self.points = value
		else:
			raise ValueError('Not enough points') 
		return True

	@validates('user_id')
	def validate_user_id(self, key, value):
		if not type(value) is type(int()):
			raise ValueError('Incorrect user_id type: type must be integer')
		if Client.query.filter_by(user_id=value).first():
			raise ValueError('Client with user_id = %d exists' % value)
		return value

	@validates('name')
	def validate_name(self, key, value):
		if len(value) < ClientConfig.NAME_MIN_LENGTH:
			raise ValueError('Incorrect name length: minimal length ' + str(ClientConfig.NAME_MIN_LENGTH) + ' symbol')
		return value

	@validates('telephone')
	def validate_telephone(self, key, value):
		if re.match(ClientConfig.TELEPHONE_FORMAT, value) is None:
			raise ValueError('Incorrect telephone format')
		return value

	@validates('points')
	def validate_telephone(self, key, value):
		if value < 0: value = 0
		return value

	def __repr__(self):
		return '<User: name: %s, email: %s, user_id: %d' % (self.name, self.telephone, self.user_id)


class Address(db.Model):
	__tablename__ = 'address'
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(128), nullable=False)
	station = db.Column(db.String(128))
	street = db.Column(db.String(256), nullable=False)
	entrance = db.Column(db.Integer)
	floor = db.Column(db.Integer)
	passcode = db.Column(db.String(32))
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

	@validates('client_id')
	def validate_client_id(self, key, value):
		if  not Client.query.filter_by(id=value).first():
			raise ValueError('Incorrect client_id')
		return value

	def __init__(self, client_id, city, street, station=None, ent=None, floor=None, passcode=None):
		self.city = city
		self.street = street
		self.station = station
		self.entrance = ent
		self.floor = floor
		self.passcode = passcode
		self.client_id = client_id

	def __repr__(self):
		return '<Address: client_id: %d, city: %s, street: %s' % (self.client_id, self.city, self.street)

class History(db.Model):
	__tablename__ = 'history'
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime(), default=datetime.utcnow())
	order_id = db.Column(db.Integer, unique=True)
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

	def __init__(self, order_id):
		self.order_id = order_id

	def __repr__(self):
		return '<History: id: %d, order_id: %d, datetime: %s>' % (self.id, self.order_id, str(self.datetime))

