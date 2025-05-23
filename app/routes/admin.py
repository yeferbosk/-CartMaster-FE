from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from app.decorators import admin_required
from app.services.api_service import APIService

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Datos de ejemplo
MOCK_CLIENTS = [
    {
        'clienteId': 1,
        'clienteNombre': 'Juan Pérez',
        'clienteCorreo': 'juan.perez@example.com',
        'tarjetas': [
            {
                'tarjetaId': 1,
                'tarjetaNumero': '4532111122223333',
                'tarjetaFechaVencimiento': '12/2025',
                'tarjetaFranquicia': 'VISA',
                'tarjetaEstado': 'ACTIVO',
                'tarjetaCupoTotal': 5000000.0,
                'tarjetaCupoDisponible': 3000000.0,
                'tarjetaCupoUtilizado': 2000000.0
            }
        ]
    },
    {
        'clienteId': 2,
        'clienteNombre': 'María López',
        'clienteCorreo': 'maria.lopez@example.com',
        'tarjetas': [
            {
                'tarjetaId': 2,
                'tarjetaNumero': '5412555566667777',
                'tarjetaFechaVencimiento': '03/2026',
                'tarjetaFranquicia': 'MASTERCARD',
                'tarjetaEstado': 'BLOQUEADO',
                'tarjetaCupoTotal': 8000000.0,
                'tarjetaCupoDisponible': 8000000.0,
                'tarjetaCupoUtilizado': 0.0
            },
            {
                'tarjetaId': 3,
                'tarjetaNumero': '4532888899990000',
                'tarjetaFechaVencimiento': '08/2024',
                'tarjetaFranquicia': 'VISA',
                'tarjetaEstado': 'ACTIVO',
                'tarjetaCupoTotal': 3000000.0,
                'tarjetaCupoDisponible': 1500000.0,
                'tarjetaCupoUtilizado': 1500000.0
            }
        ]
    }
]

MOCK_CARDS = []
for client in MOCK_CLIENTS:
    for card in client['tarjetas']:
        card['cliente'] = {
            'clienteId': client['clienteId'],
            'clienteNombre': client['clienteNombre'],
            'clienteCorreo': client['clienteCorreo']
        }
        MOCK_CARDS.append(card)

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    try:
        # Obtener tarjetas con información de clientes
        cards = APIService.get_cards_with_clients()
        
        # Obtener lista de clientes únicos de las tarjetas
        clients = []
        client_ids = set()
        
        for card in cards:
            if card.get('cliente') and card['cliente']['id'] not in client_ids:
                clients.append(card['cliente'])
                client_ids.add(card['cliente']['id'])
        
        return render_template('admin/dashboard.html', cards=cards, clients=clients)
    except Exception as e:
        flash(f'Error al cargar el dashboard: {str(e)}', 'danger')
        return render_template('admin/dashboard.html', cards=[], clients=[])

@bp.route('/clientes')
@login_required
@admin_required
def listar_clientes():
    try:
        clients = APIService.get_all_clients()
        return render_template('admin/clientes.html', clients=clients)
    except Exception as e:
        flash(f'Error al cargar los clientes: {str(e)}', 'danger')
        return render_template('admin/clientes.html', clients=[])

@bp.route('/clientes/<int:client_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_cliente(client_id):
    try:
        APIService.delete_client(client_id)
        flash('Cliente eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el cliente: {str(e)}', 'danger')
    return redirect(url_for('admin.listar_clientes'))

@bp.route('/tarjetas')
@login_required
@admin_required
def listar_tarjetas():
    try:
        cards = APIService.get_cards_with_clients()
        return render_template('admin/tarjetas.html', cards=cards)
    except Exception as e:
        flash(f'Error al cargar las tarjetas: {str(e)}', 'danger')
        return render_template('admin/tarjetas.html', cards=[])

@bp.route('/tarjetas/<int:card_id>')
@login_required
@admin_required
def ver_tarjeta(card_id):
    try:
        card = APIService.get_card(card_id)
        return render_template('admin/tarjeta_detalle.html', card=card)
    except Exception as e:
        flash(f'Error al cargar la tarjeta: {str(e)}', 'danger')
        return redirect(url_for('admin.listar_tarjetas'))

@bp.route('/tarjetas/<int:card_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_tarjeta(card_id):
    if request.method == 'POST':
        try:
            data = {
                'estado': request.form['estado'],
                'cupo_total': float(request.form['cupo_total']),
                'cupo_disponible': float(request.form['cupo_disponible'])
            }
            result = APIService.update_card(card_id, data)
            if result:
                flash('Tarjeta actualizada correctamente', 'success')
            else:
                flash('Error al actualizar la tarjeta', 'danger')
            return redirect(url_for('admin.ver_tarjeta', card_id=card_id))
        except Exception as e:
            flash(f'Error al actualizar la tarjeta: {str(e)}', 'danger')
            return redirect(url_for('admin.ver_tarjeta', card_id=card_id))
    
    try:
        card = APIService.get_card(card_id)
        return render_template('admin/tarjeta_editar.html', card=card)
    except Exception as e:
        flash(f'Error al cargar la tarjeta: {str(e)}', 'danger')
        return redirect(url_for('admin.listar_tarjetas'))

@bp.route('/tarjetas/<int:card_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_tarjeta(card_id):
    try:
        APIService.delete_card(card_id)
        flash('Tarjeta eliminada correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar la tarjeta: {str(e)}', 'danger')
    return redirect(url_for('admin.listar_tarjetas')) 