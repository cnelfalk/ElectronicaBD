import os
import sys

# Definición del Diagrama en PlantUML (estándar de UML)
PLANTUML_DIAGRAM = """@startuml
left to right direction
skinparam packageStyle rectangle
skinparam roundCorner 10
skinparam actor {
    BackgroundColor #6366f1
    BorderColor #4f46e5
    FontColor #1e293b
}
skinparam usecase {
    BackgroundColor #ffffff
    BorderColor #334155
    ArrowColor #6366f1
}
skinparam rectangle {
    BackgroundColor #f8fafc
    BorderColor #cbd5e1
}

actor "Visitante\\n(Anónimo)" as Guest
actor "Usuario Registrado" as User
actor "Sistema / Cron\\n(Orquestador)" as System

User --|> Guest

rectangle "TechMatch (Sistema de Comparación de Hardware)" {
    usecase "Buscar productos" as UC1
    usecase "Filtrar catálogo\\n(Categoría o Perfil)" as UC2
    usecase "Ver ficha de producto\\ny ofertas de precios" as UC3
    usecase "Comparar productos\\n(Veredicto por perfil)" as UC4
    usecase "Registrarse / Iniciar Sesión" as UC5
    usecase "Recuperar contraseña" as UC5_1
    
    usecase "Gestionar favoritos\\n(Agregar / Quitar)" as UC6
    usecase "Ver lista de favoritos" as UC7
    usecase "Ver historial de\\ncomparaciones guardadas" as UC8
    usecase "Cerrar sesión" as UC9
    
    usecase "Ejecutar scraping diario\\n(run_bots.py)" as UC10
    usecase "Extraer especificaciones\\nde fabricantes" as UC10_1
    usecase "Extraer precios e imágenes\\nde retailers" as UC10_2
    usecase "Normalizar términos técnicos\\n(normalizacion.py)" as UC11
    usecase "Validar compatibilidad\\nde componentes (validacion.py)" as UC12
    usecase "Actualizar base de datos\\n(MySQL)" as UC13
}

Guest --> UC1
Guest --> UC2
Guest --> UC3
Guest --> UC4
Guest --> UC5
Guest --> UC5_1

User --> UC6
User --> UC7
User --> UC8
User --> UC9

System --> UC10
System --> UC12
System --> UC13

UC10 ..> UC10_1 : <<include>>
UC10 ..> UC10_2 : <<include>>
UC10 ..> UC11 : <<include>>
@enduml
"""

MERMAID_DIAGRAM = """flowchart TD
    %% Actors
    Visitante["👤 Visitante (Anónimo)"]
    Usuario["👤 Usuario Registrado"]
    Sistema["⚙️ Sistema / Cron (Orquestador)"]

    %% Inheritance (simulado)
    Usuario -.->|Hereda de| Visitante

    subgraph TechMatch ["TechMatch (Sistema de Comparación de Hardware)"]
        %% Use Cases for Guest
        UC1(["Buscar productos"])
        UC2(["Filtrar catálogo\\n(Categoría o Perfil de Uso)"])
        UC3(["Ver ficha técnica de producto\\ny ofertas de precios"])
        UC4(["Comparar productos side-by-side\\n(con veredicto)"])
        UC5(["Registrarse / Iniciar Sesión"])
        UC5_1(["Recuperar contraseña"])

        %% Use Cases for Registered
        UC6(["Gestionar favoritos\\n(Agregar o Quitar)"])
        UC7(["Ver lista de favoritos"])
        UC8(["Ver historial de comparaciones"])
        UC9(["Cerrar sesión"])

        %% Use Cases for System / Cron
        UC10(["Ejecutar scraping diario"])
        UC10_1(["Extraer especificaciones\\nde fabricantes"])
        UC10_2(["Extraer precios e imágenes\\nde retailers"])
        UC11(["Normalizar especificaciones\\ny términos técnicos"])
        UC12(["Validar compatibilidad\\nde componentes"])
        UC13(["Actualizar base de datos\\n(catálogo y ofertas)"])
    end

    %% Connections
    Visitante --> UC1
    Visitante --> UC2
    Visitante --> UC3
    Visitante --> UC4
    Visitante --> UC5
    Visitante --> UC5_1

    Usuario --> UC6
    Usuario --> UC7
    Usuario --> UC8
    Usuario --> UC9

    Sistema --> UC10
    Sistema --> UC12
    Sistema --> UC13

    UC10 -.->|&lt;&lt;include&gt;&gt;| UC10_1
    UC10 -.->|&lt;&lt;include&gt;&gt;| UC10_2
    UC10 -.->|&lt;&lt;include&gt;&gt;| UC11
"""

# HTML Template con Mermaid integrado
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch - Diagrama de Casos de Uso</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg-color: #0f172a;
            --panel-bg: #1e293b;
            --text-color: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-color: #6366f1;
            --accent-hover: #4f46e5;
            --border-color: #334155;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        header {{
            text-align: center;
            margin-bottom: 30px;
            max-width: 800px;
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0 0 10px 0;
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        p {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            line-height: 1.6;
            margin: 0;
        }}
        .container {{
            width: 95%;
            max-width: 1200px;
            background-color: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .mermaid {{
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            width: 100%;
            overflow-x: auto;
            display: flex;
            justify-content: center;
            box-sizing: border-box;
        }}
        .footer {{
            margin-top: 40px;
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-align: center;
        }}
        .actions {{
            margin-top: 25px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .btn {{
            background-color: var(--accent-color);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }}
        .btn:hover {{
            background-color: var(--accent-hover);
            transform: translateY(-2px);
        }}
        .btn-secondary {{
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
        }}
        .btn-secondary:hover {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
    </style>
</head>
<body>
    <header>
        <h1>Diagrama de Casos de Uso - TechMatch</h1>
        <p>Este diagrama interactivo ilustra la relación de los actores y los casos de uso definidos en la arquitectura del sistema.</p>
    </header>

    <div class="container">
        <div class="mermaid">
            %%{{init: {{'theme': 'default', 'themeVariables': {{ 'fontSize': '16px' }} }} }}%%
{mermaid_code}
        </div>

        <div class="actions">
            <button class="btn" onclick="window.print()">Imprimir / Guardar PDF</button>
            <a href="diagrama_casos_uso.png" class="btn btn-secondary" target="_blank">Ver Imagen PNG</a>
            <a href="diagrama_casos_uso.puml" class="btn btn-secondary" download>Descargar PlantUML (.puml)</a>
            <a href="diagrama_casos_uso.mmd" class="btn btn-secondary" download>Descargar Mermaid (.mmd)</a>
        </div>
    </div>

    <div class="footer">
        Desarrollado para TechMatch • Generado automáticamente por Python Utility.
    </div>

    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>
"""

def main():
    print("=== Generador de Diagrama de Casos de Uso de TechMatch ===")
    
    # 1. Escribir archivo PlantUML (.puml)
    puml_filename = "diagrama_casos_uso.puml"
    try:
        with open(puml_filename, "w", encoding="utf-8") as f:
            f.write(PLANTUML_DIAGRAM)
        print(f"[OK] Guardado archivo PlantUML en: {puml_filename}")
    except Exception as e:
        print(f"[ERROR] Al guardar PlantUML: {e}")

    # 2. Escribir archivo Mermaid (.mmd)
    mmd_filename = "diagrama_casos_uso.mmd"
    try:
        with open(mmd_filename, "w", encoding="utf-8") as f:
            f.write(MERMAID_DIAGRAM)
        print(f"[OK] Guardado archivo Mermaid en: {mmd_filename}")
    except Exception as e:
        print(f"[ERROR] Al guardar Mermaid: {e}")

    # 3. Escribir archivo HTML interactivo
    html_filename = "diagrama_casos_uso.html"
    try:
        html_content = HTML_TEMPLATE.format(mermaid_code=MERMAID_DIAGRAM)
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[OK] Guardado archivo HTML en: {html_filename}")
    except Exception as e:
        print(f"[ERROR] Al guardar HTML: {e}")

    # 4. Renderizar y descargar PNG usando la API pública de Kroki (con PlantUML)
    png_filename = "diagrama_casos_uso.png"
    print("[...] Intentando renderizar diagrama PlantUML a PNG mediante Kroki...")
    
    try:
        import requests
        
        # Enviamos el código raw PlantUML al endpoint de Kroki
        url = "https://kroki.io/plantuml/png"
        headers = {"Content-Type": "text/plain; charset=utf-8"}
        
        response = requests.post(url, data=PLANTUML_DIAGRAM.encode('utf-8'), headers=headers, timeout=10)
        
        if response.status_code == 200:
            with open(png_filename, "wb") as f:
                f.write(response.content)
            print(f"[OK] Imagen PNG descargada exitosamente en: {png_filename}")
        else:
            print(f"[ERROR] Kroki retorno estado de error {response.status_code}: {response.text}")
            print("(!) Sugerencia: Puedes abrir el archivo HTML generado para ver el diagrama.")
            
    except ImportError:
        print("[WARN] No se encontro el modulo 'requests' para hacer la llamada a Kroki.")
        print("    Para instalarlo ejecuta: pip install requests")
        print("    O puedes usar el entorno virtual: venv\\Scripts\\activate y correr el script.")
    except Exception as e:
        print(f"[ERROR] Ocurrio un error al contactar a la API de Kroki: {e}")
        print("(!) El archivo HTML y los fuentes se crearon correctamente, por lo que puedes utilizarlos.")

    print("\nProceso finalizado. Archivos generados:")
    print(f" - Fuente PlantUML: {os.path.abspath(puml_filename)}")
    print(f" - Fuente Mermaid:  {os.path.abspath(mmd_filename)}")
    print(f" - Vista HTML:     {os.path.abspath(html_filename)}")
    if os.path.exists(png_filename):
        print(f" - Imagen PNG:     {os.path.abspath(png_filename)}")

if __name__ == "__main__":
    main()
