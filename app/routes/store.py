from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_required, current_user
import os
import random
from app.services.api_service import APIService
from app.routes.client import client_required

bp = Blueprint('store', __name__, url_prefix='/store')

def get_products():
    """Obtiene la lista de productos con sus precios"""
    img_folder = os.path.join(current_app.static_folder, 'img')
    products = []
    product_id = 1

    for filename in os.listdir(img_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # Generar un precio aleatorio entre 1,500,000 y 5,000,000 COP
            price = random.uniform(1500000, 5000000)
            
            # Obtener el nombre del producto del archivo
            name = filename.split('.')[0].replace('_', ' ').title()
            
            products.append({
                'id': product_id,
                'name': name,
                'image': filename,
                'price': price
            })
            product_id += 1
    
    return products

@bp.route('/')
@client_required
def store():
    """Vista principal de la tienda"""
    try:
        # Obtener el ID del cliente de la sesión
        client_id = session.get('client_id')
        if not client_id:
            flash('Error: No se pudo identificar el cliente.', 'danger')
            return redirect(url_for('client.dashboard'))

        # Obtener las tarjetas del cliente
        cards = APIService.get_client_cards(client_id)
        
        # Obtener los productos
        products = get_products()
        
        return render_template('store/store.html', products=products, cards=cards)
    except Exception as e:
        flash(f'Error al cargar la tienda: {str(e)}', 'danger')
        return redirect(url_for('client.dashboard'))

@bp.route('/purchase', methods=['POST'])
@client_required
def purchase():
    """Procesa la compra de un producto"""
    try:
        card_id = request.form.get('card_id')
        product_price = float(request.form.get('product_price'))
        
        if not card_id or not product_price:
            flash('Error: Datos de compra incompletos.', 'danger')
            return redirect(url_for('store.store'))
        
        # Obtener la tarjeta
        card = APIService.get_card(card_id)
        if not card:
            flash('Error: Tarjeta no encontrada.', 'danger')
            return redirect(url_for('store.store'))
        
        # Verificar cupo disponible
        available_limit = float(card['tarjetaCupoDisponible'])
        if available_limit < product_price:
            flash('Error: Cupo insuficiente en la tarjeta seleccionada.', 'danger')
            return redirect(url_for('store.store'))
        
        # Calcular nuevo cupo disponible
        new_available_limit = available_limit - product_price
        
        # Actualizar cupo disponible
        result = APIService.update_card_available_limit(card_id, new_available_limit)
        if result:
            flash('¡Compra realizada exitosamente!', 'success')
        else:
            flash('Error al procesar la compra. Por favor intente nuevamente.', 'danger')
        
        return redirect(url_for('store.store'))
    except Exception as e:
        flash(f'Error al procesar la compra: {str(e)}', 'danger')
        return redirect(url_for('store.store')) 