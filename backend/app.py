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
        emailUsuario = datos.get('emailUsuario')
        contraseniaPlana = datos.get('contraseniaUsuario')

        if not emailUsuario or not contraseniaPlana:
            return jsonify({'success': False, 'mensaje': 'Faltan credenciales'}), 400

        resultado = authServicio.autenticarUsuario(emailUsuario, contraseniaPlana)
        
        # retornarRespuesta - 200 OK o 401 Unauthorized si las credenciales son invalidas
        return jsonify(resultado), 200 if resultado['success'] else 401

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
        # extraerParametros - Capturamos los IDs y el perfil desde la URL
        # Usamos type=int para forzar que los IDs sean numeros y evitar errores de SQL
        idProductoA = request.args.get('idA', type=int)
        idProductoB = request.args.get('idB', type=int)
        perfilUso = request.args.get('perfil', default='Uso General', type=str)

        # validacionBasica - Comprobamos que el frontend haya enviado ambos IDs
        if not idProductoA or not idProductoB:
            return jsonify({
                'success': False, 
                'mensaje': 'Se requieren exactamente dos IDs (idA, idB) para comparar.'
            }), 400

        # Obtener las categorías de los dos productos seleccionados
        categoriaA = comparacionServicio.productoDao.obtenerCategoriaPorId(idProductoA)
        categoriaB = comparacionServicio.productoDao.obtenerCategoriaPorId(idProductoB)

        if not categoriaA or not categoriaB:
            return jsonify({
                'success': False,
                'mensaje': 'Uno o ambos productos no existen o no tienen una categoría asignada.'
            }), 404

        # Validar que ambos pertenezcan a la misma categoría
        if categoriaA != categoriaB:
            return jsonify({
                'success': False,
                'mensaje': f'No se pueden comparar productos de diferentes categorías ({categoriaA} vs {categoriaB}).'
            }), 400

        # Redirigir al servicio adecuado según la categoría
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
        
        # verificarRespuesta - Si el servicio no encontro los IDs en la BD, devuelve un 404 Not Found
        if not resultado.get('success'):
            return jsonify(resultado), 404

        # retornarJson - Si todo salio bien, devolvemos el veredicto completo
        return jsonify(resultado), 200

    except Exception as e:
        # atraparErrores - Si algo explota en Python, evitamos que el servidor se caiga
        return jsonify({'success': False, 'mensaje': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/api/favoritos/agregar', methods=['POST'])
def agregarFavoritoEndpoint():
    try:
        datos = request.get_json()
        idUsuario = datos.get('idUsuario')
        idProducto = datos.get('idProducto')

        resultado = favoritoServicio.agregar(idUsuario, idProducto)
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/favoritos/<int:idUsuario>', methods=['GET'])
def listarFavoritosEndpoint(idUsuario):
    try:
        resultado = favoritoServicio.listar(idUsuario)
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/favoritos/eliminar', methods=['DELETE'])
def eliminarFavoritoEndpoint():
    try:
        datos = request.get_json()
        idUsuario = datos.get('idUsuario')
        idProducto = datos.get('idProducto')
        
        resultado = favoritoServicio.eliminar(idUsuario, idProducto)
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/comparar/guardar', methods=['POST'])
def guardarComparacionEndpoint():
    try:
        datos = request.get_json()
        idUsuario = datos.get('idUsuario')
        idProductoA = datos.get('idProductoA')
        idProductoB = datos.get('idProductoB')

        if not idUsuario or not idProductoA or not idProductoB:
            return jsonify({'success': False, 'mensaje': 'Faltan datos requeridos (idUsuario, idProductoA, idProductoB)'}), 400

        # Obtener el id_categoria numerico directo desde el DAO (sin abrir cursores en el controlador)
        idCategoria = comparacionServicio.productoDao.obtenerIdCategoriaNumerica(idProductoA)

        resultado = comparacionServicio.guardarComparacion(idUsuario, idProductoA, idProductoB, idCategoria)
        if resultado:
            return jsonify({'success': True, 'mensaje': 'Comparación guardada exitosamente'}), 200
        else:
            return jsonify({'success': False, 'mensaje': 'Error al guardar la comparación en la base de datos'}), 500
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

if __name__ == '__main__':
    # host='0.0.0.0' permite que Flask sea visible en toda la red (incluído Tailscale)
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=True)
