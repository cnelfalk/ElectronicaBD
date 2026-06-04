# Producto - clase base supertipo para todos los componentes del catalogo
class Producto:
    # __init__ - inicializa los atributos comunes que todo hardware debe tener
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca):
        self.idProducto = idProducto
        self.modeloProducto = modeloProducto
        self.imgUrl = imgUrl
        self.urlOficial = urlOficial
        self.idCategoria = idCategoria
        self.idMarca = idMarca
        self.categoria = None
        self.marca = None

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        d = {
            "idProducto": self.idProducto,
            "modeloProducto": self.modeloProducto,
            "imgUrl": self.imgUrl,
            "urlOficial": self.urlOficial,
            "idCategoria": self.idCategoria,
            "idMarca": self.idMarca,
            
            # Compatibilidad con frontend (snake_case)
            "id_producto": self.idProducto,
            "modelo": self.modeloProducto,
            "img_url": self.imgUrl,
            "categoria": self.categoria,
            "marca": self.marca
        }
        if hasattr(self, 'fecha_agregado_fav'):
            from datetime import datetime
            val = getattr(self, 'fecha_agregado_fav')
            if isinstance(val, datetime):
                d['fecha_agregado_fav'] = val.strftime('%Y-%m-%d %H:%M:%S')
            else:
                d['fecha_agregado_fav'] = val
        if hasattr(self, 'total_favoritos'):
            d['total_favoritos'] = self.total_favoritos
        return d

    # Métodos para emular un diccionario (POO híbrida)
    def __getitem__(self, key):
        mapping = {
            "id_producto": "idProducto",
            "modelo": "modeloProducto",
            "modelo_producto": "modeloProducto",
            "img_url": "imgUrl",
            "url_oficial": "urlOficial",
            "id_categoria": "idCategoria",
            "id_marca": "idMarca",
            "frecuencia_base": "frecuenciaBase",
            "frecuencia_turbo": "frecuenciaTurbo",
            "id_socket": "idSocket",
            "vram_gb": "vram",
            "tipo_memoria": "tipoMemoria",
            "tdp_w": "consumoWh",
            "consumo_wh": "consumoWh",
            "capacidad_gb": "capacidadGbRam",
            "capacidad_gb_ram": "capacidadGbRam",
            "velocidad_mhz": "velocidadMhz",
            "latencia": "latenciaCl",
            "latencia_cl": "latenciaCl",
            "tipo_ram": "tipoRam",
            "capacidad_gb_almacenamiento": "capacidadGbAlmacenamiento",
            "tipo_disco": "tipoAlmacenamiento",
            "tipo_almacenamiento": "tipoAlmacenamiento",
            "velocidad_lectura": "velLectura",
            "vel_lectura": "velLectura",
            "vel_escritura": "velEscritura",
            "cpu_modelo": "cpu",
            "gpu_modelo": "gpu",
            "ram_gb": "ram",
            "almacenamiento_gb": "almacenamiento",
            "peso_kg": "pesoKg",
            "tamanio_pantalla": "tamanioPantalla",
            "tasa_refresco_hz": "tasaRefrescoHz",
            "capacidad_bateria_wh": "capacidadBateriaWh"
        }
        mapped_attr = mapping.get(key, key)
        if hasattr(self, mapped_attr):
            return getattr(self, mapped_attr)
        # Si no existe en el mapeo ni como atributo, levantar KeyError para emular dict
        raise KeyError(key)

    def __setitem__(self, key, value):
        mapping = {
            "id_producto": "idProducto",
            "modelo": "modeloProducto",
            "modelo_producto": "modeloProducto",
            "img_url": "imgUrl",
            "url_oficial": "urlOficial",
            "id_categoria": "idCategoria",
            "id_marca": "idMarca",
            "frecuencia_base": "frecuenciaBase",
            "frecuencia_turbo": "frecuenciaTurbo",
            "id_socket": "idSocket",
            "vram_gb": "vram",
            "tipo_memoria": "tipoMemoria",
            "tdp_w": "consumoWh",
            "consumo_wh": "consumoWh",
            "capacidad_gb": "capacidadGbRam",
            "capacidad_gb_ram": "capacidadGbRam",
            "velocidad_mhz": "velocidadMhz",
            "latencia": "latenciaCl",
            "latencia_cl": "latenciaCl",
            "tipo_ram": "tipoRam",
            "capacidad_gb_almacenamiento": "capacidadGbAlmacenamiento",
            "tipo_disco": "tipoAlmacenamiento",
            "tipo_almacenamiento": "tipoAlmacenamiento",
            "velocidad_lectura": "velLectura",
            "vel_lectura": "velLectura",
            "vel_escritura": "velEscritura",
            "cpu_modelo": "cpu",
            "gpu_modelo": "gpu",
            "ram_gb": "ram",
            "almacenamiento_gb": "almacenamiento",
            "peso_kg": "pesoKg",
            "tamanio_pantalla": "tamanioPantalla",
            "tasa_refresco_hz": "tasaRefrescoHz",
            "capacidad_bateria_wh": "capacidadBateriaWh"
        }
        mapped_attr = mapping.get(key, key)
        setattr(self, mapped_attr, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default