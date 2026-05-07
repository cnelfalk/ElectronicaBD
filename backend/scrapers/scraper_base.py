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

    def _crearDriver(self):
        opciones = Options()
        opciones.add_argument('--headless')
        opciones.add_argument('--disable-gpu')
        opciones.add_argument('--no-sandbox')
        opciones.add_argument('--disable-dev-shm-usage')
        opciones.add_argument(f'user-agent={self.userAgent}')
        servicio = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=servicio, options=opciones)

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
