import os

def volcar_contenido_a_txt(ruta_raiz, archivo_salida):
    # Extensiones que queremos ignorar (archivos binarios, venv, etc.)
    ignorar = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.exe', '.bin', '.pdf', '.db'}
    carpetas_ignorar = {'venv', '__pycache__', '.git', '.vscode', 'node_modules'}

    with open(archivo_salida, 'w', encoding='utf-8') as f_salida:
        # os.walk recorre carpetas y subcarpetas automáticamente
        for raiz, carpetas, archivos in os.walk(ruta_raiz):
            
            # Filtrar carpetas a ignorar para no entrar en ellas
            carpetas[:] = [d for d in carpetas if d not in carpetas_ignorar]

            for nombre_archivo in archivos:
                # Verificar extensión
                _, ext = os.path.splitext(nombre_archivo)
                if ext.lower() in ignorar:
                    continue

                ruta_completa = os.path.join(raiz, nombre_archivo)
                
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f_lectura:
                        contenido = f_lectura.read()
                        
                    # Escribir encabezado y contenido en el .txt
                    f_salida.write(f"\n{'='*60}\n")
                    f_salida.write(f"RUTA: {ruta_completa}\n")
                    f_salida.write(f"ARCHIVO: {nombre_archivo}\n")
                    f_salida.write(f"{'='*60}\n\n")
                    f_salida.write(contenido)
                    f_salida.write("\n\n")
                    
                except Exception as e:
                    f_salida.write(f"\n[ERROR leyendo {nombre_archivo}: {e}]\n")

    print(f"¡Listo! Se ha generado el archivo: {archivo_salida}")

if __name__ == "__main__":
    # Usa '.' para la carpeta actual donde pongas el script
    directorio_actual = "."
    nombre_resultado = "resumen_proyecto.txt"
    volcar_contenido_a_txt(directorio_actual, nombre_resultado)