from flask import Blueprint, render_template, current_app, flash, redirect, url_for, session
from flask_login import login_required, current_user
import requests
from app.models import Card
from app.services.api_service import APIService
from functools import wraps

bp = Blueprint('client', __name__, url_prefix='/client')

def client_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        try:
            if not current_user.is_authenticated:
                flash('Por favor inicie sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not current_user.role:
                # Si no hay rol, intentar recuperarlo de la sesión
                current_user.role = session.get('user_role')
            
            if not current_user.is_client:
                flash('Acceso denegado. Se requiere una cuenta de cliente.', 'danger')
                return redirect(url_for('auth.login'))
                
            return f(*args, **kwargs)
        except Exception as e:
            flash('Error de autenticación. Por favor inicie sesión nuevamente.', 'danger')
            session.clear()
            return redirect(url_for('auth.login'))
    return decorated_function

@bp.route('/dashboard')
@client_required
def dashboard():
    try:
        # Obtener el ID del cliente de la sesión
        client_id = session.get('client_id')
        if not client_id:
            flash('Error: No se pudo identificar el cliente.', 'danger')
            return redirect(url_for('auth.login'))

        # Obtener las tarjetas del cliente usando su ID
        cards = APIService.get_client_cards(client_id)
        return render_template('client/dashboard.html', cards=cards)
    except Exception as e:
        flash(f'Error al cargar las tarjetas: {str(e)}', 'danger')
        return render_template('client/dashboard.html', cards=[])

@bp.route('/profile')
@login_required
def profile():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
        
    try:
        response = requests.get(
            f"{current_app.config['BACKEND_URL']}/api/clientes/{current_user.id}"
        )
        
        if response.status_code == 200:
            client_data = response.json()
            return render_template('client/profile.html', client=client_data)
        else:
            flash('Error loading profile', 'error')
            return render_template('client/profile.html')
            
    except requests.exceptions.RequestException:
        flash('Error connecting to the server', 'error')
        return render_template('client/profile.html') 