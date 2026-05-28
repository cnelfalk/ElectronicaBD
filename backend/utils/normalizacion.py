import re
import unicodedata

def limpiar_texto(texto):
    if not texto:
        return ""
    # Normalizar diacríticos (remover acentos)
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    # Convertir a minúsculas
    texto = texto.lower()
    # Mantener alfanuméricos, espacios, guiones y barras diagonales
    texto = re.sub(r'[^a-z0-9\s\-/]', ' ', texto)
    # Limpiar espacios múltiples
    texto = ' '.join(texto.split())
    return texto

def coincide_modelo(nombre_retail, nombre_oficial):
    retail_clean = limpiar_texto(nombre_retail)
    oficial_clean = limpiar_texto(nombre_oficial)
    
    stop_words = {
        'notebook', 'laptop', 'pc', 'computadora', 'gamer', 'gaming', 'ssd', 
        'ram', 'gb', 'tb', 'windows', 'home', 'pro', 'intel', 'amd', 'nvidia', 
        'geforce', 'rtx', 'gtx', 'radeon', 'generacion', 'gen', 'hz', 'display', 
        'pantalla', 'screen', 'silver', 'grey', 'gray', 'black', 'white', 
        'azul', 'negro', 'gris', 'plata', 'wifi', 'bluetooth', 'camara', 
        'camera', 'keyboard', 'teclado', 'mouse', 'bateria', 'battery', 
        'con', 'para', 'de', 'del', 'la', 'el', 'en', 'y'
    }
    
    palabras_retail = [w for w in retail_clean.split() if w not in stop_words]
    palabras_oficial = [w for w in oficial_clean.split() if w not in stop_words]
    
    if not palabras_oficial:
        return False
        
    coincidentes = 0
    for wo in palabras_oficial:
        match_found = False
        for wr in palabras_retail:
            if wo == wr:
                match_found = True
                break
            # Si es un código alfanumérico (ej: longitud >= 3), verificar subcadenas
            if len(wo) >= 3 and len(wr) >= 3:
                if wo in wr or wr in wo:
                    match_found = True
                    break
        if match_found:
            coincidentes += 1
            
    total_oficial = len(palabras_oficial)
    if total_oficial <= 2:
        return coincidentes == total_oficial
    else:
        porcentaje = coincidentes / total_oficial
        return porcentaje >= 0.75

def extraer_specs_de_titulo(titulo):
    titulo_lower = titulo.lower()
    
    # Valores por defecto
    ram = 8
    almacenamiento = 256
    cpu_modelo = "Desconocido"
    
    # 1. Extraer RAM
    ram_match = re.search(r'\b(4|8|12|16|24|32|64)\s*(?:gb|g)\s*(?:ram|ddr\d)?\b', titulo_lower)
    if ram_match:
        ram = int(ram_match.group(1))
    
    # 2. Extraer Almacenamiento
    tb_match = re.search(r'\b([1-2])\s*(?:tb|tera|terabyte)\b', titulo_lower)
    if tb_match:
        almacenamiento = int(tb_match.group(1)) * 1024
    else:
        storage_match = re.search(r'\b(120|128|240|256|480|500|512|960|1000|1024)\s*(?:gb|g)\b', titulo_lower)
        if storage_match:
            almacenamiento = int(storage_match.group(1))
        else:
            alt_storage = re.search(r'\b(\d+)\s*(?:gb)?\s*(?:ssd|hdd|nvme|m\.2)\b', titulo_lower)
            if alt_storage:
                val = int(alt_storage.group(1))
                if val in [1, 2]:
                    almacenamiento = val * 1024
                elif val >= 120 and val <= 4096:
                    almacenamiento = val
                    
    # 3. Extraer Familia de CPU
    if "ryzen 9" in titulo_lower or "r9" in titulo_lower:
        cpu_modelo = "AMD Ryzen 9"
    elif "ryzen 7" in titulo_lower or "r7" in titulo_lower:
        cpu_modelo = "AMD Ryzen 7"
    elif "ryzen 5" in titulo_lower or "r5" in titulo_lower:
        cpu_modelo = "AMD Ryzen 5"
    elif "ryzen 3" in titulo_lower or "r3" in titulo_lower:
        cpu_modelo = "AMD Ryzen 3"
    elif "ryzen" in titulo_lower:
        cpu_modelo = "AMD Ryzen 5"
    elif "core i9" in titulo_lower or "i9" in titulo_lower:
        cpu_modelo = "Intel Core i9"
    elif "core i7" in titulo_lower or "i7" in titulo_lower:
        cpu_modelo = "Intel Core i7"
    elif "core i5" in titulo_lower or "i5" in titulo_lower:
        cpu_modelo = "Intel Core i5"
    elif "core i3" in titulo_lower or "i3" in titulo_lower:
        cpu_modelo = "Intel Core i3"
    elif "celeron" in titulo_lower:
        cpu_modelo = "Intel Celeron"
    elif "pentium" in titulo_lower:
        cpu_modelo = "Intel Pentium"
    elif "athlon" in titulo_lower:
        cpu_modelo = "AMD Athlon"
        
    return {
        'ram': ram,
        'almacenamiento': almacenamiento,
        'cpu_modelo': cpu_modelo
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE EXTRACCIÓN DE SPECS PARA GPU, RAM Y ALMACENAMIENTO
# Extraen datos técnicos desde los títulos de productos scrapeados por retailers.
# Se usan en ProductoDAO.upsertProductoRetail() cuando el producto es nuevo.
# ═══════════════════════════════════════════════════════════════════════════════

def extraer_specs_gpu(titulo):
    """
    Extrae especificaciones técnicas de una GPU a partir del título del producto.
    Retorna un dict con: vram_gb, tipo_memoria, bus_bits, tdp_w, familia.
    """
    t = titulo.lower()

    # VRAM (ej: "8gb", "12 gb", "16gb gddr6")
    vram = 8  # default
    vram_match = re.search(r'\b(\d{1,2})\s*gb', t)
    if vram_match:
        val = int(vram_match.group(1))
        if val in [2, 3, 4, 6, 8, 10, 12, 16, 24]:
            vram = val

    # Tipo de memoria (GDDR5, GDDR6, GDDR6X)
    tipo_memoria = "GDDR6"
    if "gddr6x" in t:
        tipo_memoria = "GDDR6X"
    elif "gddr5" in t:
        tipo_memoria = "GDDR5"
    elif "gddr6" in t:
        tipo_memoria = "GDDR6"

    # Bus de memoria (128, 192, 256, 384 bits)
    bus_bits = 128
    bus_match = re.search(r'\b(64|128|192|256|384)\s*(?:bits?|bit)\b', t)
    if bus_match:
        bus_bits = int(bus_match.group(1))
    else:
        # Estimar bus por VRAM: regla general
        if vram >= 16:
            bus_bits = 256
        elif vram >= 10:
            bus_bits = 192
        elif vram >= 8:
            bus_bits = 128

    # TDP estimado por modelo
    tdp = 150  # default
    if "4090" in t:
        tdp = 450
    elif "4080" in t:
        tdp = 320
    elif "4070 ti" in t:
        tdp = 285
    elif "4070" in t:
        tdp = 200
    elif "4060 ti" in t:
        tdp = 160
    elif "4060" in t:
        tdp = 115
    elif "3090" in t:
        tdp = 350
    elif "3080" in t:
        tdp = 320
    elif "3070" in t:
        tdp = 220
    elif "3060 ti" in t:
        tdp = 200
    elif "3060" in t:
        tdp = 170
    elif "7900 xtx" in t:
        tdp = 355
    elif "7900 xt" in t:
        tdp = 315
    elif "7800 xt" in t:
        tdp = 263
    elif "7700 xt" in t:
        tdp = 245
    elif "7600" in t:
        tdp = 165

    # Familia de GPU (para scoring)
    familia = "Desconocida"
    if any(k in t for k in ["rtx 4090", "rtx 4080"]):
        familia = "NVIDIA High-End"
    elif any(k in t for k in ["rtx 4070", "rtx 3080", "rtx 3070", "7900"]):
        familia = "NVIDIA/AMD High"
    elif any(k in t for k in ["rtx 4060", "rtx 3060", "7800", "7700"]):
        familia = "Mid-Range"
    elif any(k in t for k in ["rtx 3050", "1650", "1660", "7600", "6600"]):
        familia = "Entry Gaming"
    elif any(k in t for k in ["gt 1030", "gt 730", "rx 550", "rx 6400"]):
        familia = "Entry"

    return {
        'vram_gb': vram,
        'tipo_memoria': tipo_memoria,
        'bus_bits': bus_bits,
        'tdp_w': tdp,
        'familia': familia
    }


def extraer_specs_ram(titulo):
    """
    Extrae especificaciones técnicas de un módulo RAM a partir del título del producto.
    Retorna un dict con: capacidad_gb, tipo_memoria, velocidad_mhz, cantidad_modulos, latencia.
    """
    t = titulo.lower()

    # Capacidad total (ej: "16gb", "32 gb", "2x8gb")
    capacidad = 8  # default
    # Patrón kit: 2x8gb, 2x16gb
    kit_match = re.search(r'(\d)\s*x\s*(\d{1,2})\s*gb', t)
    if kit_match:
        modulos = int(kit_match.group(1))
        por_modulo = int(kit_match.group(2))
        capacidad = modulos * por_modulo
    else:
        cap_match = re.search(r'\b(\d{1,3})\s*gb\b', t)
        if cap_match:
            val = int(cap_match.group(1))
            if val in [4, 8, 16, 32, 64, 128]:
                capacidad = val

    # Cantidad de módulos
    cantidad_modulos = 1
    if kit_match:
        cantidad_modulos = int(kit_match.group(1))
    elif "dual" in t or "kit" in t:
        cantidad_modulos = 2

    # Tipo de memoria (DDR4, DDR5)
    tipo = "DDR4"
    if "ddr5" in t:
        tipo = "DDR5"
    elif "ddr4" in t:
        tipo = "DDR4"
    elif "ddr3" in t:
        tipo = "DDR3"

    # Velocidad en MHz (ej: "3200mhz", "4800 mhz", "6000mhz")
    velocidad = 3200  # default DDR4
    vel_match = re.search(r'(\d{4,5})\s*mhz', t)
    if vel_match:
        velocidad = int(vel_match.group(1))
    else:
        # Defaults por tipo
        if tipo == "DDR5":
            velocidad = 4800
        elif tipo == "DDR3":
            velocidad = 1600

    # Latencia CAS (ej: "cl16", "cl18", "c36")
    latencia = None
    lat_match = re.search(r'c(?:l|as)?\s*(\d{2})', t)
    if lat_match:
        latencia = int(lat_match.group(1))

    return {
        'capacidad_gb': capacidad,
        'tipo_memoria': tipo,
        'velocidad_mhz': velocidad,
        'cantidad_modulos': cantidad_modulos,
        'latencia': latencia
    }


def extraer_specs_almacenamiento(titulo):
    """
    Extrae especificaciones de un dispositivo de almacenamiento (SSD/HDD) 
    a partir del título del producto.
    Retorna un dict con: capacidad_gb, tipo_disco, interfaz, velocidad_lectura, formato.
    """
    t = titulo.lower()

    # Capacidad (ej: "1tb", "500gb", "2 tb", "240gb")
    capacidad = 512  # default
    tb_match = re.search(r'\b(\d{1,2})\s*tb\b', t)
    if tb_match:
        capacidad = int(tb_match.group(1)) * 1024
    else:
        gb_match = re.search(r'\b(\d{3,4})\s*gb\b', t)
        if gb_match:
            val = int(gb_match.group(1))
            if 120 <= val <= 4096:
                capacidad = val

    # Tipo de disco (SSD, HDD, NVMe)
    tipo = "SSD"
    if "nvme" in t or "m.2" in t or "pcie" in t:
        tipo = "SSD NVMe"
    elif "hdd" in t or "mecanico" in t or "7200" in t or "5400" in t:
        tipo = "HDD"
    elif "sata" in t and "ssd" in t:
        tipo = "SSD SATA"
    elif "ssd" in t:
        tipo = "SSD"

    # Interfaz
    interfaz = "SATA III"
    if "nvme" in t or "pcie" in t or "m.2" in t:
        interfaz = "PCIe NVMe"
        if "gen4" in t or "gen 4" in t or "pcie 4" in t:
            interfaz = "PCIe 4.0 NVMe"
        elif "gen5" in t or "gen 5" in t or "pcie 5" in t:
            interfaz = "PCIe 5.0 NVMe"
        elif "gen3" in t or "gen 3" in t or "pcie 3" in t:
            interfaz = "PCIe 3.0 NVMe"
    elif "sata" in t:
        interfaz = "SATA III"

    # Velocidad de lectura estimada (MB/s)
    vel_lectura = 550  # default SATA
    vel_match = re.search(r'(\d{3,5})\s*mb/?s', t)
    if vel_match:
        vel_lectura = int(vel_match.group(1))
    elif "nvme" in t or "pcie" in t:
        # Defaults por generación PCIe
        if "gen5" in t or "gen 5" in t:
            vel_lectura = 10000
        elif "gen4" in t or "gen 4" in t:
            vel_lectura = 5000
        elif "gen3" in t or "gen 3" in t:
            vel_lectura = 3500
        else:
            vel_lectura = 3500

    # Formato (2.5", M.2, 3.5")
    formato = "2.5\""
    if "m.2" in t or "m2" in t or "nvme" in t:
        formato = "M.2 2280"
    elif "3.5" in t:
        formato = "3.5\""

    return {
        'capacidad_gb': capacidad,
        'tipo_disco': tipo,
        'interfaz': interfaz,
        'velocidad_lectura': vel_lectura,
        'formato': formato
    }
