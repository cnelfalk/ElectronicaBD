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
        # extraerParametrosUrl - captura las variables enviadas por JS (ej: ?categoria=GPU)
        categoria = request.args.get('categoria')
        perfil = request.args.get('perfil')
        busqueda = request.args.get('busqueda')

        # delegarAlServicio - pasa los filtros al intermediario de negocio
        resultado = productoServicio.listarProductos(categoria, perfil, busqueda)
        
        # retornarJson - envia el paquete al navegador
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error del servidor: {str(e)}'}), 500

# compararEndpoint - Ruta GET para evaluar dos equipos (Laptops o CPUs)
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

        # Redirigir al servicio adecuado
        if categoriaA == 'Laptop':
            resultado = comparacionServicio.generarRecomendacionLaptops(idProductoA, idProductoB, perfilUso)
        elif categoriaA == 'CPU':
            resultado = comparacionServicio.generarRecomendacionCPUs(idProductoA, idProductoB, perfilUso)
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

if __name__ == '__main__':
    # host='0.0.0.0' permite que Flask sea visible en toda la red (incluído Tailscale)
    app.run(debug=True, port=5000, host='0.0.0.0')