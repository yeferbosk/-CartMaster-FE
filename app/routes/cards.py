from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
import requests
from app.routes.client import client_required
from app.services.api_service import APIService

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_card():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        card_data = {
            'tarjeta_numero': request.form.get('number'),
            'tarjeta_fecha_vencimiento': request.form.get('expiry_date'),
            'tarjeta_franquicia': request.form.get('franchise'),
            'tarjeta_cupo_total': float(request.form.get('total_limit')),
            'tarjeta_cupo_disponible': float(request.form.get('total_limit')),
            'cliente_id': current_user.id
        }
        
        try:
            response = requests.post(
                f"{current_app.config['BACKEND_URL']}/api/tarjetas",
                json=card_data
            )
            
            if response.status_code == 201:
                flash('Card added successfully!', 'success')
                return redirect(url_for('client.dashboard'))
            else:
                flash('Error adding card', 'error')
        except requests.exceptions.RequestException:
            flash('Error connecting to the server', 'error')
            
    return render_template('cards/new.html')

@bp.route('/<int:card_id>')
@login_required
def card_details(card_id):
    try:
        response = requests.get(
            f"{current_app.config['BACKEND_URL']}/api/tarjetas/{card_id}"
        )
        
        if response.status_code == 200:
            card_data = response.json()
            if card_data['cliente_id'] != current_user.id and not current_user.is_admin:
                flash('Unauthorized access', 'error')
                return redirect(url_for('client.dashboard'))
            return render_template('cards/details.html', card=card_data)
        else:
            flash('Error loading card details', 'error')
            return redirect(url_for('client.dashboard'))
    except requests.exceptions.RequestException:
        flash('Error connecting to the server', 'error')
        return redirect(url_for('client.dashboard'))

@bp.route('/<int:card_id>/status', methods=['POST'])
@login_required
def update_card_status(card_id):
    if not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('client.dashboard'))
        
    new_status = request.form.get('status')
    
    try:
        response = requests.patch(
            f"{current_app.config['BACKEND_URL']}/api/tarjetas/{card_id}/estado",
            json={'estado': new_status}
        )
        
        if response.status_code == 200:
            flash('Card status updated successfully!', 'success')
        else:
            flash('Error updating card status', 'error')
    except requests.exceptions.RequestException:
        flash('Error connecting to the server', 'error')
        
    return redirect(url_for('cards.card_details', card_id=card_id))

@bp.route('/mis-tarjetas')
@client_required
def mis_tarjetas():
    try:
        # Obtener las tarjetas del cliente usando su email
        cards = APIService.get_client_cards(current_user.email)
        return render_template('cards/mis_tarjetas.html', cards=cards)
    except Exception as e:
        flash(f'Error al cargar las tarjetas: {str(e)}', 'danger')
        return render_template('cards/mis_tarjetas.html', cards=[]) 