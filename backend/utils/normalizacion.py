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
    cpu_modelo = "Intel Core i5"
    
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
