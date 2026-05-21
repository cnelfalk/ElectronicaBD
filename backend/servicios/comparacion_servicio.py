from dao.producto_dao import ProductoDAO

# ComparacionServicio - Contiene la inteligencia de evaluacion y traduccion de especificaciones.
class ComparacionServicio:
    
    # __init__ - Define el diccionario base para cuantificar el rendimiento de los procesadores.
    def __init__(self):
        self.productoDao = ProductoDAO()
        
        # Diccionario de Scoring: Transforma el texto sucio del scraper en un valor numerico duro.
        self.puntajeCpu = {
            "celeron": 15, "pentium": 20,
            "ryzen 3": 40, "core i3": 40,
            "ryzen 5": 70, "core i5": 70,
            "ryzen 7": 90, "core i7": 90,
            "ryzen 9": 100, "core i9": 100
        }
    
    # _calcularPuntajeCpu - Busca coincidencias entre el nombre del CPU extraido y nuestro diccionario.
    # Atributos: modeloCpu (str). Retorna: int (Puntaje)
    def _calcularPuntajeCpu(self, modeloCpu):
        if not modeloCpu: 
            return 0
        modeloLower = modeloCpu.lower()
        for clave, puntaje in self.puntajeCpu.items():
            if clave in modeloLower:
                return puntaje
        return 30 # Valor base si tiene un procesador antiguo o no reconocido

    # generarRecomendacionLaptops - Metodo principal que orquesta la comparacion.
    # Atributos: idProductoA (int), idProductoB (int), perfilUso (str)
    def generarRecomendacionLaptops(self, idProductoA, idProductoB, perfilUso):
        # 1. Traer los datos limpios desde la base de datos
        laptopA = self.productoDao.obtenerLaptopPorId(idProductoA)
        laptopB = self.productoDao.obtenerLaptopPorId(idProductoB)

        # Si por algun motivo el ID no existe en la BD
        if not laptopA or not laptopB:
            return {"success": False, "mensaje": "Uno de los productos no existe o no es una Laptop."}

        preciosA = self.productoDao.obtenerPreciosProducto(idProductoA)
        preciosB = self.productoDao.obtenerPreciosProducto(idProductoB)

        recomendacion = {
            "success": True,
            "datosA": laptopA,
            "datosB": laptopB,
            "preciosA": preciosA,
            "preciosB": preciosB,
            "ganador": None,
            "motivo": "",
            "puntajeA": 0,
            "puntajeB": 0
        }

        # 2. Traducir textos a valores matematicos
        rendimientoCpuA = self._calcularPuntajeCpu(laptopA['cpu_modelo'])
        rendimientoCpuB = self._calcularPuntajeCpu(laptopB['cpu_modelo'])
        
        # 3. Algoritmo Condicional segun el Perfil de Uso elegido por el usuario
        perfilLower = perfilUso.lower() if perfilUso else "general"

        if perfilLower == 'desarrollo de software':
            # Desarrollo prioriza fuertemente la RAM (maquinas virtuales, Docker) y CPU
            recomendacion['puntajeA'] = (laptopA['ram_gb'] * 3) + (rendimientoCpuA * 2)
            recomendacion['puntajeB'] = (laptopB['ram_gb'] * 3) + (rendimientoCpuB * 2)
            
        elif perfilLower in ['gaming', 'diseño']:
            # Gaming/Diseño prioriza Tasa de Refresco, CPU y RAM.
            # Nota: Al no tener benchmark de GPU exacto, usamos los Hz como factor multiplicador ligero.
            bonoHzA = 15 if laptopA['tasa_refresco_hz'] > 60 else 0
            bonoHzB = 15 if laptopB['tasa_refresco_hz'] > 60 else 0
            
            recomendacion['puntajeA'] = (laptopA['ram_gb'] * 2) + rendimientoCpuA + bonoHzA
            recomendacion['puntajeB'] = (laptopB['ram_gb'] * 2) + rendimientoCpuB + bonoHzB

        elif perfilLower == 'ofimatica':
            # Ofimatica prioriza Bateria alta y Peso bajo, la RAM y CPU importan menos.
            # Multiplicamos la bateria por 0.5 para normalizar y restamos el peso.
            recomendacion['puntajeA'] = (laptopA['capacidad_bateria_wh'] * 0.5) - laptopA['peso_kg'] + (laptopA['ram_gb'] * 1.5)
            recomendacion['puntajeB'] = (laptopB['capacidad_bateria_wh'] * 0.5) - laptopB['peso_kg'] + (laptopB['ram_gb'] * 1.5)
            
        else:
            # Uso General: Equilibrio entre RAM y CPU
            recomendacion['puntajeA'] = (laptopA['ram_gb'] * 2) + rendimientoCpuA
            recomendacion['puntajeB'] = (laptopB['ram_gb'] * 2) + rendimientoCpuB

        # 4. Determinar el Ganador y redactar la justificacion
        if recomendacion['puntajeA'] > recomendacion['puntajeB']:
            recomendacion['ganador'] = laptopA['modelo']
            recomendacion['motivo'] = f"Para el perfil '{perfilUso}', {laptopA['modelo']} ofrece mejores prestaciones con su procesador {laptopA['cpu_modelo']} y {laptopA['ram_gb']}GB de RAM."
        elif recomendacion['puntajeB'] > recomendacion['puntajeA']:
            recomendacion['ganador'] = laptopB['modelo']
            recomendacion['motivo'] = f"Para el perfil '{perfilUso}', {laptopB['modelo']} es la opcion superior gracias a sus {laptopB['ram_gb']}GB de RAM y CPU {laptopB['cpu_modelo']}."
        else:
            recomendacion['ganador'] = "Empate Técnico"
            recomendacion['motivo'] = "Ambos equipos ofrecen capacidades idénticas para el uso solicitado. Te sugerimos guiarte por el diseño físico o el precio."

        return recomendacion

    # generarRecomendacionCPUs - Metodo principal que orquesta la comparacion de procesadores.
    def generarRecomendacionCPUs(self, idProductoA, idProductoB, perfilUso):
        cpuA = self.productoDao.obtenerCPUPorId(idProductoA)
        cpuB = self.productoDao.obtenerCPUPorId(idProductoB)

        if not cpuA or not cpuB:
            return {"success": False, "mensaje": "Uno de los productos no existe o no es una CPU."}

        preciosA = self.productoDao.obtenerPreciosProducto(idProductoA)
        preciosB = self.productoDao.obtenerPreciosProducto(idProductoB)

        recomendacion = {
            "success": True,
            "datosA": cpuA,
            "datosB": cpuB,
            "preciosA": preciosA,
            "preciosB": preciosB,
            "ganador": None,
            "motivo": "",
            "puntajeA": 0,
            "puntajeB": 0
        }

        perfilLower = perfilUso.lower() if perfilUso else "general"

        frecBaseA = float(cpuA.get('frecuencia_base') or 3.0)
        frecTurboA = float(cpuA.get('frecuencia_turbo') or frecBaseA)
        nucleosA = int(cpuA.get('nucleos') or 4)
        hilosA = int(cpuA.get('hilos') or 8)
        tdpA = int(cpuA.get('tdp') or 65)

        frecBaseB = float(cpuB.get('frecuencia_base') or 3.0)
        frecTurboB = float(cpuB.get('frecuencia_turbo') or frecBaseB)
        nucleosB = int(cpuB.get('nucleos') or 4)
        hilosB = int(cpuB.get('hilos') or 8)
        tdpB = int(cpuB.get('tdp') or 65)

        if perfilLower in ['gaming', 'diseño']:
            recomendacion['puntajeA'] = (frecTurboA * 15) + (nucleosA * 8) + (hilosA * 2)
            recomendacion['puntajeB'] = (frecTurboB * 15) + (nucleosB * 8) + (hilosB * 2)

        elif perfilLower == 'desarrollo de software':
            recomendacion['puntajeA'] = (nucleosA * 15) + (hilosA * 10) + (frecBaseA * 5)
            recomendacion['puntajeB'] = (nucleosB * 15) + (hilosB * 10) + (frecBaseB * 5)

        elif perfilLower == 'ofimatica':
            # Ofimática prioriza bajo TDP y frecuencia base
            recomendacion['puntajeA'] = (frecBaseA * 20) + (nucleosA * 5) + (100 - tdpA) * 0.5
            recomendacion['puntajeB'] = (frecBaseB * 20) + (nucleosB * 5) + (100 - tdpB) * 0.5

        else:
            recomendacion['puntajeA'] = (frecBaseA * 10) + (frecTurboA * 10) + (nucleosA * 5)
            recomendacion['puntajeB'] = (frecBaseB * 10) + (frecTurboB * 10) + (nucleosB * 5)

        if recomendacion['puntajeA'] > recomendacion['puntajeB']:
            recomendacion['ganador'] = cpuA['modelo']
            recomendacion['motivo'] = f"Para el perfil '{perfilUso}', {cpuA['modelo']} ofrece mayor rendimiento debido a sus {cpuA['nucleos']} núcleos, {cpuA['hilos']} hilos y frecuencia turbo de {cpuA['frecuencia_turbo']} GHz."
        elif recomendacion['puntajeB'] > recomendacion['puntajeA']:
            recomendacion['ganador'] = cpuB['modelo']
            recomendacion['motivo'] = f"Para el perfil '{perfilUso}', {cpuB['modelo']} es la opción recomendada gracias a sus {cpuB['nucleos']} núcleos, {cpuB['hilos']} hilos y frecuencia turbo de {cpuB['frecuencia_turbo']} GHz."
        else:
            recomendacion['ganador'] = "Empate Técnico"
            recomendacion['motivo'] = "Ambos procesadores cuentan con características equivalentes de rendimiento para este perfil de uso."

        return recomendacion