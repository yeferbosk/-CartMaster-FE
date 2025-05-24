import requests
from flask import current_app
from typing import Dict, List, Optional, Union

class APIService:
    @staticmethod
    def get_base_url() -> str:
        return current_app.config['BACKEND_URL']

    @staticmethod
    def login(email: str, password: str) -> Optional[Dict]:
        try:
            response = requests.post(
                f"{APIService.get_base_url()}/clientes/login",
                json={
                    "correo": email,
                    "contrasena": password
                }
            )
            
            if response.status_code == 401:
                return None
                
            if not response.text:
                raise ValueError("El servidor devolvió una respuesta vacía")
            
            response_data = response.json() if response.text else {}
            role = response_data.get('tipo', 'CLIENTE')
            client_id = response_data.get('clienteId')  # Puede ser None para administradores
            
            return {
                'role': role,
                'nombre': email,
                'email': email,
                'client_id': client_id  # Incluimos el ID del cliente si existe
            }
            
        except Exception as e:
            raise Exception(f"Error en login: {str(e)}")

    # Endpoints de Tarjetas

    @staticmethod
    def get_all_cards() -> List[Dict]:
        """Obtiene todas las tarjetas"""
        try:
            response = requests.get(f"{APIService.get_base_url()}/api/tarjetas")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            raise Exception(f"Error al obtener tarjetas: {str(e)}")

    @staticmethod
    def get_card(card_id: int) -> Optional[Dict]:
        """Obtiene una tarjeta específica por ID"""
        try:
            response = requests.get(f"{APIService.get_base_url()}/api/tarjetas/{card_id}")
            if response.status_code == 200 and response.text:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                raise Exception(f"Error del servidor: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error al obtener tarjeta {card_id}: {str(e)}")

    @staticmethod
    def get_client_cards(client_id: int) -> List[Dict]:
        """Obtiene todas las tarjetas de un cliente específico usando su ID"""
        try:
            response = requests.get(f"{APIService.get_base_url()}/clientes/{client_id}/tarjetas")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            raise Exception(f"Error al obtener tarjetas del cliente {client_id}: {str(e)}")

    @staticmethod
    def update_card(card_id: int, data: Dict) -> Optional[Dict]:
        """Actualiza los datos de una tarjeta"""
        try:
            response = requests.put(
                f"{APIService.get_base_url()}/api/tarjetas/{card_id}",
                json={
                    "tarjetaEstado": data.get("estado"),
                    "tarjetaCupoTotal": float(data.get("cupo_total")),
                    "tarjetaCupoDisponible": float(data.get("cupo_disponible"))
                }
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            raise Exception(f"Error al actualizar tarjeta {card_id}: {str(e)}")

    @staticmethod
    def delete_card(card_id: int) -> bool:
        """Elimina (inactiva) una tarjeta"""
        try:
            response = requests.delete(f"{APIService.get_base_url()}/api/tarjetas/{card_id}")
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"Error al eliminar tarjeta {card_id}: {str(e)}")

    @staticmethod
    def get_cards_with_clients() -> List[Dict]:
        """Obtiene todas las tarjetas con información de sus clientes"""
        try:
            response = requests.get(f"{APIService.get_base_url()}/api/tarjetas/con-clientes")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            raise Exception(f"Error al obtener tarjetas con clientes: {str(e)}")

    @staticmethod
    def create_card(client_id: int, card_data: Dict) -> Optional[Dict]:
        """Crea una nueva tarjeta para un cliente específico"""
        try:
            response = requests.post(
                f"{APIService.get_base_url()}/api/tarjetas/crear/{client_id}",
                json={
                    "tarjetaNumero": card_data['numero'],
                    "tarjetaFechaVencimiento": card_data['fecha_vencimiento'],
                    "tarjetaFranquicia": card_data['franquicia'],
                    "tarjetaEstado": "ACTIVO",
                    "tarjetaCupoTotal": float(card_data['cupo_total']),
                    "tarjetaCupoDisponible": float(card_data['cupo_total'])  # Inicialmente igual al cupo total
                }
            )
            if response.status_code == 201:
                # Asegurarse de que la respuesta tenga contenido
                if response.text:
                    return response.json()
                else:
                    raise Exception("El servidor no devolvió datos de la tarjeta creada")
            elif response.status_code == 400:
                raise Exception("Datos de tarjeta inválidos")
            elif response.status_code == 404:
                raise Exception("Cliente no encontrado")
            else:
                raise Exception(f"Error del servidor: {response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión al crear tarjeta: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al crear tarjeta: {str(e)}")

    @staticmethod
    def update_card_general(card_id: int, card_data: Dict) -> Optional[Dict]:
        """Actualiza los datos generales de una tarjeta"""
        try:
            response = requests.put(
                f"{APIService.get_base_url()}/api/tarjetas/actualizar_generales/{card_id}",
                json={
                    "tarjetaNumero": card_data['numero'],
                    "tarjetaFechaVencimiento": card_data['fecha_vencimiento'],
                    "tarjetaFranquicia": card_data['franquicia'],
                    "tarjetaEstado": card_data['estado']
                }
            )
            if response.status_code == 200 and response.text:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                raise Exception(f"Error del servidor: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error al actualizar tarjeta {card_id}: {str(e)}")

    @staticmethod
    def deactivate_card(card_id: int) -> bool:
        """Desactiva una tarjeta"""
        try:
            response = requests.delete(f"{APIService.get_base_url()}/api/tarjetas/{card_id}")
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"Error al desactivar la tarjeta {card_id}: {str(e)}")

    @staticmethod
    def update_card_available_limit(card_id: int, available_limit: float) -> Optional[Dict]:
        """Actualiza el cupo disponible de una tarjeta"""
        try:
            response = requests.put(
                f"{APIService.get_base_url()}/api/tarjetas/actualizar_cupo_disponible/{card_id}",
                json={
                    "tarjetaCupoDisponible": available_limit
                }
            )
            if response.status_code == 200 and response.text:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                raise Exception(f"Error del servidor: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error al actualizar cupo de tarjeta {card_id}: {str(e)}")

    # Endpoints de Clientes

    @staticmethod
    def get_all_clients() -> List[Dict]:
        """Obtiene todos los clientes únicos a partir de las tarjetas"""
        try:
            response = requests.get(f"{APIService.get_base_url()}/api/tarjetas/con-clientes")
            if response.status_code == 200:
                # Obtener todas las tarjetas con información de clientes
                cards_data = response.json()
                
                # Crear un diccionario para almacenar clientes únicos por ID
                unique_clients = {}
                
                # Extraer clientes únicos de las tarjetas
                for card in cards_data:
                    if 'cliente' in card:
                        client = card['cliente']
                        client_id = client['id']
                        if client_id not in unique_clients:
                            unique_clients[client_id] = client
                
                # Devolver la lista de clientes únicos
                return list(unique_clients.values())
            return []
        except Exception as e:
            raise Exception(f"Error al obtener clientes: {str(e)}")

    @staticmethod
    def delete_client(client_id: int) -> bool:
        """Elimina un cliente y todas sus tarjetas"""
        try:
            response = requests.delete(f"{APIService.get_base_url()}/clientes/{client_id}")
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"Error al eliminar cliente {client_id}: {str(e)}") 