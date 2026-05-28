import datetime
from modelos.marca import Marca
from modelos.categoria import Categoria
from modelos.socket import Socket
from modelos.tienda import Tienda
from modelos.perfil_uso import PerfilUso
from modelos.producto_perfil import ProductoPerfil
from modelos.producto import Producto
from modelos.cpu import CPU
from modelos.laptop import Laptop
from modelos.gpu import GPU
from modelos.ram import RAM
from modelos.almacenamiento import Almacenamiento
from modelos.placa_madre import PlacaMadre
from modelos.comparacion_guardada import ComparacionGuardada
from modelos.usuario import Usuario

def verificar_modelos():
    print("=== INICIANDO VERIFICACIÓN DE MODELOS ===")
    
    # 1. Verificar Marca
    marca = Marca(1, "Intel", "https://intel.com")
    print(f"[OK] Marca instanciada: {marca.to_dict()}")

    # 2. Verificar Categoria
    categoria = Categoria(1, "CPU")
    print(f"[OK] Categoria instanciada: {categoria.to_dict()}")

    # 3. Verificar Socket
    socket = Socket(1, "LGA1700")
    print(f"[OK] Socket instanciado: {socket.to_dict()}")

    # 4. Verificar Tienda
    tienda = Tienda(1, "Compra Gamer", "https://compragamer.com")
    print(f"[OK] Tienda instanciada: {tienda.to_dict()}")

    # 5. Verificar PerfilUso
    perfil = PerfilUso(1, "gaming")
    print(f"[OK] PerfilUso instanciado: {perfil.to_dict()}")

    # 6. Verificar ProductoPerfil
    prod_perfil = ProductoPerfil(1, 100)
    print(f"[OK] ProductoPerfil instanciado: {prod_perfil.to_dict()}")

    # 7. Verificar Producto base
    prod = Producto(100, "Core i5-12400F", "https://img.url", "https://intel.com/i5", 1, 1)
    print(f"[OK] Producto base instanciado: {prod.to_dict()}")

    # 8. Verificar CPU (hereda de Producto)
    cpu = CPU(101, "Ryzen 5 5600X", "https://img.url", "https://amd.com/ryzen5", 1, 2, 6, 12, 3.7, 4.6, 65, 1)
    print(f"[OK] CPU instanciado (heredado): modelo={cpu.modeloProducto}, nucleos={cpu.nucleos}")

    # 9. Verificar Laptop (hereda de Producto, encapsula componentes)
    laptop = Laptop(102, "ThinkPad E14", "https://img.url", "https://lenovo.com", 2, 3, cpu, None, None, None, 1.6, 14.0, 60, 45)
    print(f"[OK] Laptop instanciada: modelo={laptop.modeloProducto}, cpu_modelo={laptop.cpu.modeloProducto}")

    # 10. Verificar GPU (hereda de Producto)
    gpu = GPU(103, "RTX 4060 Ti", "https://img.url", "https://nvidia.com", 3, 4, 1, 8, "GDDR6", 160)
    print(f"[OK] GPU instanciada: {gpu.to_dict()}")

    # 11. Verificar RAM (hereda de Producto)
    ram = RAM(104, "Vengeance LPX DDR4 16GB", "https://img.url", "https://corsair.com", 4, 5, 1, 16, 3200, 16, "DDR4")
    print(f"[OK] RAM instanciada: {ram.to_dict()}")

    # 12. Verificar Almacenamiento (hereda de Producto)
    almacenamiento = Almacenamiento(105, "Samsung 980 Pro 1TB", "https://img.url", "https://samsung.com", 5, 6, 1, 1000, "SSD", 7000, 5000)
    print(f"[OK] Almacenamiento instanciado: {almacenamiento.to_dict()}")

    # 13. Verificar PlacaMadre (hereda de Producto)
    placa = PlacaMadre(106, "ASUS TUF B550-PLUS", "https://img.url", "https://asus.com", 6, 1, 1, "ATX", "DDR4", 1)
    print(f"[OK] PlacaMadre instanciada: {placa.to_dict()}")

    # 14. Verificar ComparacionGuardada
    comparacion = ComparacionGuardada(1, datetime.datetime.now(), 1, 10, [101, 102])
    print(f"[OK] ComparacionGuardada instanciada: {comparacion.to_dict()}")

    # 15. Verificar Usuario
    usuario = Usuario(10, "Lucas", "lucas@example.com", "hash_pass")
    print(f"[OK] Usuario instanciado: id={usuario.idUsuario}, email={usuario.emailUsuario}")

    print("=== TODOS LOS MODELOS FUERON INSTANCIADOS CORRECTAMENTE ===")

if __name__ == "__main__":
    verificar_modelos()
