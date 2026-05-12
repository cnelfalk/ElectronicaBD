# 💻 TechMatch - Sistema de Comparación de Hardware

TechMatch es una plataforma integral de comparación de hardware que permite a los usuarios encontrar y comparar componentes de PC y laptops. El sistema utiliza **bots de web scraping** para extraer automáticamente especificaciones técnicas desde las páginas oficiales de los fabricantes y precios actualizados desde tiendas online reconocidas.

## 🚀 Características Principales

- **Catálogo Automatizado**: Mantenimiento automático de productos, especificaciones y precios mediante web scraping.
- **Comparador Inteligente**: Herramienta de comparación de hardware basada en perfiles de uso.
- **Gestión de Usuarios**: Registro, autenticación y sistema de favoritos/comparaciones guardadas.
- **Arquitectura Modular**: Separación clara entre el motor de extracción de datos (Scrapers), la API de negocio (Backend) y la interfaz de usuario (Frontend).

---

## 🏗️ Arquitectura del Sistema

El proyecto está diseñado bajo un enfoque modular, dividiendo las responsabilidades en distintas capas:

### 1. Frontend (Cliente)
Desarrollado en **PHP**, HTML, CSS y JavaScript. Se encarga de la interfaz de usuario, interactuando de forma dinámica con la API REST del backend para mostrar el catálogo, el comparador y gestionar las sesiones de los usuarios.

### 2. Backend (API REST)
Desarrollado en **Python con Flask**. Expone los endpoints necesarios para el frontend. Implementa una arquitectura en capas:
- **Controladores (App)**: Manejo de rutas y peticiones HTTP (`app.py`).
- **Servicios**: Lógica de negocio y procesamiento de datos.
- **DAO (Data Access Object)**: Capa exclusiva para la comunicación segura con la base de datos MySQL (`producto_dao.py`, `usuario_dao.py`, etc.).
- **Modelos**: Representación orientada a objetos de las entidades (Productos, Laptops, CPUs, Usuarios).

### 3. Motor de Scraping (Bots)
Un conjunto de scripts automatizados en Python (utilizando **Selenium** y **BeautifulSoup**) orquestados por `run_bots.py`.
- **Scrapers de Especificaciones**: Extraen datos técnicos de sitios oficiales (ej. ASUS, Lenovo, AMD, Intel).
- **Scrapers de Retailers**: Extraen precios y disponibilidad de tiendas online (ej. MercadoLibre, Compra Gamer).

### 4. Base de Datos
Base de datos relacional **MySQL** centralizada. Almacena de manera estructurada las relaciones entre productos, categorías, marcas, perfiles de uso, tiendas y especificaciones técnicas.

---

## 🛠️ Tecnologías Utilizadas

- **Frontend**: PHP, HTML5, CSS3, JavaScript.
- **Backend**: Python 3.x, Flask, Flask-CORS.
- **Scraping**: Selenium WebDriver, BeautifulSoup4, Requests, lxml.
- **Base de Datos**: MySQL (Conector: `mysql-connector-python`).
- **Seguridad**: `bcrypt` para el hasheo de contraseñas.

---

## 📂 Estructura del Proyecto

```text
/
├── backend/                  # API REST y Motor de Scraping
│   ├── app.py                # Punto de entrada de la API Flask
│   ├── config.py             # Configuraciones del sistema y BD
│   ├── run_bots.py           # Orquestador del motor de scraping
│   ├── Requerimientos.txt    # Dependencias de Python
│   ├── dao/                  # Data Access Objects (Capa de Base de Datos)
│   ├── database/             # Conexión a MySQL (Patrón Singleton)
│   ├── modelos/              # Clases de dominio (Producto, Laptop, Usuario, etc.)
│   ├── scrapers/             # Scripts de extracción de datos (Bots)
│   └── servicios/            # Lógica de negocio (Auth, Comparaciones, etc.)
├── frontend/                 # Interfaz de Usuario en PHP
│   ├── index.php / etc.      # Vistas y lógica de presentación
│   ├── assets/               # Recursos estáticos (CSS, JS, Imágenes)
│   └── componentes/          # Componentes reutilizables de UI
└── sql/                      # Scripts de base de datos
```

---

## ⚙️ Configuración e Instalación

### Requisitos Previos
- Servidor Web para PHP (ej. Laragon, XAMPP).
- Python 3.8 o superior.
- MySQL Server.
- Navegador Chrome (para Selenium).

### Instalación del Backend y Bots
1. Navegar al directorio `backend`:
   ```bash
   cd backend
   ```
2. Crear un entorno virtual e instalar las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r Requerimientos.txt
   ```
3. Configurar las variables de entorno o editar `config.py` con las credenciales de la base de datos.
4. Iniciar el servidor Flask:
   ```bash
   python app.py
   ```

### Instalación del Frontend
1. Colocar el contenido de la carpeta `frontend` en el directorio público del servidor web (ej. `www` en Laragon o `htdocs` en XAMPP).
2. Asegurarse de que las llamadas a la API en JS apunten a la URL correcta del backend (por defecto `http://localhost:5000/api/`).

---

## 🤖 Ejecución del Motor de Scraping

Para actualizar el catálogo con los últimos productos y precios, ejecutar el orquestador de bots:

```bash
cd backend
python run_bots.py
```

Este script ejecutará secuencialmente:
1. **Bots de Retailers**: Actualización de precios desde tiendas.
2. **Bots de Fabricantes (Laptops)**: Extracción de specs de equipos completos.
3. **Bots de Fabricantes (Componentes)**: Extracción de specs de piezas individuales (CPUs, etc.).

---

## 📡 Endpoints de la API Principal

- `POST /api/register`: Registro de nuevos usuarios.
- `POST /api/login`: Autenticación de usuarios.
- `GET /api/productos`: Obtener el catálogo filtrado (soporta parámetros `categoria`, `perfil`, `busqueda`).
- `GET /api/comparar`: Comparar dos productos (requiere `idA`, `idB` y `perfil`).
