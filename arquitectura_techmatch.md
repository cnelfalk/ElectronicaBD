# Arquitectura TechMatch - Flask Backend + PHP Frontend

## Estructura del Proyecto

```
TechMatch/
│
├── backend/                            # API REST con Flask (Python)
│   ├── app.py                          # Punto de entrada Flask (rutas HTTP)
│   ├── config.py                       # Configuración centralizada (BD, secret key, CORS)
│   ├── run_bots.py                     # Orquestador de scrapers
│   ├── requirements.txt                # Dependencias Python
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── conexion.py                 # ConexionDB (Singleton)
│   │
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── usuario.py                  # class Usuario
│   │   ├── producto.py                 # class Producto (supertipo)
│   │   ├── laptop.py                   # class Laptop(Producto)
│   │   ├── cpu.py                      # class CPU(Producto)
│   │   ├── gpu.py                      # class GPU(Producto)
│   │   ├── ram.py                      # class RAM(Producto)
│   │   ├── placa_madre.py              # class PlacaMadre(Producto)
│   │   ├── almacenamiento.py           # class Almacenamiento(Producto)
│   │   ├── marca.py                    # class Marca
│   │   ├── categoria.py                # class Categoria
│   │   ├── perfil_uso.py               # class PerfilUso (NUEVO)
│   │   ├── producto_perfil.py          # class ProductoPerfil (NUEVO - N:M)
│   │   ├── tienda.py                   # class Tienda
│   │   ├── socket.py                   # class Socket
│   │   └── comparacion_guardada.py     # class ComparacionGuardada
│   │
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── usuario_dao.py              # class UsuarioDAO
│   │   ├── producto_dao.py             # class ProductoDAO (CRUD + upsert precios)
│   │   ├── marca_dao.py                # class MarcaDAO
│   │   ├── categoria_dao.py            # class CategoriaDAO
│   │   ├── perfil_uso_dao.py           # class PerfilUsoDAO (NUEVO)
│   │   ├── tienda_dao.py               # class TiendaDAO
│   │   ├── socket_dao.py               # class SocketDAO
│   │   ├── comparacion_dao.py          # class ComparacionDAO
│   │   └── favorito_dao.py             # class FavoritoDAO
│   │
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── auth_servicio.py            # class AuthServicio (login, registro, bcrypt)
│   │   ├── producto_servicio.py        # class ProductoServicio (búsqueda, filtros)
│   │   ├── comparacion_servicio.py     # class ComparacionServicio (comparar productos)
│   │   └── favorito_servicio.py        # class FavoritoServicio (agregar, listar, quitar)
│   │
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── scraper_base.py             # class ScraperBase (abstracta)
│   │   ├── scrapers_precios.py         # class CompraGamerScraper, MercadoLibreScraper
│   │   └── scrapers_especificaciones.py # class AMDScraper, IntelScraper, LenovoScraper, AsusScraper
│   │
│   └── utils/
│       ├── __init__.py
│       ├── normalizacion.py            # Normalización de términos técnicos (FHD→1920x1080, etc)
│       └── validacion.py               # Validación de compatibilidad (CPU-Socket, RAM-Placa)
│
├── frontend/                           # Interfaz web con PHP
│   ├── index.php                       # Home / Landing page
│   ├── login.php                       # Formulario de login
│   ├── registro.php                    # Formulario de registro
│   ├── catalogo.php                    # Listado de productos con filtros
│   ├── detalle_producto.php            # Ficha de un producto individual
│   ├── comparar.php                    # Vista de comparación lado a lado
│   ├── favoritos.php                   # Lista de favoritos del usuario
│   ├── comparaciones_guardadas.php     # Historial de comparaciones
│   │
│   ├── components/
│   │   ├── navbar.php                  # Barra de navegación
│   │   ├── footer.php                  # Pie de página
│   │   └── card_producto.php           # Tarjeta reutilizable de producto
│   │
│   ├── config/
│   │   └── api.php                     # URL base del backend Flask
│   │
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css               # Estilos CSS
│   │   ├── js/
│   │   │   ├── api.js                  # Cliente API (fetch al backend Flask)
│   │   │   ├── catalogo.js             # Lógica de filtros y búsqueda
│   │   │   ├── comparacion.js          # Lógica de comparación
│   │   │   └── favoritos.js            # Lógica de favoritos
│   │   └── img/
│   │       └── logo.png                # Logo TechMatch
│   │
│   └── utils/
│       ├── session.php                 # Manejo de sesión PHP
│       └── helpers.php                 # Funciones auxiliares
│
└── sql/
    ├── schema.sql                      # Script de creación de la BD (18 tablas, 3FN)
    └── seed_data.sql                   # Datos iniciales (categorías, perfiles, marcas, etc)
```

---

## Resumen por Capa

### Backend (Flask - Python)

| Capa | Archivos | Responsabilidad |
|---|---|---|
| **modelos/** | 15 clases | Representan las entidades del modelo relacional |
| **dao/** | 9 clases | CRUD contra las 18 tablas de la BD |
| **servicios/** | 4 clases | Lógica de negocio (auth, búsqueda, comparación, favoritos) |
| **scrapers/** | 3 archivos, 7 clases | Jerarquía OOP de scrapers (1 base abstracta + 2 precios + 4 specs) |
| **utils/** | 2 módulos | Normalización de términos y validación de compatibilidad |

### Frontend (PHP)

| Capa | Archivos | Responsabilidad |
|---|---|---|
| **pages/** | 8 páginas | Vistas principales de la aplicación |
| **components/** | 3 componentes | Elementos reutilizables (navbar, footer, cards) |
| **assets/** | CSS, JS, Imágenes | Recursos estáticos y lógica del cliente |
| **config/** | 1 archivo | Configuración de conexión al backend |

---

## Entidades del Modelo (actualizadas)

### Entidades principales (13):
1. **Usuarios** - Gestión de cuentas
2. **Productos** - Supertipo para todos los productos
3. **Laptops** - Especialización de Productos
4. **CPU** - Especialización de Productos
5. **GPU** - Especialización de Productos
6. **RAM** - Especialización de Productos
7. **Placa_Madre** - Especialización de Productos
8. **Almacenamiento** - Especialización de Productos
9. **Marcas** - Fabricantes de productos
10. **Categorias** - Tipos de productos (CPU, GPU, Laptop, etc.)
11. **Perfiles_Uso** - Perfiles de uso (Gaming, Desarrollo, Ofimática, Diseño) **[NUEVO]**
12. **Tiendas** - Tiendas donde se venden productos
13. **Socket** - Compatibilidad CPU-Placa
14. **Comparaciones_Guardadas** - Historial de comparaciones del usuario

### Tablas de relación (5):
1. **Productos_Perfiles** - N:M entre Productos y Perfiles_Uso **[NUEVO]**
2. **Guarda_Favorito** - N:M entre Usuarios y Productos
3. **Contiene** - N:M entre Comparaciones_Guardadas y Productos
4. **Se_Vende_En** - N:M entre Productos y Tiendas (con precio y URL)

**Total: 18 tablas**

---

## Comunicación Backend ↔ Frontend

### Flujo de datos:
```
PHP Frontend → HTTP Request → Flask Backend → MySQL
                                     ↓
PHP Frontend ← JSON Response ← Flask Backend ← MySQL
```

### Ejemplo de endpoint:
```
GET http://localhost:5000/api/productos?categoria=CPU&perfil=Gaming
```

**Respuesta JSON:**
```json
{
  "success": true,
  "data": [
    {
      "id_producto": 1,
      "modelo": "Intel Core i9-13900K",
      "marca": "Intel",
      "categoria": "CPU",
      "perfiles": ["Gaming", "Desarrollo"],
      "specs": {
        "nucleos": 24,
        "hilos": 32,
        "frecuencia_base": 3.0,
        "frecuencia_turbo": 5.8
      },
      "precios": [
        {
          "tienda": "Compra Gamer",
          "precio": 550000,
          "url": "https://compragamer.com/producto/..."
        }
      ]
    }
  ]
}
```

---

## Nuevos cambios implementados

### 1. Entidad Perfiles_Uso
- Permite filtrar productos por perfil de uso
- Relación N:M con Productos mediante Productos_Perfiles
- Un producto puede servir para múltiples perfiles

### 2. Restricción de comparaciones homogéneas
- `Comparaciones_Guardadas` tiene `id_categoria`
- Solo se pueden comparar productos de la misma categoría
- CPU vs CPU ✓, Laptop vs Laptop ✓, CPU vs GPU ✗

### 3. Compatibilidad CPU-Placa
- `Placa_Madre` ahora tiene `id_socket`
- Se puede validar si un CPU encaja en una placa
- Validación en `utils/validacion.py`

### 4. Correcciones del modelo
- ✅ Typo corregido: `tasa_refresco_hz`
- ✅ UNIQUE constraint en `email_usuario`
- ✅ Columna extraña `Placa_Madrecol` eliminada

---

## Convenciones de Código

### Nomenclatura (español):
- **Clases:** `UsuarioDAO`, `ProductoServicio`, `ComparacionGuardada`
- **Métodos:** `obtenerProductos()`, `crearComparacion()`, `validarCompatibilidad()`
- **Variables:** `idUsuario`, `nombreProducto`, `precioActual`

### Comentarios (camelCase):
```python
# obtenerProductosPorCategoria - filtra productos según la categoría especificada
def obtenerProductosPorCategoria(self, idCategoria):
    # construirQuery - genera el SQL con filtros dinámicos
    query = self._construirQuery(idCategoria)
    # ejecutarConsulta - realiza la consulta y retorna resultados
    return self.conexion.ejecutar(query)
```

**Regla:** Comentarios solo explican el código, NO dan especificaciones manuales al equipo.
