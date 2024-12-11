import requests

BASE_URL = "http://localhost:8000/api/"
TOKEN_URL = "http://localhost:8000/api/token/"

username = input("Username: ")
password = input("Password: ")

# Obtener token
resp = requests.post(TOKEN_URL, data={'username': username, 'password': password})
if resp.status_code == 200:
    token = resp.json()['access']
    print("Token obtenido:", token)
else:
    print("Error autenticando:", resp.status_code, resp.text)
    exit()

headers = {
    'Authorization': f'Bearer {token}'
}

def formatear_precio_clp(precio_str):
    # Intentamos convertir el precio a float
    try:
        precio = float(precio_str)
        # Si es un entero (ej: 50.0), mostramos 50 CLP
        if precio.is_integer():
            return f"{int(precio)} CLP"
        else:
            # Caso contrario, mostramos con los decimales necesarios
            return f"{precio_str} CLP"
    except ValueError:
        # Si no se puede convertir, devolvemos lo que hay
        return f"{precio_str} CLP"

def crear_servicio():
    name = input("Nombre del servicio: ").strip()
    category = solicitar_categoria()
    details = input("Detalles del servicio: ").strip()
    price = solicitar_precio()

    service_data = {
        "mechanic": 1,  # Ajusta si tu mecánico tiene otro ID
        "name": name,
        "category": category,
        "details": details,
        "price": price
    }
    create_resp = requests.post(BASE_URL + "services/", headers=headers, json=service_data)
    if create_resp.status_code == 201:
        # Servicio creado con éxito
        data = create_resp.json()
        precio_formateado = formatear_precio_clp(data['price'])
        print(f"Servicio agregado con éxito:")
        print(f"ID: {data['id']}")
        print(f"Nombre: {data['name']}")
        print(f"Categoría: {data['category']}")
        print(f"Detalles: {data['details']}")
        print(f"Precio: {precio_formateado}")
    else:
        print("Error al crear servicio:", create_resp.status_code, create_resp.json())

def listar_servicios():
    list_resp = requests.get(BASE_URL + "services/", headers=headers)
    if list_resp.status_code == 200:
        servicios = list_resp.json()
        if servicios:
            for s in servicios:
                precio_formateado = formatear_precio_clp(s['price'])
                # Mostrar solo ID, Nombre, Precio y Detalles
                print(f"ID: {s['id']}, Nombre: {s['name']}, Precio: {precio_formateado}, Detalles: {s['details']}")
        else:
            print("No hay servicios disponibles.")
    else:
        print("Error al listar servicios:", list_resp.status_code, list_resp.text)

def actualizar_servicio():
    service_id = input("ID del servicio a actualizar: ").strip()
    if not service_id.isdigit():
        print("ID inválido.")
        return

    name = input("Nuevo nombre del servicio (deja en blanco si no quieres cambiarlo): ").strip()
    category = solicitar_categoria()
    details = input("Nuevos detalles del servicio (deja en blanco si no quieres cambiarlo): ").strip()
    price = solicitar_precio()

    update_data = {
        "mechanic": 1,
        "name": name if name else "Servicio Actualizado",
        "category": category,
        "details": details if details else "Sin cambios",
        "price": price
    }
    update_resp = requests.put(BASE_URL + f"services/{service_id}/", headers=headers, json=update_data)
    if update_resp.status_code == 200:
        data = update_resp.json()
        precio_formateado = formatear_precio_clp(data['price'])
        print("Servicio actualizado con éxito:")
        print(f"ID: {data['id']}")
        print(f"Nombre: {data['name']}")
        print(f"Categoría: {data['category']}")
        print(f"Detalles: {data['details']}")
        print(f"Precio: {precio_formateado}")
    else:
        print("Error al actualizar servicio:", update_resp.status_code, update_resp.json())


def eliminar_servicio():
    service_id = input("ID del servicio a eliminar: ").strip()
    if not service_id.isdigit():
        print("ID inválido.")
        return
    delete_resp = requests.delete(BASE_URL + f"services/{service_id}/", headers=headers)
    if delete_resp.status_code == 204:
        print("Servicio eliminado con éxito.")
    else:
        print("Error al eliminar servicio:", delete_resp.status_code, delete_resp.text)

def solicitar_categoria():
    while True:
        categoria = input("Categoría (MANT/REPA/OTRO): ").strip().upper()
        if categoria in ['MANT', 'REPA', 'OTRO', '']:
            return categoria if categoria else 'OTRO'
        else:
            print("Categoría inválida. Debe ser MANT, REPA u OTRO.")

def solicitar_precio():
    while True:
        precio = input("Precio: ").strip()
        try:
            float(precio)
            return precio
        except ValueError:
            print("Precio inválido. Debe ser un número.")

def menu():
    while True:
        print("\n=== MENÚ DE OPERACIONES ===")
        print("1. Crear servicio")
        print("2. Listar servicios")
        print("3. Actualizar servicio")
        print("4. Eliminar servicio")
        print("5. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == '1':
            crear_servicio()
        elif opcion == '2':
            listar_servicios()
        elif opcion == '3':
            actualizar_servicio()
        elif opcion == '4':
            eliminar_servicio()
        elif opcion == '5':
            break
        else:
            print("Opción no válida, por favor elige una opción entre 1 y 5.")

menu()
