# CartMaster Frontend

Sistema robusto de gestión de tarjetas de crédito construido con Flask, que proporciona una interfaz de usuario segura e intuitiva para interactuar con el servicio backend de CartMaster.

## 📋 Descripción General

CartMaster Frontend es una aplicación web basada en Flask que sirve como interfaz de usuario para operaciones de gestión de tarjetas de crédito. Proporciona una forma segura y eficiente de manejar tareas relacionadas con tarjetas de crédito mientras mantiene una experiencia de usuario limpia y moderna.

## 🔧 Stack Tecnológico

- **Framework:** Flask 3.0.2
- **Frontend:** HTML5, CSS3, JavaScript
- **Autenticación:** Flask-Login 0.6.3
- **Formularios:** Flask-WTF 1.2.1
- **Cliente HTTP:** Requests 2.31.0
- **Gestión de Entorno:** python-dotenv 1.0.1
- **Gestión de Tiempo:** Flask-Moment 1.0.6

## 🚀 Comenzando

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/AFlazaroo/CartMaster-FED.git
cd CartMaster-FE
```

2. **Crear y activar el entorno virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
# Modo desarrollo
python wsgi.py

La aplicación estará disponible en `http://localhost:5000`

## 📁 Estructura del Proyecto

```
CartMaster-FE/
├── app/                    # Paquete de la aplicación
│   ├── __init__.py        # Inicialización de la app
│   ├── models.py          # Modelos de base de datos
│   ├── decorators.py      # Decoradores personalizados
│   ├── routes/            # Manejadores de rutas
│   ├── services/          # Lógica de negocio
│   ├── static/            # Archivos estáticos (CSS, JS, imágenes)
│   └── templates/         # Plantillas Jinja2
├── venv/                  # Entorno virtual

├── requirements.txt       # Dependencias Python
├── README.md             # Documentación del proyecto
└── wsgi.py               # Punto de entrada WSGI
```

## 🛠️ Características

- **Autenticación de Usuario**
  - Inicio de sesión y registro seguros
  - Gestión de sesiones

- **Gestión de Tarjetas**
  - Visualización y gestión de tarjetas de crédito
  - Activación/desactivación de tarjetas
  - Gestión de límites en administrador

## 📮 Contacto

Para soporte o consultas, por favor contáctanos:
- Email: yaacosta@unbosque.edu.co

---
Hecho con ❤️ por el Equipo CartMaster (Lazaro y yeferson)