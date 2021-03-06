from ConfigParser import SafeConfigParser
settings = SafeConfigParser()
settings.read('/home/bakit/CP/food-delivery/logic/settings.cfg')

cli_url = settings.get('ClientBackend', 'URL') + settings.get('ClientBackend', 'PORT')
restr_url = settings.get('RestaurantBackend', 'URL') + settings.get('RestaurantBackend', 'PORT')
auth_url = settings.get('AuthBackend', 'URL') + settings.get('AuthBackend', 'PORT')

import requests
import json

JSON_HEADER = {'Content-Type' : 'application/json'}

##############################################################
##############################################################
############################AUTH

def auth_register(email, password, role='Client'):
	api_url = auth_url + '/auth/register'
	r = requests.post(api_url, \
		data=json.dumps({'email':email, 'password':password,'role':role}), headers=JSON_HEADER)
	if r.status_code == 201:
		flag = True
	else:
		flag = False
	return flag, json.loads(r.text)

def auth_login(email, password):
	api_url = auth_url + '/auth/login'
	r = requests.get(api_url, params={'email':email, 'password':password})
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def auth_user_info(user_id):
	api_url = auth_url + '/auth/user/info'
	r = requests.get(api_url, params={'user_id':user_id})
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def auth_logout(session_id):
	api_url = auth_url + '/auth/logout'
	r = requests.get(api_url, params={'session_id':session_id})
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def auth_session_state(session_id):
	api_url = auth_url + '/auth/session/state'
	r = requests.get(api_url, params={'session_id':session_id})
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def auth_upassw_update(user_id, password, new_password):
	api_url = auth_url + '/auth/user/password/update'
	r = requests.put(api_url, \
		data=json.dumps({'user_id':user_id,'password':password, 'new_password':new_password}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def auth_uemail_update(user_id, email):
	api_url = auth_url + '/auth/user/email/update'
	r = requests.put(api_url, \
		data=json.dumps({'email':email,'user_id':user_id}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def auth_user_delete(session_id, email, password):
	api_url = auth_url + '/auth/user/delete'
	r = requests.delete(api_url, \
		data=json.dumps({'email':email, 'password':password, 'new_password':new_password}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def auth_user_raw_delete(user_id):
	api_url = auth_url + '/auth/user/raw_delete'
	r = requests.delete(api_url, params={'user_id':user_id})
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

##############################################################
##############################################################
############################CLIENTS

def cli_register(user_id, name, telephone):
	api_url = cli_url + '/client/register'
	r = requests.post(api_url, \
		data = json.dumps({'name':name, 'user_id':user_id, 'telephone':telephone}), headers=JSON_HEADER)
	if r.status_code == 201: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def cli_update(user_id, name, telephone):
	api_url = cli_url + '/client/data/update'
	r = requests.put(api_url, \
		data = json.dumps({'name':name, 'user_id':user_id, 'telephone':telephone}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def cli_delete(user_id):
	api_url = cli_url + '/client/delete'
	r = requests.delete(api_url, \
		data = json.dumps({'user_id':user_id}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def cli_info(user_id):
	api_url = cli_url + '/client/info'
	r = requests.get(api_url, params={'user_id':user_id})
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def cli_address_create(user_id, city, street, station=None, entrance=None, passcode=None,floor=None):
	api_url = cli_url + '/client/address/create'
	r = requests.post(api_url, \
		data=json.dumps({'user_id':user_id, 'city':city, 'street':street, 'station':station, \
				'entrance':entrance, 'passcode':passcode, 'floor':floor}), headers=JSON_HEADER)
	if r.status_code == 201: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def cli_address_update(address_id, city, street, station=None, entrance=None, passcode=None,floor=None):
	api_url = cli_url + '/client/address/update'
	r = requests.put(api_url, \
		data=json.dumps({'address_id':address_id, 'city':city, 'street':street, 'station':station, \
				'entrance':entrance, 'passcode':passcode, 'floor':floor}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def cli_address_delete(address_id):
	api_url = cli_url + '/client/address/delete'
	r = requests.delete(api_url, data=json.dumps({'address_id':address_id}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def cli_address_list(user_id):
	api_url = cli_url + '/client/address/list'
	r = requests.get(api_url, params={'user_id':user_id})
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

##############################################################
##############################################################
############################RESTAURANTS
def restr_get_cities(real_city=False):
	api_url = restr_url + '/restaurant/cities/list'
	r = requests.get(api_url, data=json.dumps({'real_city':real_city}), headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restr_get_cuisines(city=None):
	api_url = restr_url + '/restaurant/cuisines/list'
	if city is not None: r = requests.get(api_url, params={'city':city})
	else: r = requests.get(api_url)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restr_register(user_id, name, email, telephone):
	api_url = restr_url + '/restaurant/register'
	r = requests.post(api_url,\
		data=json.dumps({'name':name, 'email':email, 'user_id':user_id,'telephone':telephone}),headers=JSON_HEADER)
	if r.status_code == 201: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restr_cuisines_add(restaurant_id, cuisines):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/cuisines/add'
	r = requests.post(api_url, data=json.dumps({'cuisines':cuisines}),headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restr_cuisines_delete(restaurant_id, cuisines):
	api_url = restr_url + '/restaurant/cuisine/list/'+str(restaurant_id)+'/delete'
	r = requests.delete(api_url, data=json.dumps({'cuisines':cuisines}),headers=JSON_HEADER)
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restr_attributes_create(restaurant_id, open_from, open_to, min_payment, delivery_payment, delivery_time, wdays, online_payment):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/attributes/create'
	r = requests.post(api_url, \
			data=json.dumps({'open_from':open_from,'open_to':open_to,'min_payment':min_payment,\
				'delivery_payment':delivery_payment,'delivery_time':delivery_time,\
				'wdays':wdays,'online_payment':online_payment}),\
			headers=JSON_HEADER)
	if r.status_code == 201: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restr_address_create(restaurant_id, city, street, telephone, station=None):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/address/create'
	r = requests.post(api_url, data=json.dumps({'city':city,'street':street, 'station':station, 'telephone':telephone}),\
				headers=JSON_HEADER)
	if r.status_code == 201: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restr_officials_create(restaurant_id, name, email, telephone, info=None):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/officials/create'
	r = requests.post(api_url, data=json.dumps({'name':name,'email':email, 'telephone':telephone, 'info':info}),\
				headers=JSON_HEADER)
	if r.status_code == 201: flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restr_delete(user_id):
	api_url = restr_url + '/restaurant/delete'
	r = requests.delete(api_url, params={'user_id':user_id})
	if r.status_code == 200: flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_info(user_id=None, restaurant_id=None):
	api_url = restr_url + '/restaurant/info'
	r = requests.get(api_url, params={'user_id':user_id, 'restaurant_id':restaurant_id})
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_update(restaurant_id, email, telephone, name):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/update'
	r = requests.put(api_url, data=json.dumps({'email':email, 'name':name, 'telephone':telephone}), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_address_list(restaurant_id):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/address/list'
	r = requests.get(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_address_update(restaurant_id, address_id, data):
	api_url = restr_url + '/restaurant/' + str(restaurant_id)+ '/address/' + str(address_id) + '/update'
	r = requests.put(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_officials_list(restaurant_id):
	api_url = restr_url + '/restaurant/'+ str(restaurant_id) + '/officials/list'
	r = requests.get(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_officials_update(officials_id, data):
	api_url = restr_url + '/restaurant/officials/'+str(officials_id)+'/update'
	r = requests.put(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_attributes(restaurant_id):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/attributes'
	r = requests.get(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_attributes_update(attribute_id, open_from, open_to, min_payment, delivery_payment, delivery_time, online_payment, wdays):
	api_url = restr_url + '/restaurant/attributes/'+str(attribute_id)+'/update'
	r = requests.put(api_url, data=json.dumps({'open_from':open_from, 'open_to':open_to, 'min_payment':min_payment, 'wdays':wdays,\
			'delivery_payment':delivery_payment,'delivery_time':delivery_time, 'online_payment':online_payment}),\
							headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_menu(restaurant_id):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/menu'
	r = requests.get(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_menu_delete(restaurant_id, menu_id, menu_item_id):
	api_url = restr_url + '/restaurant/'+str(restaurant_id)+'/menu/'+str(menu_id)+'/menu_item/'+str(menu_item_id)+'/delete'
	r = requests.delete(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_menu_item_create(restaurant_id, menu_id, data):
	api_url = restr_url + '/restaurant/'+str(restaurant_id)+'/menu/'+str(menu_id)+'/menu_item/create'
	r = requests.post(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 201:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_menu_update(restaurant_id, menu_id, menu_item_id, data):
	api_url = restr_url + '/restaurant/'+str(restaurant_id)+'/menu/'+str(menu_id)+'/menu_item/'+str(menu_item_id)+'/update'
	r = requests.put(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_cities_add(city):
	api_url = restr_url + '/restaurant/cities/add'
	r = requests.post(api_url, data=json.dumps({'city':city}), headers=JSON_HEADER)
	if r.status_code == 201:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurants_by_preferences(data):
	api_url = restr_url + '/restaurant/list/by_preferences'
	r = requests.get(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_order_confirm(restaurant_id, data):
	api_url = restr_url + '/restaurant/' + str(restaurant_id) + '/order/confirmation'
	r = requests.post(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 201:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_client_history(user_id):
	api_url = restr_url + '/restaurant/client/history'
	r = requests.get(api_url, params={'user_id':user_id})
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)



def restaurant_history(data):
	api_url = restr_url + '/restaurant/history'
	r = requests.get(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_order_status_change(restaurant_id, order_id, status_type):
	api_url = restr_url + '/restaurant/'+str(restaurant_id)+'/order/'+str(order_id)+'/status/change'
	r = requests.put(api_url, params={'status_type':status_type})
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def auth_users_by_role(role_name):
	api_url = auth_url + '/user/list/' + role_name
	r = requests.get(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def client_list():
	api_url = cli_url + '/client/list'
	r = requests.get(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_list(activated):
	api_url = restr_url + '/restaurant/list'
	r = requests.get(api_url,data=json.dumps({'activated':activated}), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_activated_change(restaurant_id):
	api_url = restr_url + '/restaurant/'+str(restaurant_id)+'/activated/change'
	r = requests.get(api_url)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def client_add_points(user_id, points):
	api_url = cli_url + '/client/add/points'
	r = requests.put(api_url, data=json.dumps({'user_id':user_id, 'points':points}), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)

def restaurant_cuisine_create(title):
	api_url = restr_url + '/restaurant/cuisine/create'
	r = requests.post(api_url, data=json.dumps({'title':title}), headers=JSON_HEADER)
	if r.status_code == 201:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)


def restaurant_attributes_add_delete(data):
	api_url = restr_url + '/restaurant/additional/attributes/delete'
	r = requests.delete(api_url, data=json.dumps(data), headers=JSON_HEADER)
	if r.status_code == 200:
		flag = True
	else: flag = False
	return flag, json.loads(r.text)
