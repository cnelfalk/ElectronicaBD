from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from servicios.auth_servicio import AuthServicio
from servicios.producto_servicio import ProductoServicio
from servicios.comparacion_servicio import ComparacionServicio
from servicios.favorito_servicio import FavoritoServicio

# inicializarAplicacion - configura el servidor Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# instanciarServicio - creamos una instancia global del servicio de autenticacion
authServicio = AuthServicio()
# Instanciar el servicio globalmente
favoritoServicio = FavoritoServicio()
productoServicio = ProductoServicio()
comparacionServicio = ComparacionServicio()

# registrarUsuarioEndpoint - recibe peticion POST desde PHP para registrar un usuario
@app.route('/api/register', methods=['POST'])
def registrarUsuarioEndpoint():
    try:
        # extraerDatos - obtiene el payload JSON enviado por el frontend
        datos = request.get_json()
        nombreUsuario = datos.get('nombreUsuario')
        emailUsuario = datos.get('emailUsuario')
        contraseniaPlana = datos.get('contraseniaUsuario')

        # validacionBasica - asegurar que no lleguen campos vacios desde PHP
        if not nombreUsuario or not emailUsuario or not contraseniaPlana:
            return jsonify({'success': False, 'mensaje': 'Faltan datos requeridos'}), 400

        # ejecutarRegistro - delega la logica al servicio
        resultado = authServicio.registrarUsuario(nombreUsuario, emailUsuario, contraseniaPlana)
        
        # retornarRespuesta - devuelve 200 OK si es exitoso, o 400 Bad Request si falla
        return jsonify(resultado), 200 if resultado['success'] else 400

    except Exception as e:
        # manejarErrorGlobal - atrapa excepciones no controladas
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# loginUsuarioEndpoint - recibe credenciales POST y devuelve estado de autenticacion
@app.route('/api/login', methods=['POST'])
def loginUsuarioEndpoint():
    try:
        datos = request.get_json()
        
        # ---------------------------------------------------------
        # CAMBIO: Ahora recibimos 'identificador' desde el frontend
        # ---------------------------------------------------------
        identificador = datos.get('identificador')
        contraseniaPlana = datos.get('contraseniaUsuario')

        if not identificador or not contraseniaPlana:
            return jsonify({'success': False, 'mensaje': 'Faltan credenciales'}), 400

        # Pasamos el identificador (que puede ser email o usuario) al servicio
        resultado = authServicio.autenticarUsuario(identificador, contraseniaPlana)
        
        # retornarRespuesta - 200 OK o 401 Unauthorized si las credenciales son invalidas
        return jsonify(resultado), 200 if resultado['success'] else 401

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# ══════════════════════════════════════════════════════
#  RECUPERACIÓN DE CONTRASEÑA
# ══════════════════════════════════════════════════════

# solicitarRecuperacionEndpoint - recibe POST con email y envía código de recuperación
@app.route('/api/recuperar/solicitar', methods=['POST'])
def solicitarRecuperacionEndpoint():
    try:
        datos = request.get_json()
        emailUsuario = datos.get('emailUsuario')

        if not emailUsuario:
            return jsonify({'success': False, 'mensaje': 'Se requiere un correo electrónico'}), 400

        resultado = authServicio.solicitarRecuperacion(emailUsuario)
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# verificarCodigoEndpoint - recibe POST con email y código, devuelve token si es válido
@app.route('/api/recuperar/verificar', methods=['POST'])
def verificarCodigoEndpoint():
    try:
        datos = request.get_json()
        emailUsuario = datos.get('emailUsuario')
        codigo = datos.get('codigo')

        if not emailUsuario or not codigo:
            return jsonify({'success': False, 'mensaje': 'Faltan datos requeridos'}), 400

        resultado = authServicio.verificarCodigo(emailUsuario, codigo)
        return jsonify(resultado), 200 if resultado['success'] else 400

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# cambiarContraseniaEndpoint - recibe POST con email, token y nueva contraseña
@app.route('/api/recuperar/cambiar', methods=['POST'])
def cambiarContraseniaEndpoint():
    try:
        datos = request.get_json()
        emailUsuario = datos.get('emailUsuario')
        token = datos.get('token')
        nuevaContrasenia = datos.get('nuevaContrasenia')

        if not emailUsuario or not token or not nuevaContrasenia:
            return jsonify({'success': False, 'mensaje': 'Faltan datos requeridos'}), 400

        if len(nuevaContrasenia) < 6:
            return jsonify({'success': False, 'mensaje': 'La contraseña debe tener al menos 6 caracteres'}), 400

        resultado = authServicio.cambiarContrasenia(emailUsuario, token, nuevaContrasenia)
        return jsonify(resultado), 200 if resultado['success'] else 400

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# obtenerProductosEndpoint - ruta GET para consultar el catalogo
@app.route('/api/productos', methods=['GET'])
def obtenerProductosEndpoint():
    try:
        categoria = request.args.get('categoria')
        perfil    = request.args.get('perfil')
        busqueda  = request.args.get('busqueda')
        marca     = request.args.get('marca')
        ordenar   = request.args.get('ordenar')

        resultado = productoServicio.listarProductos(categoria, perfil, busqueda, marca, ordenar)
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# obtenerMarcasEndpoint - ruta GET para listar marcas con productos (para poblar el filtro del catálogo)
@app.route('/api/marcas', methods=['GET'])
def obtenerMarcasEndpoint():
    try:
        return jsonify(productoServicio.obtenerMarcas()), 200
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# obtenerCategoriasEndpoint - ruta GET para listar todas las categorías del sistema
@app.route('/api/categorias', methods=['GET'])
def obtenerCategoriasEndpoint():
    try:
        return jsonify(productoServicio.obtenerCategorias()), 200
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# obtenerTiendasEndpoint - ruta GET para listar todas las tiendas registradas
@app.route('/api/tiendas', methods=['GET'])
def obtenerTiendasEndpoint():
    try:
        return jsonify(productoServicio.obtenerTiendas()), 200
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# detalleProductoEndpoint - Ruta GET para obtener el detalle completo de un producto
@app.route('/api/productos/<int:idProducto>', methods=['GET'])
def detalleProductoEndpoint(idProducto):
    try:
        detalle = productoServicio.obtenerDetalle(idProducto)

        if not detalle:
            return jsonify({'success': False, 'mensaje': 'Producto no encontrado.'}), 404

        return jsonify({'success': True, 'data': detalle}), 200

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# compararEndpoint - Ruta GET para evaluar dos equipos (Laptops, CPUs, GPUs, RAM o Almacenamiento)
@app.route('/api/comparar', methods=['GET'])
def compararEndpoint():
    try:
        idProductoA = request.args.get('idA', type=int)
        idProductoB = request.args.get('idB', type=int)
        perfilUso = request.args.get('perfil', default='Uso General', type=str)

        if not idProductoA or not idProductoB:
            return jsonify({
                'success': False, 
                'mensaje': 'Se requieren exactamente dos IDs (idA, idB) para comparar.'
            }), 400

        categoriaA = comparacionServicio.productoDao.obtenerCategoriaPorId(idProductoA)
        categoriaB = comparacionServicio.productoDao.obtenerCategoriaPorId(idProductoB)

        if not categoriaA or not categoriaB:
            return jsonify({
                'success': False,
                'mensaje': 'Uno o ambos productos no existen o no tienen una categoría asignada.'
            }), 404

        if categoriaA != categoriaB:
            return jsonify({
                'success': False,
                'mensaje': f'No se pueden comparar productos de diferentes categorías ({categoriaA} vs {categoriaB}).'
            }), 400

        if categoriaA == 'Laptop':
            resultado = comparacionServicio.generarRecomendacionLaptops(idProductoA, idProductoB, perfilUso)
        elif categoriaA == 'CPU':
            resultado = comparacionServicio.generarRecomendacionCPUs(idProductoA, idProductoB, perfilUso)
        elif categoriaA == 'GPU':
            resultado = comparacionServicio.generarRecomendacionGPUs(idProductoA, idProductoB, perfilUso)
        elif categoriaA == 'RAM':
            resultado = comparacionServicio.generarRecomendacionRAMs(idProductoA, idProductoB, perfilUso)
        elif categoriaA == 'Almacenamiento':
            resultado = comparacionServicio.generarRecomendacionAlmacenamiento(idProductoA, idProductoB, perfilUso)
        else:
            return jsonify({
                'success': False,
                'mensaje': f'La categoría {categoriaA} no está soportada para comparación actualmente.'
            }), 400
        
        if not resultado.get('success'):
            return jsonify(resultado), 404

        # Verificar si la comparación ya fue guardada por el usuario
        idUsuario = request.args.get('idUsuario', type=int)
        if idUsuario:
            resultado['yaGuardada'] = comparacionServicio.comparacionDao.existeComparacion(idUsuario, idProductoA, idProductoB)
        else:
            resultado['yaGuardada'] = False

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error interno del servidor: {str(e)}'}), 500

# guardarComparacionEndpoint - recibe POST con idUsuario, idProductoA e idProductoB y guarda la comparacion
@app.route('/api/comparar/guardar', methods=['POST'])
def guardarComparacionEndpoint():
    try:
        datos = request.get_json()
        idUsuario = datos.get('idUsuario')
        idProductoA = datos.get('idProductoA')
        idProductoB = datos.get('idProductoB')

        if not idUsuario or not idProductoA or not idProductoB:
            return jsonify({'success': False, 'mensaje': 'Faltan datos requeridos'}), 400

        # Obtener idCategoria del primer producto
        idCategoria = comparacionServicio.productoDao.obtenerIdCategoriaNumerica(idProductoA)

        resultado = comparacionServicio.guardarComparacion(idUsuario, idProductoA, idProductoB, idCategoria)
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

@app.route('/api/comparar/historial/<int:idUsuario>', methods=['GET'])
def obtenerHistorialComparacionesEndpoint(idUsuario):
    try:
        historial = comparacionServicio.obtenerComparacionesUsuario(idUsuario)
        return jsonify({'success': True, 'data': historial}), 200
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

@app.route('/api/comparar/<int:idComparacion>', methods=['DELETE'])
def eliminarComparacionEndpoint(idComparacion):
    try:
        resultado = comparacionServicio.eliminarComparacion(idComparacion)
        if resultado:
            return jsonify({'success': True, 'mensaje': 'Comparación eliminada exitosamente'}), 200
        else:
            return jsonify({'success': False, 'mensaje': 'Error al eliminar la comparación'}), 500
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# ══════════════════════════════════════════════════════
#  FAVORITOS
# ══════════════════════════════════════════════════════

# obtenerFavoritosEndpoint - recibe GET con idUsuario y devuelve la lista de favoritos
@app.route('/api/favoritos/<int:idUsuario>', methods=['GET'])
def obtenerFavoritosEndpoint(idUsuario):
    try:
        resultado = favoritoServicio.listar(idUsuario)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# agregarFavoritoEndpoint - recibe POST con idUsuario e idProducto y agrega a favoritos
@app.route('/api/favoritos/agregar', methods=['POST'])
def agregarFavoritoEndpoint():
    try:
        datos = request.get_json()
        idUsuario = datos.get('idUsuario')
        idProducto = datos.get('idProducto')

        if not idUsuario or not idProducto:
            return jsonify({'success': False, 'mensaje': 'Faltan datos requeridos'}), 400

        resultado = favoritoServicio.agregar(idUsuario, idProducto)
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# eliminarFavoritoEndpoint - recibe DELETE con idUsuario e idProducto y remueve de favoritos
@app.route('/api/favoritos/eliminar', methods=['DELETE'])
def eliminarFavoritoEndpoint():
    try:
        datos = request.get_json()
        idUsuario = datos.get('idUsuario')
        idProducto = datos.get('idProducto')

        if not idUsuario or not idProducto:
            return jsonify({'success': False, 'mensaje': 'Faltan datos requeridos'}), 400

        resultado = favoritoServicio.eliminar(idUsuario, idProducto)
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

if __name__ == '__main__':
    # host='0.0.0.0' permite que Flask sea visible en toda la red (incluído Tailscale)
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=True)