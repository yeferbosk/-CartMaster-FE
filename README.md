# CartMaster Frontend

Aplicación frontend desarrollada en Flask para la gestión de tarjetas de crédito. Esta aplicación trabaja en conjunto con el backend CartMaster desarrollado en Spring Boot.

## Características

- Autenticación de usuarios (clientes y administradores)
- Gestión de tarjetas de crédito
- Seguimiento de límites de crédito
- Gestión del estado de las tarjetas
- Diseño responsivo con Bootstrap 5

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Backend CartMaster en ejecución (aplicación Spring Boot)

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd cartmaster-frontend
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Crear un archivo `.env` en el directorio raíz con el siguiente contenido:
```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
BACKEND_URL=http://localhost:8080
```

## Ejecutar la Aplicación

1. Asegúrate de que el backend CartMaster esté en ejecución

2. Iniciar el servidor de desarrollo Flask:
```bash
flask run
```

3. Acceder a la aplicación en `http://localhost:5000`

## Uso

1. Registra una nueva cuenta o inicia sesión con credenciales existentes
2. Añade y gestiona tarjetas de crédito
3. Visualiza límites de crédito y estado de las tarjetas
4. Los administradores pueden gestionar los estados de las tarjetas

## Estructura del Proyecto

```
cartmaster-frontend/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── cards.py
│   │   └── client.py
│   └── templates/
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── cards/
│       │   ├── details.html
│       │   └── new.html
│       ├── client/
│       │   ├── dashboard.html
│       │   └── profile.html
│       └── base.html
├── requirements.txt
└── README.md
```

## Consideraciones de Seguridad

- Todas las contraseñas son manejadas de forma segura por el backend
- La gestión de sesiones es manejada por Flask-Login
- Protección CSRF habilitada por defecto
- Los datos sensibles no se almacenan en el frontend

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad
3. Realiza tus cambios
4. Sube los cambios a tu rama
5. Crea un Pull Request 