# test_bot.py
from scraper.scrapers_precios import MercadoLibreScraper

def probar_scraping():
    print("=== Iniciando Test de Bots ===")
    
    # Instanciamos el scraper de ML. 
    # id_tienda=2 corresponde a ML según tu schema.sql
    ml_bot = MercadoLibreScraper(id_tienda=2)
    
    # Ejecutamos la extracción
    datos_extraidos = ml_bot.extraer()
    
    print("\n=== Resultados Obtenidos ===")
    if not datos_extraidos:
        print("No se encontraron resultados. Verificá tu conexión o los selectores.")
        return

    for i, item in enumerate(datos_extraidos, 1):
        print(f"{i}. {item['modelo']}")
        print(f"   Precio: ${item['precio']:,.2f}")
        print(f"   Link: {item['url_producto']}")
        print("-" * 50)

if __name__ == "__main__":
    probar_scraping()