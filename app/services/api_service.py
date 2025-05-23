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
            
            role = response.text.strip()
            return {
                'role': role,
                'nombre': email,
                'email': email
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
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            raise Exception(f"Error al obtener tarjeta {card_id}: {str(e)}")

    @staticmethod
    def get_client_cards(client_id: int) -> List[Dict]:
        """Obtiene todas las tarjetas de un cliente específico"""
        try:
            response = requests.get(f"{APIService.get_base_url()}/api/tarjetas/cliente/{client_id}")
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
                    "tarjetaEstado": data.get("tarjetaEstado"),
                    "tarjetaCupoTotal": data.get("tarjetaCupoTotal"),
                    "tarjetaCupoDisponible": data.get("tarjetaCupoDisponible")
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

    # Endpoints de Clientes

    @staticmethod
    def get_all_clients() -> List[Dict]:
        """Obtiene todos los clientes"""
        try:
            response = requests.get(f"{APIService.get_base_url()}/clientes/lista")
            if response.status_code == 200:
                return response.json()
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