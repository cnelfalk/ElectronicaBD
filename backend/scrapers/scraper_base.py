import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import time
import random
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dao.producto_dao import ProductoDAO


class ScraperBase(ABC):
    def __init__(self, marca):
        self.marca = marca
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        self.headers = {'User-Agent': self.userAgent}
        self.dao = ProductoDAO()

    @abstractmethod
    def ejecutarScraping(self):
        pass

    def _limpiarLocksWdm(self):
        try:
            home = os.path.expanduser("~")
            wdm_dir = os.path.join(home, ".wdm")
            if os.path.exists(wdm_dir):
                import glob
                lock_files = glob.glob(os.path.join(wdm_dir, "*lock*")) + glob.glob(os.path.join(wdm_dir, ".*lock*"))
                for lf in lock_files:
                    if os.path.isfile(lf):
                        try:
                            os.remove(lf)
                            print(f"  [WDM] Eliminado archivo de bloqueo residual: {lf}")
                        except Exception as re:
                            print(f"  [WDM] No se pudo remover {lf}: {re}")
        except Exception as e:
            print(f"  [WDM] Advertencia al limpiar archivos de bloqueo: {e}")

    def _crearDriver(self):
        self._limpiarLocksWdm()
        opciones = Options()
        opciones.add_argument('--headless')
        opciones.add_argument('--disable-gpu')
        opciones.add_argument('--no-sandbox')
        opciones.add_argument('--disable-dev-shm-usage')
        opciones.add_argument('--window-size=1920,1080')
        opciones.add_argument('--disable-http2')
        opciones.add_argument(f'user-agent={self.userAgent}')
        
        # Anti-detect options to bypass bot protection / CAPTCHAs
        opciones.add_argument('--disable-blink-features=AutomationControlled')
        opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
        opciones.add_experimental_option('useAutomationExtension', False)
        
        # Priorizar Selenium Manager nativo (no crea archivos .wdm-lock)
        try:
            driver = webdriver.Chrome(options=opciones)
        except Exception as e:
            print(f"  [WDM] Selenium Manager nativo fallo: {e}")
            print("  [WDM] Intentando con ChromeDriverManager como fallback...")
            try:
                servicio = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=servicio, options=opciones)
            except Exception as fe:
                print(f"  [WDM] Fallo critico al iniciar WebDriver: {fe}")
                raise fe

        # Remove webdriver signature via CDP command
        try:
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            })
        except Exception as cdpe:
            print(f"  [WDM] Advertencia al configurar comando CDP: {cdpe}")

        return driver

    def _esperar(self, minSeg=1, maxSeg=3):
        time.sleep(random.uniform(minSeg, maxSeg))

    def extraerSpecsDeTexto(self, titulo):
        specs = {
            "ramGb": 8,
            "almacenamientoGb": 256,
            "cpuModelo": "Desconocido",
            "gpuModelo": "Integrada"
        }

        t = titulo.lower()

        matchRam = re.search(r'(\d+)\s*gb\s*ram?', t)
        if matchRam:
            specs["ramGb"] = int(matchRam.group(1))

        matchAlm = re.search(r'(\d+)\s*(gb|tb)\s*(ssd|hdd|nvme)', t)
        if matchAlm:
            valor = int(matchAlm.group(1))
            specs["almacenamientoGb"] = valor * 1000 if matchAlm.group(2) == 'tb' else valor

        if   "ryzen 9" in t: specs["cpuModelo"] = "AMD Ryzen 9"
        elif "ryzen 7" in t: specs["cpuModelo"] = "AMD Ryzen 7"
        elif "ryzen 5" in t: specs["cpuModelo"] = "AMD Ryzen 5"
        elif "ryzen 3" in t: specs["cpuModelo"] = "AMD Ryzen 3"
        elif "core i9" in t: specs["cpuModelo"] = "Intel Core i9"
        elif "core i7" in t: specs["cpuModelo"] = "Intel Core i7"
        elif "core i5" in t: specs["cpuModelo"] = "Intel Core i5"
        elif "core i3" in t: specs["cpuModelo"] = "Intel Core i3"

        if   "rtx 4090" in t: specs["gpuModelo"] = "NVIDIA RTX 4090"
        elif "rtx 4080" in t: specs["gpuModelo"] = "NVIDIA RTX 4080"
        elif "rtx 4070" in t: specs["gpuModelo"] = "NVIDIA RTX 4070"
        elif "rtx 4060" in t: specs["gpuModelo"] = "NVIDIA RTX 4060"
        elif "rtx 3080" in t: specs["gpuModelo"] = "NVIDIA RTX 3080"
        elif "rtx 3070" in t: specs["gpuModelo"] = "NVIDIA RTX 3070"
        elif "rtx 3060" in t: specs["gpuModelo"] = "NVIDIA RTX 3060"
        elif "rx 7900"  in t: specs["gpuModelo"] = "AMD RX 7900"
        elif "rx 7800"  in t: specs["gpuModelo"] = "AMD RX 7800"
        elif "rx 7600"  in t: specs["gpuModelo"] = "AMD RX 7600"

        return specs
