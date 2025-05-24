from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, role):
        self.email = email
        self.role = role
        self.id = email  # Usando el email como ID único
        self.nombre = None  # Añadido para almacenar el nombre del usuario
        self.client_id = None  # Añadido para almacenar el ID del cliente

    @property
    def is_admin(self):
        return self.role == 'ADMINISTRADOR'

    @property
    def is_client(self):
        return self.role == 'CLIENTE'

    @staticmethod
    def get(user_id):
        # Este método es requerido por Flask-Login
        # En este caso, simplemente devolvemos un usuario con el email como ID
        # ya que no estamos almacenando usuarios en una base de datos local
        return User(user_id, None)

    @staticmethod
    def get_default_admin():
        # Devolver un administrador por defecto para desarrollo
        return User(
            email="admin@cartmaster.com",
            role="ADMINISTRADOR"
        )

    @staticmethod
    def from_json(json_data):
        user = User(
            email=json_data.get('email'),
            role=json_data.get('role', 'CLIENTE')
        )
        user.nombre = json_data.get('nombre')
        user.client_id = json_data.get('client_id')  # Añadido para manejar el ID del cliente
        return user

class Card:
    def __init__(self, id, number, expiry_date, franchise, status, total_limit, available_limit, used_limit, client_id):
        self.id = id
        self.number = number
        self.expiry_date = expiry_date
        self.franchise = franchise
        self.status = status
        self.total_limit = total_limit
        self.available_limit = available_limit
        self.used_limit = used_limit
        self.client_id = client_id

    @staticmethod
    def from_json(json_data):
        return Card(
            id=json_data['tarjeta_id'],
            number=json_data['tarjeta_numero'],
            expiry_date=json_data['tarjeta_fecha_vencimiento'],
            franchise=json_data['tarjeta_franquicia'],
            status=json_data['tarjeta_estado'],
            total_limit=float(json_data['tarjeta_cupo_total']),
            available_limit=float(json_data['tarjeta_cupo_disponible']),
            used_limit=float(json_data['tarjeta_cupo_utilizado']),
            client_id=json_data['cliente_id']
        ) 