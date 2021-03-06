from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask_wtf.csrf import CsrfProtect
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
csrf = CsrfProtect()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	csrf.init_app(app)

	from main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app
	
