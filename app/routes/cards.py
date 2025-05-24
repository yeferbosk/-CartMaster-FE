from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_required, current_user
import requests
from app.routes.client import client_required
from app.services.api_service import APIService

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.route('/new', methods=['GET', 'POST'])
@client_required
def new_card():
    if request.method == 'POST':
        try:
            # Obtener el ID del cliente de la sesión
            client_id = session.get('client_id')
            if not client_id:
                flash('Error: No se pudo identificar el cliente.', 'danger')
                return redirect(url_for('client.dashboard'))

            card_data = {
                'numero': request.form.get('numero'),
                'fecha_vencimiento': request.form.get('fecha_vencimiento'),
                'franquicia': request.form.get('franquicia'),
                'cupo_total': request.form.get('cupo_total')
            }

            # Validar datos requeridos
            if not all(card_data.values()):
                flash('Por favor complete todos los campos requeridos.', 'danger')
                return render_template('cards/new.html')

            # Intentar crear la tarjeta
            result = APIService.create_card(client_id, card_data)
            if result:
                flash('Tarjeta agregada exitosamente.', 'success')
                # Obtener el ID de la tarjeta creada del resultado
                new_card_id = result.get('tarjetaId')
                if new_card_id:
                    # Redirigir a la vista de detalles de la tarjeta
                    return redirect(url_for('cards.card_details', card_id=new_card_id))
                else:
                    # Si no hay ID, redirigir a la lista de tarjetas
                    return redirect(url_for('cards.mis_tarjetas'))
            else:
                flash('Error al crear la tarjeta. Por favor intente nuevamente.', 'danger')
                return render_template('cards/new.html')

        except Exception as e:
            flash(f'Error al crear la tarjeta: {str(e)}', 'danger')
            return render_template('cards/new.html')

    return render_template('cards/new.html')

@bp.route('/<int:card_id>')
@client_required
def card_details(card_id):
    try:
        # Obtener el ID del cliente de la sesión
        client_id = session.get('client_id')
        if not client_id:
            flash('Error: No se pudo identificar el cliente.', 'danger')
            return redirect(url_for('client.dashboard'))

        # Obtener los detalles de la tarjeta
        card = APIService.get_card(card_id)
        
        if not card:
            flash('No se encontró la tarjeta solicitada.', 'danger')
            return redirect(url_for('client.dashboard'))

        return render_template('cards/card_view.html', card=card)
    except Exception as e:
        flash(f'Error al cargar los detalles de la tarjeta: {str(e)}', 'danger')
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
        # Obtener el ID del cliente de la sesión
        client_id = session.get('client_id')
        if not client_id:
            flash('Error: No se pudo identificar el cliente.', 'danger')
            return redirect(url_for('client.dashboard'))

        # Obtener las tarjetas del cliente usando su ID
        cards = APIService.get_client_cards(client_id)
        return render_template('cards/mis_tarjetas.html', cards=cards)
    except Exception as e:
        flash(f'Error al cargar las tarjetas: {str(e)}', 'danger')
        return render_template('cards/mis_tarjetas.html', cards=[])

@bp.route('/<int:card_id>/edit', methods=['GET', 'POST'])
@client_required
def edit_card(card_id):
    try:
        # Obtener el ID del cliente de la sesión
        client_id = session.get('client_id')
        if not client_id:
            flash('Error: No se pudo identificar el cliente.', 'danger')
            return redirect(url_for('client.dashboard'))

        # Obtener los detalles de la tarjeta
        card = APIService.get_card(card_id)
        
        if not card:
            flash('No se encontró la tarjeta solicitada.', 'danger')
            return redirect(url_for('client.dashboard'))

        if request.method == 'POST':
            card_data = {
                'numero': request.form.get('numero'),
                'fecha_vencimiento': request.form.get('fecha_vencimiento'),
                'franquicia': request.form.get('franquicia'),
                'estado': request.form.get('estado')
            }

            # Validar datos requeridos
            if not all(card_data.values()):
                flash('Por favor complete todos los campos requeridos.', 'danger')
                return render_template('cards/edit.html', card=card)

            # Intentar actualizar la tarjeta
            result = APIService.update_card_general(card_id, card_data)
            if result:
                flash('Tarjeta actualizada exitosamente.', 'success')
                return redirect(url_for('cards.card_details', card_id=card_id))
            else:
                flash('Error al actualizar la tarjeta. Por favor intente nuevamente.', 'danger')
                return render_template('cards/edit.html', card=card)

        return render_template('cards/edit.html', card=card)
    except Exception as e:
        flash(f'Error al editar la tarjeta: {str(e)}', 'danger')
        return redirect(url_for('cards.card_details', card_id=card_id))

@bp.route('/<int:card_id>/deactivate', methods=['POST'])
@client_required
def deactivate_card(card_id):
    try:
        # Obtener el ID del cliente de la sesión
        client_id = session.get('client_id')
        if not client_id:
            flash('Error: No se pudo identificar el cliente.', 'danger')
            return redirect(url_for('client.dashboard'))

        # Intentar desactivar la tarjeta
        if APIService.deactivate_card(card_id):
            flash('Tarjeta desactivada exitosamente.', 'success')
        else:
            flash('Error al desactivar la tarjeta.', 'danger')

        # Redirigir a la página anterior
        return redirect(request.referrer or url_for('client.dashboard'))
    except Exception as e:
        flash(f'Error al desactivar la tarjeta: {str(e)}', 'danger')
        return redirect(url_for('client.dashboard')) 