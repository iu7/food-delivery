from datetime import datetime, timedelta
from flask import request, jsonify
from . import main
from .. import db, store
from .. exceptions import UException
from .. models import User
from uuid import uuid4

SESSION_LIFETIME = timedelta(days=1)

def create_session_id():
	return unicode(uuid4())

@main.route('/')
def index():
	return ''

@main.route('/auth/register', methods=['POST'])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	role = request.json.get('role')
	try:
		user = User(email, password, role)
		db.session.add(user)
		db.session.commit()
	except ValueError as error:
		raise UException(message=error.message)
	except Exception as exc:
		raise UException(message='Unexpected server exception', status_code=500, payload=exc.message)
	return jsonify(status='created', email=user.email, user_id=user.id), 201

@main.route('/auth/user/info')
def auth_user_info():
	user_id = request.args.get('user_id')
	if not user_id:
		raise UException('Incorrect user_id')
	user = User.query.filter_by(id=user_id).first()
	if not user:
		raise UException(message='Unexpected server exception', status_code=500, payload='Could not find user')
	return jsonify(email=user.email, user_id=user.id, role=user.get_role_name())

@main.route('/auth/login')
def login():
	email = request.args.get('email')
	password = request.args.get('password')
	user = User.query.filter_by(email=email).first()
	if not user:
		raise UException(message='Incorrect email or password', payload='User with email: %s was not found'%email)
	if not user.verify_password(password):
		raise UException(message='Incorrect email or password', payload='Incorrect password')
	session_id = create_session_id()
	store[session_id] = {'user_id' : user.id, 'created' : datetime.utcnow()}
	return jsonify(session_id=session_id, user_id=user.id, role=user.get_role_name())

@main.route('/auth/logout')
def logout():
	session_id = request.args.get('session_id')
	if not session_id:
		raise UException(message='Incorrect request: session_id is required')
	s = store.get(session_id)
	if not s:
		raise UException(message='Incorrect session_id')
	store.pop(session_id)
	return jsonify(logout=True)

@main.route('/auth/session/state')
def session_state():
	session_id = request.args.get('session_id')
	if not session_id:
		raise UException(message='Incorrect request')
	s = store.get(session_id)
	if not s:
		raise UException(message='Incorrect session_id')
	expired = False
	uid = s['user_id']
	role = None
	if datetime.utcnow() - s['created'] >= SESSION_LIFETIME:
		store.pop(session_id)
		expired = True
	else:
		email = None
		user = User.query.filter_by(id=uid).first()
		if user:
			role = user.get_role_name()
			email = user.email
	return jsonify(session_id=session_id, expired=expired, user_id=uid, role=role, email=email)

@main.route('/auth/user/password/update', methods=['PUT'])
def password_update():
	user_id = request.json.get('user_id')
	#email = request.json.get('email')
	password = request.json.get('password')
	new_password = request.json.get('new_password')
	user = User.query.filter_by(id=user_id).first()
	if not user:
		raise UException(message='Incorrect user_id', payload='User with user_id: %d was not found'%user_id)
	if not user.verify_password(password):
		raise UException(message='Incorrect password', payload='Incorrect password')
	try:
		user.password_hash = new_password
		db.session.commit()
	except ValueError as error:
		raise UException(message=error.message)
	except Exception as exc:
		raise UException(message='Unexpected server exception', status_code=500, payload=exc.message)
	return jsonify(status='updated', email=user.email, user_id=user.id)


@main.route('/auth/user/email/update', methods=['PUT'])
def email_update():
	user_id = request.json.get('user_id')
	#email = request.json.get('email')
	#password = request.json.get('password')
	email = request.json.get('email')
	user = User.query.filter_by(id=user_id).first()
	if not user:
		raise UException(message='Incorrect user_id or password', payload='User with email: %s was not found'%email)
	#if not user.verify_password(password):
	#	raise UException(message='Incorrect email or password', payload='Incorrect password')
	try:
		user.email = email
		db.session.commit()
	except ValueError as error:
		raise UException(message=error.message)
	except Exception as exc:
		raise UException(message='Unexpected server exception', status_code=500, payload=exc.message)
	return jsonify(status='updated', email=user.email, user_id=user.id)


@main.route('/auth/user/delete', methods=['DELETE'])
def user_delete():
	email = request.json.get('email')
	password = request.json.get('password')
	session_id = request.json.get('session_id')
	if not session_id:
		raise UException(message='Incorrect query: session_id is required')
	s = store.get(session_id)
	if not s:
		raise UException(message='Incorrect session_id')
	user = User.query.filter_by(email=email).first()
	if not user:
		raise UException(message='Incorrect email or password', payload='User with email: %s was not found'%email)
	if not user.verify_password(password):
		raise UException(message='Incorrect email or password', payload='Incorrect password')
	try:
		db.session.delete(user)
		db.session.commit()
		store.pop(session_id)
	except:
		raise UException(message='Unexpected server exception', status_code=500)
	return jsonify(status='deleted')

@main.route('/auth/user/raw_delete', methods=['DELETE'])
def user_raw_delete():
	user_id = request.args.get('user_id')
	user = User.query.filter_by(id=user_id).first()
	if not user:
		raise UException(message='Incorrect email or password', payload='User with email: %s was not found'%email)
	try:
		db.session.delete(user)
		db.session.commit()
	except:
		raise UException(message='Unexpected server exception', status_code=500)
	return jsonify(status='deleted')


@main.route('/user/list/<role>')
def user_list(role):
	if not role:
		raise UException('Incorrect request')
	users = User.get_users(role)
	return jsonify(users=users)
