import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.conexion import ConexionDB
from scrapers.scraper_imagenes import ScraperImagenes

def main():
    conn = ConexionDB.obtenerInstancia()
    if not conn:
        print("Error: No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor()
    try:
        # Clear ML images
        cursor.execute("""
            UPDATE productos 
            SET img_url = '' 
            WHERE img_url LIKE '%mlstatic.com%' OR img_url LIKE '%mercadolibre%'
        """)
        conn.commit()
        print(f"Base de datos limpia: Se borraron {cursor.rowcount} imagenes de Mercado Libre antiguas.")
        
        # Start ScraperImagenes to fetch professional ones
        print("Iniciando ScraperImagenes con filtros profesionales...")
        scraper = ScraperImagenes()
        scraper.ejecutarScraping()
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    main()
