from dao.producto_dao import ProductoDAO
from dao.comparacion_dao import ComparacionDAO

# ComparacionServicio - Contiene la inteligencia de evaluacion y traduccion de especificaciones.
class ComparacionServicio:
    
    # __init__ - Define el diccionario base para cuantificar el rendimiento de los procesadores.
    def __init__(self):
        self.productoDao = ProductoDAO()
        self.comparacionDao = ComparacionDAO()
        
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

        # Sanitizar valores de especificaciones y castear de Decimal a float/int
        for laptop in [laptopA, laptopB]:
            if laptop:
                laptop['peso_kg'] = float(laptop.get('peso_kg') or 1.6)
                laptop['tamanio_pantalla'] = float(laptop.get('tamanio_pantalla') or 15.6)
                laptop['tasa_refresco_hz'] = int(laptop.get('tasa_refresco_hz') or 60)
                laptop['capacidad_bateria_wh'] = float(laptop.get('capacidad_bateria_wh') or 45.0)
                laptop['ram_gb'] = int(laptop.get('ram_gb') or 8)
                laptop['almacenamiento_gb'] = int(laptop.get('almacenamiento_gb') or 256)

        # 2. Traducir textos a valores matematicos
        rendimientoCpuA = self._calcularPuntajeCpu(laptopA['cpu_modelo'])
        rendimientoCpuB = self._calcularPuntajeCpu(laptopB['cpu_modelo'])
        laptopA['cpu_score'] = rendimientoCpuA
        laptopB['cpu_score'] = rendimientoCpuB
        
        # 3. Algoritmo Condicional segun el Perfil de Uso elegido por el usuario
        perfilLower = perfilUso.lower() if perfilUso else "general"
        perfilLower = perfilLower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

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
        if recomendacion['puntajeA'] > recomendacion['puntajeB'] or recomendacion['puntajeB'] > recomendacion['puntajeA']:
            if recomendacion['puntajeA'] > recomendacion['puntajeB']:
                recomendacion['ganador'] = laptopA['modelo']
                ganador = laptopA
                perdedor = laptopB
                g_cpu_score = rendimientoCpuA
                p_cpu_score = rendimientoCpuB
            else:
                recomendacion['ganador'] = laptopB['modelo']
                ganador = laptopB
                perdedor = laptopA
                g_cpu_score = rendimientoCpuB
                p_cpu_score = rendimientoCpuA

            motivos_lista = []
            
            # Comparar CPU
            if g_cpu_score > p_cpu_score:
                motivos_lista.append(f"un procesador más potente ({ganador['cpu_modelo']} vs {perdedor['cpu_modelo']})")
            
            # Comparar RAM
            if ganador['ram_gb'] > perdedor['ram_gb']:
                motivos_lista.append(f"mayor cantidad de memoria RAM ({ganador['ram_gb']} GB vs {perdedor['ram_gb']} GB)")
            
            # Comparar Almacenamiento
            if ganador['almacenamiento_gb'] > perdedor['almacenamiento_gb']:
                motivos_lista.append(f"más espacio de almacenamiento ({ganador['almacenamiento_gb']} GB vs {perdedor['almacenamiento_gb']} GB)")

            # Comparar Batería
            if ganador['capacidad_bateria_wh'] > perdedor['capacidad_bateria_wh'] + 5:
                motivos_lista.append(f"una batería de mayor capacidad ({int(ganador['capacidad_bateria_wh'])} Wh vs {int(perdedor['capacidad_bateria_wh'])} Wh)")

            # Comparar Peso
            if ganador['peso_kg'] < perdedor['peso_kg'] - 0.2:
                motivos_lista.append(f"un diseño más ligero y transportable ({ganador['peso_kg']} kg vs {perdedor['peso_kg']} kg)")

            # Comparar Tasa de Refresco
            if ganador['tasa_refresco_hz'] > perdedor['tasa_refresco_hz']:
                motivos_lista.append(f"una pantalla más fluida de {ganador['tasa_refresco_hz']} Hz")

            if motivos_lista:
                if len(motivos_lista) == 1:
                    detalles = motivos_lista[0]
                else:
                    detalles = ", ".join(motivos_lista[:-1]) + " y " + motivos_lista[-1]
                recomendacion['motivo'] = f"Este equipo es recomendado para el perfil '{perfilUso}' porque ofrece {detalles}."
            else:
                recomendacion['motivo'] = f"Este equipo se posiciona con un mejor equilibrio general en rendimiento y portabilidad para tus tareas."
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
        perfilLower = perfilLower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

        # Sanitizar valores de especificaciones y castear de Decimal a float/int
        for cpu in [cpuA, cpuB]:
            if cpu:
                cpu['nucleos'] = int(cpu.get('nucleos') or 4)
                cpu['hilos'] = int(cpu.get('hilos') or 8)
                cpu['frecuencia_base'] = float(cpu.get('frecuencia_base') or 3.0)
                cpu['frecuencia_turbo'] = float(cpu.get('frecuencia_turbo') or cpu['frecuencia_base'])
                cpu['tdp'] = int(cpu.get('tdp') or 65)

        frecBaseA = cpuA['frecuencia_base']
        frecTurboA = cpuA['frecuencia_turbo']
        nucleosA = cpuA['nucleos']
        hilosA = cpuA['hilos']
        tdpA = cpuA['tdp']

        frecBaseB = cpuB['frecuencia_base']
        frecTurboB = cpuB['frecuencia_turbo']
        nucleosB = cpuB['nucleos']
        hilosB = cpuB['hilos']
        tdpB = cpuB['tdp']

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
            recomendacion['motivo'] = f"Este procesador es recomendado para el perfil '{perfilUso}' debido a sus {cpuA['nucleos']} núcleos, {cpuA['hilos']} hilos y frecuencia turbo de {cpuA['frecuencia_turbo']} GHz."
        elif recomendacion['puntajeB'] > recomendacion['puntajeA']:
            recomendacion['ganador'] = cpuB['modelo']
            recomendacion['motivo'] = f"Este procesador es recomendado para el perfil '{perfilUso}' debido a sus {cpuB['nucleos']} núcleos, {cpuB['hilos']} hilos y frecuencia turbo de {cpuB['frecuencia_turbo']} GHz."
        else:
            recomendacion['ganador'] = "Empate Técnico"
            recomendacion['motivo'] = "Ambos procesadores cuentan con características equivalentes de rendimiento para este perfil de uso."

        return recomendacion

    # ═══════════════════════════════════════════════════════════════════════════
    # COMPARACIÓN DE GPUs
    # ═══════════════════════════════════════════════════════════════════════════
    def generarRecomendacionGPUs(self, idProductoA, idProductoB, perfilUso):
        gpuA = self.productoDao.obtenerGPUPorId(idProductoA)
        gpuB = self.productoDao.obtenerGPUPorId(idProductoB)

        if not gpuA or not gpuB:
            return {"success": False, "mensaje": "Uno de los productos no existe o no es una GPU."}

        preciosA = self.productoDao.obtenerPreciosProducto(idProductoA)
        preciosB = self.productoDao.obtenerPreciosProducto(idProductoB)

        recomendacion = {
            "success": True,
            "datosA": gpuA,
            "datosB": gpuB,
            "preciosA": preciosA,
            "preciosB": preciosB,
            "ganador": None,
            "motivo": "",
            "puntajeA": 0,
            "puntajeB": 0
        }

        # Sanitizar valores
        for gpu in [gpuA, gpuB]:
            if gpu:
                gpu['vram_gb'] = int(gpu.get('vram_gb') or 8)
                gpu['bus_bits'] = int(gpu.get('bus_bits') or 128)
                gpu['tdp_w'] = int(gpu.get('tdp_w') or 150)

        perfilLower = perfilUso.lower() if perfilUso else "general"
        perfilLower = perfilLower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

        # Scoring basado en VRAM (peso fuerte), bus y TDP
        if perfilLower in ['gaming', 'diseño']:
            # Gaming/Diseño: VRAM es rey, bus importa para ancho de banda
            recomendacion['puntajeA'] = (gpuA['vram_gb'] * 10) + (gpuA['bus_bits'] / 16) + (gpuA['tdp_w'] * 0.1)
            recomendacion['puntajeB'] = (gpuB['vram_gb'] * 10) + (gpuB['bus_bits'] / 16) + (gpuB['tdp_w'] * 0.1)
        elif perfilLower == 'ofimatica':
            # Ofimática: bajo consumo es prioritario, VRAM es secundaria
            recomendacion['puntajeA'] = (gpuA['vram_gb'] * 5) + (300 - gpuA['tdp_w']) * 0.5
            recomendacion['puntajeB'] = (gpuB['vram_gb'] * 5) + (300 - gpuB['tdp_w']) * 0.5
        else:
            # General: balance entre VRAM y consumo
            recomendacion['puntajeA'] = (gpuA['vram_gb'] * 8) + (gpuA['bus_bits'] / 16)
            recomendacion['puntajeB'] = (gpuB['vram_gb'] * 8) + (gpuB['bus_bits'] / 16)

        # Determinar ganador
        if recomendacion['puntajeA'] > recomendacion['puntajeB']:
            recomendacion['ganador'] = gpuA['modelo']
            motivos = []
            if gpuA['vram_gb'] > gpuB['vram_gb']:
                motivos.append(f"mayor VRAM ({gpuA['vram_gb']} GB vs {gpuB['vram_gb']} GB)")
            if gpuA['bus_bits'] > gpuB['bus_bits']:
                motivos.append(f"un bus de memoria más amplio ({gpuA['bus_bits']} bits vs {gpuB['bus_bits']} bits)")
            detalles = ", ".join(motivos) if motivos else "un mejor equilibrio de rendimiento general"
            recomendacion['motivo'] = f"Esta placa de video es recomendada para el perfil '{perfilUso}' porque ofrece {detalles}."
        elif recomendacion['puntajeB'] > recomendacion['puntajeA']:
            recomendacion['ganador'] = gpuB['modelo']
            motivos = []
            if gpuB['vram_gb'] > gpuA['vram_gb']:
                motivos.append(f"mayor VRAM ({gpuB['vram_gb']} GB vs {gpuA['vram_gb']} GB)")
            if gpuB['bus_bits'] > gpuA['bus_bits']:
                motivos.append(f"un bus de memoria más amplio ({gpuB['bus_bits']} bits vs {gpuA['bus_bits']} bits)")
            detalles = ", ".join(motivos) if motivos else "un mejor equilibrio de rendimiento general"
            recomendacion['motivo'] = f"Esta placa de video es recomendada para el perfil '{perfilUso}' porque ofrece {detalles}."
        else:
            recomendacion['ganador'] = "Empate Técnico"
            recomendacion['motivo'] = "Ambas placas de video ofrecen prestaciones equivalentes para este perfil de uso."

        return recomendacion

    # ═══════════════════════════════════════════════════════════════════════════
    # COMPARACIÓN DE RAM
    # ═══════════════════════════════════════════════════════════════════════════
    def generarRecomendacionRAMs(self, idProductoA, idProductoB, perfilUso):
        ramA = self.productoDao.obtenerRAMPorId(idProductoA)
        ramB = self.productoDao.obtenerRAMPorId(idProductoB)

        if not ramA or not ramB:
            return {"success": False, "mensaje": "Uno de los productos no existe o no es RAM."}

        preciosA = self.productoDao.obtenerPreciosProducto(idProductoA)
        preciosB = self.productoDao.obtenerPreciosProducto(idProductoB)

        recomendacion = {
            "success": True,
            "datosA": ramA,
            "datosB": ramB,
            "preciosA": preciosA,
            "preciosB": preciosB,
            "ganador": None,
            "motivo": "",
            "puntajeA": 0,
            "puntajeB": 0
        }

        # Sanitizar
        for ram in [ramA, ramB]:
            if ram:
                ram['capacidad_gb'] = int(ram.get('capacidad_gb') or 8)
                ram['velocidad_mhz'] = int(ram.get('velocidad_mhz') or 3200)
                ram['cantidad_modulos'] = int(ram.get('cantidad_modulos') or 1)
                ram['latencia'] = int(ram.get('latencia') or 0)

        perfilLower = perfilUso.lower() if perfilUso else "general"
        perfilLower = perfilLower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

        # Bonus dual channel
        bonoDualA = 10 if ramA['cantidad_modulos'] >= 2 else 0
        bonoDualB = 10 if ramB['cantidad_modulos'] >= 2 else 0

        if perfilLower == 'desarrollo de software':
            # Desarrollo: capacidad es prioridad absoluta
            recomendacion['puntajeA'] = (ramA['capacidad_gb'] * 5) + (ramA['velocidad_mhz'] / 100) + bonoDualA
            recomendacion['puntajeB'] = (ramB['capacidad_gb'] * 5) + (ramB['velocidad_mhz'] / 100) + bonoDualB
        elif perfilLower in ['gaming', 'diseño']:
            # Gaming: velocidad y dual channel importan más
            recomendacion['puntajeA'] = (ramA['capacidad_gb'] * 3) + (ramA['velocidad_mhz'] / 50) + bonoDualA * 2
            recomendacion['puntajeB'] = (ramB['capacidad_gb'] * 3) + (ramB['velocidad_mhz'] / 50) + bonoDualB * 2
        else:
            # General
            recomendacion['puntajeA'] = (ramA['capacidad_gb'] * 4) + (ramA['velocidad_mhz'] / 100) + bonoDualA
            recomendacion['puntajeB'] = (ramB['capacidad_gb'] * 4) + (ramB['velocidad_mhz'] / 100) + bonoDualB

        # Determinar ganador
        if recomendacion['puntajeA'] > recomendacion['puntajeB']:
            recomendacion['ganador'] = ramA['modelo']
            motivos = []
            if ramA['capacidad_gb'] > ramB['capacidad_gb']:
                motivos.append(f"mayor capacidad ({ramA['capacidad_gb']} GB vs {ramB['capacidad_gb']} GB)")
            if ramA['velocidad_mhz'] > ramB['velocidad_mhz']:
                motivos.append(f"mayor velocidad ({ramA['velocidad_mhz']} MHz vs {ramB['velocidad_mhz']} MHz)")
            detalles = ", ".join(motivos) if motivos else "un mejor equilibrio entre capacidad y velocidad"
            recomendacion['motivo'] = f"Esta memoria es recomendada para el perfil '{perfilUso}' porque ofrece {detalles}."
        elif recomendacion['puntajeB'] > recomendacion['puntajeA']:
            recomendacion['ganador'] = ramB['modelo']
            motivos = []
            if ramB['capacidad_gb'] > ramA['capacidad_gb']:
                motivos.append(f"mayor capacidad ({ramB['capacidad_gb']} GB vs {ramA['capacidad_gb']} GB)")
            if ramB['velocidad_mhz'] > ramA['velocidad_mhz']:
                motivos.append(f"mayor velocidad ({ramB['velocidad_mhz']} MHz vs {ramA['velocidad_mhz']} MHz)")
            detalles = ", ".join(motivos) if motivos else "un mejor equilibrio entre capacidad y velocidad"
            recomendacion['motivo'] = f"Esta memoria es recomendada para el perfil '{perfilUso}' porque ofrece {detalles}."
        else:
            recomendacion['ganador'] = "Empate Técnico"
            recomendacion['motivo'] = "Ambas memorias RAM ofrecen prestaciones equivalentes para este perfil de uso."

        return recomendacion

    # ═══════════════════════════════════════════════════════════════════════════
    # COMPARACIÓN DE ALMACENAMIENTO
    # ═══════════════════════════════════════════════════════════════════════════
    def generarRecomendacionAlmacenamiento(self, idProductoA, idProductoB, perfilUso):
        almA = self.productoDao.obtenerAlmacenamientoPorId(idProductoA)
        almB = self.productoDao.obtenerAlmacenamientoPorId(idProductoB)

        if not almA or not almB:
            return {"success": False, "mensaje": "Uno de los productos no existe o no es un dispositivo de almacenamiento."}

        preciosA = self.productoDao.obtenerPreciosProducto(idProductoA)
        preciosB = self.productoDao.obtenerPreciosProducto(idProductoB)

        recomendacion = {
            "success": True,
            "datosA": almA,
            "datosB": almB,
            "preciosA": preciosA,
            "preciosB": preciosB,
            "ganador": None,
            "motivo": "",
            "puntajeA": 0,
            "puntajeB": 0
        }

        # Sanitizar
        for alm in [almA, almB]:
            if alm:
                alm['capacidad_gb'] = int(alm.get('capacidad_gb') or 512)
                alm['velocidad_lectura'] = int(alm.get('velocidad_lectura') or 550)

        perfilLower = perfilUso.lower() if perfilUso else "general"
        perfilLower = perfilLower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

        # Bonus por tipo NVMe vs SATA
        def bonoTipo(tipo):
            if tipo and 'nvme' in tipo.lower():
                return 20
            elif tipo and 'ssd' in tipo.lower():
                return 10
            return 0

        bonoTipoA = bonoTipo(almA.get('tipo_disco', ''))
        bonoTipoB = bonoTipo(almB.get('tipo_disco', ''))

        if perfilLower in ['gaming', 'desarrollo de software']:
            # Velocidad es clave para gaming (carga de juegos) y desarrollo (compilación, Docker)
            recomendacion['puntajeA'] = (almA['capacidad_gb'] / 100) + (almA['velocidad_lectura'] / 50) + bonoTipoA
            recomendacion['puntajeB'] = (almB['capacidad_gb'] / 100) + (almB['velocidad_lectura'] / 50) + bonoTipoB
        elif perfilLower == 'ofimatica':
            # Ofimática: capacidad es más importante que velocidad
            recomendacion['puntajeA'] = (almA['capacidad_gb'] / 50) + (almA['velocidad_lectura'] / 200) + bonoTipoA
            recomendacion['puntajeB'] = (almB['capacidad_gb'] / 50) + (almB['velocidad_lectura'] / 200) + bonoTipoB
        else:
            # General
            recomendacion['puntajeA'] = (almA['capacidad_gb'] / 80) + (almA['velocidad_lectura'] / 100) + bonoTipoA
            recomendacion['puntajeB'] = (almB['capacidad_gb'] / 80) + (almB['velocidad_lectura'] / 100) + bonoTipoB

        # Determinar ganador
        if recomendacion['puntajeA'] > recomendacion['puntajeB']:
            recomendacion['ganador'] = almA['modelo']
            motivos = []
            if almA['capacidad_gb'] > almB['capacidad_gb']:
                motivos.append(f"mayor capacidad ({almA['capacidad_gb']} GB vs {almB['capacidad_gb']} GB)")
            if almA['velocidad_lectura'] > almB['velocidad_lectura']:
                motivos.append(f"mayor velocidad de lectura ({almA['velocidad_lectura']} MB/s vs {almB['velocidad_lectura']} MB/s)")
            detalles = ", ".join(motivos) if motivos else "un mejor equilibrio entre capacidad y velocidad"
            recomendacion['motivo'] = f"Este disco es recomendado para el perfil '{perfilUso}' porque ofrece {detalles}."
        elif recomendacion['puntajeB'] > recomendacion['puntajeA']:
            recomendacion['ganador'] = almB['modelo']
            motivos = []
            if almB['capacidad_gb'] > almA['capacidad_gb']:
                motivos.append(f"mayor capacidad ({almB['capacidad_gb']} GB vs {almA['capacidad_gb']} GB)")
            if almB['velocidad_lectura'] > almA['velocidad_lectura']:
                motivos.append(f"mayor velocidad de lectura ({almB['velocidad_lectura']} MB/s vs {almA['velocidad_lectura']} MB/s)")
            detalles = ", ".join(motivos) if motivos else "un mejor equilibrio entre capacidad y velocidad"
            recomendacion['motivo'] = f"Este disco es recomendado para el perfil '{perfilUso}' porque ofrece {detalles}."
        else:
            recomendacion['ganador'] = "Empate Técnico"
            recomendacion['motivo'] = "Ambos dispositivos de almacenamiento ofrecen prestaciones equivalentes para este perfil de uso."

        return recomendacion

    # guardarComparacion - Persiste una comparación entre dos productos en la BD
    def guardarComparacion(self, idUsuario, idProductoA, idProductoB, idCategoria=1):
        try:
            return self.comparacionDao.guardarComparacion(idUsuario, idProductoA, idProductoB, idCategoria)
        except Exception as e:
            print(f"// errorGuardarComparacionServicio: {e}")
            return False

    # obtenerComparacionesUsuario - Recupera el historial de comparaciones del usuario
    def obtenerComparacionesUsuario(self, idUsuario):
        try:
            return self.comparacionDao.obtenerComparacionesUsuario(idUsuario)
        except Exception as e:
            print(f"// errorObtenerHistorialServicio: {e}")
            return []

    # eliminarComparacion - Elimina una comparación guardada por su ID
    def eliminarComparacion(self, idComparacion):
        try:
            return self.comparacionDao.eliminarComparacion(idComparacion)
        except Exception as e:
            print(f"// errorEliminarComparacionServicio: {e}")
            return False
