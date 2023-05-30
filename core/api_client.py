import requests

def obtener_productos():
    url = 'https://musicpro.bemtorres.win/api/v1/bodega/producto'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hubo errores en la respuesta
        
        # Obtener los datos de la respuesta en formato JSON
        data = response.json()
        
        # Procesar los datos como desees
        for producto in data:
            # Hacer algo con cada producto
            print(producto)
            
    except requests.exceptions.RequestException as e:
        print('Error al realizar la solicitud:', e)

# Llamar a la función para obtener los productos
obtener_productos()
