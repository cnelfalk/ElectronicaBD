import os

def generar_documento_txt(ruta_base: str, archivo_salida: str):
    """
    Recorre recursivamente una carpeta y concatena el contenido de archivos
    de texto/código en un único TXT.
    """

    extensiones = {
        ".py", ".json", ".js", ".jsx", ".ts", ".tsx",
        ".php", ".html", ".htm", ".css",
        ".sql", ".xml", ".yaml", ".yml",
        ".txt", ".md", ".ini", ".cfg",
        ".env", ".sh", ".bat"
    }

    separador = "\n" + "=" * 80 + "\n"

    with open(archivo_salida, "w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(ruta_base):

            # Ignorar carpetas comunes innecesarias
            dirs[:] = [
                d for d in dirs
                if d not in {
                    ".git",
                    "__pycache__",
                    "node_modules",
                    "venv",
                    ".venv"
                }
            ]

            for archivo in sorted(files):
                ruta_archivo = os.path.join(root, archivo)

                if os.path.splitext(archivo)[1].lower() in extensiones:

                    out_file.write(separador)
                    out_file.write(f"ARCHIVO: {ruta_archivo}\n")
                    out_file.write(separador)

                    try:
                        with open(ruta_archivo, "r", encoding="utf-8") as in_file:
                            out_file.write(in_file.read())
                    except UnicodeDecodeError:
                        try:
                            with open(ruta_archivo, "r", encoding="latin-1") as in_file:
                                out_file.write(in_file.read())
                        except Exception as e:
                            out_file.write(f"[ERROR AL LEER: {e}]")
                    except Exception as e:
                        out_file.write(f"[ERROR AL LEER: {e}]")

                    out_file.write("\n")

    print(f"Documento generado en: {archivo_salida}")


if __name__ == "__main__":
    ruta_base = os.getcwd()  # carpeta donde ejecutás el script
    generar_documento_txt(ruta_base, "codigo_fuente_completo.txt")