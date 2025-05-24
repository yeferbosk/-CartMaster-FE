from flask import Flask, redirect, url_for, session, abort
from flask_login import LoginManager, current_user
from flask_moment import Moment
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['BACKEND_URL'] = os.getenv('BACKEND_URL', 'http://localhost:8080')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

moment = Moment(app)

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    try:
        # Recuperar el rol de la sesión
        role = session.get('user_role')
        nombre = session.get('user_nombre')
        user = User(email=user_id, role=role)
        user.nombre = nombre
        return user
    except Exception:
        return None

# Importar blueprints después de crear la aplicación
from app.routes import auth
app.register_blueprint(auth.bp)

from app.routes import admin
app.register_blueprint(admin.bp)

from app.routes import client
app.register_blueprint(client.bp)

from app.routes import cards
app.register_blueprint(cards.bp)

from app.routes import store
app.register_blueprint(store.bp)

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    try:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_client:
            return redirect(url_for('client.dashboard'))
        else:
            # Si el usuario no tiene un rol válido, cerrar sesión
            session.clear()
            return redirect(url_for('auth.login'))
    except Exception as e:
        # Si hay algún error, limpiar la sesión y redirigir al login
        session.clear()
        return redirect(url_for('auth.login')) 