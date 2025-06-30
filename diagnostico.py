import psutil
import platform
import time

# 1. Información del sistema operativo
def mostrar_informacion_os():
    uname = platform.uname()
    print("\n=== Información del sistema ===")
    print(f"Sistema operativo: {uname.system} {uname.release}")
    print(f"Versión: {uname.version}")
    print(f"Nombre del dispositivo: {uname.node}")
    print(f"Arquitectura: {uname.machine}")
    print(f"Procesador: {uname.processor}")

# 2. Información de la CPU
def mostrar_informacion_cpu():
    print("\n=== Información de la CPU ===")
    print(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"Núcleos lógicos: {psutil.cpu_count(logical=True)}")
    print(f"Porcentaje de uso de CPU: {psutil.cpu_percent(interval=1)}%")

# 3. Información de la memoria RAM
def mostrar_informacion_memoria():
    mem = psutil.virtual_memory()
    print("\n=== Información de la memoria ===")
    print(f"Memoria total: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Memoria disponible: {mem.available / (1024 ** 3):.2f} GB")
    print(f"Porcentaje de uso: {mem.percent}%")

# 4. Información de los discos
def mostrar_informacion_discos():
    print("\n=== Información de los discos ===")
    for disco in psutil.disk_partitions():
        print(f"Disco: {disco.device} ({disco.mountpoint})")
        try:
            uso = psutil.disk_usage(disco.mountpoint)
            print(f"  Total: {uso.total / (1024 ** 3):.2f} GB")
            print(f"  Usado: {uso.used / (1024 ** 3):.2f} GB")
            print(f"  Libre: {uso.free / (1024 ** 3):.2f} GB")
            print(f"  Porcentaje de uso: {uso.percent}%")
        except PermissionError:
            print("  No se pudo acceder a la información de este disco.")

# 5. Validador de dirección IP
def checker_ip(ip_address):
    try:
        separated_address = ip_address.strip().split('.')
        if len(separated_address) != 4:
            return False
        for i in separated_address:
            if not i.isdigit() or not (0 <= int(i) <= 255):
                return False
        return True
    except:
        return False

# 6. Top procesos por uso de CPU
def mostrar_top_procesos_cpu(top_n=5):
    print(f"\n=== Top {top_n} procesos por uso de CPU ===")
    procesos = []
    # Inicializa la medición de uso de CPU
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # Espera un segundo para obtener datos reales
    time.sleep(1)
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procesos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # Ordena por uso de CPU descendente
    procesos = sorted(procesos, key=lambda p: p['cpu_percent'], reverse=True)
    for proc in procesos[:top_n]:
        print(f"PID: {proc['pid']}\tCPU: {proc['cpu_percent']}%\tNombre: {proc['name']}")

# 7. Información de red
def mostrar_info_red():
    print("\n=== Interfaces de red activas ===")
    addrs = psutil.net_if_addrs()
    stats = psutil.net_io_counters(pernic=True)
    for interfaz, direcciones in addrs.items():
        print(f"\nInterfaz: {interfaz}")
        for direccion in direcciones:
            if direccion.family == psutil.AF_LINK:
                continue  # omite direcciones MAC
            if direccion.family == 2:  # IPv4
                print(f"  Dirección IP: {direccion.address}")
            elif direccion.family == 10:  # IPv6
                print(f"  Dirección IPv6: {direccion.address}")
        if interfaz in stats:
            print(f"  Bytes enviados: {stats[interfaz].bytes_sent}")
            print(f"  Bytes recibidos: {stats[interfaz].bytes_recv}")

def menu():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Información del ordenador")
        print("2. IP Scanner (validador de IP)")
        print("3. Top procesos por uso de CPU")
        print("4. Información de red")
        print("5. Salir")
        opcion = input("Elige una opción (1-5): ").strip()
        
        if opcion == "1":
            mostrar_informacion_os()
            mostrar_informacion_cpu()
            mostrar_informacion_memoria()
            mostrar_informacion_discos()
        elif opcion == "2":
            user_in = input("Introduce la dirección IP: ")
            if checker_ip(user_in):
                print(f"¡Correcto! {user_in} es una dirección IP válida.")
            else:
                print(f"¡Error! {user_in} NO es una dirección IP válida.")
        elif opcion == "3":
            mostrar_top_procesos_cpu()
        elif opcion == "4":
            mostrar_info_red()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()
