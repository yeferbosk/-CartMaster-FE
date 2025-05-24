from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.services.api_service import APIService

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Por favor ingrese todos los campos', 'danger')
            return render_template('auth/login.html')
        
        try:
            user_data = APIService.login(email, password)
            if user_data:
                user = User.from_json(user_data)
                
                # Guardar datos en la sesión
                session['user_role'] = user.role
                session['user_nombre'] = user.nombre
                session['client_id'] = user.client_id  # Guardamos el ID del cliente en la sesión si existe
                
                login_user(user)
                flash('Inicio de sesión exitoso', 'success')
                
                if user.is_admin:
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('client.dashboard'))
            else:
                flash('Credenciales inválidas', 'danger')
                return render_template('auth/login.html')
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'danger')
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            response = requests.post(
                f"{current_app.config['BACKEND_URL']}/api/clientes",
                json={
                    'cliente_nombre': name,
                    'cliente_correo': email,
                    'cliente_contrasena': password
                }
            )

            if response.status_code == 201:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Registration failed. Please try again.', 'error')
        except requests.exceptions.RequestException:
            flash('Error connecting to the server', 'error')

    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    # Limpiar datos de la sesión
    session.pop('user_role', None)
    session.pop('user_nombre', None)
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login')) 