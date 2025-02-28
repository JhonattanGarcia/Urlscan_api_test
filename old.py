import json
import requests
import os
from datetime import datetime

def read_config(filepath='config.json'):
    """
    Lee el archivo config.json y devuelve la configuración.
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filepath}.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {filepath} no tiene un formato JSON válido.")
        return {}
    except Exception as e:
        print(f"Error al leer el archivo {filepath}: {e}")
        return {}

def read_search_criteria(filepath='criteria.json'):
    """
    Lee el archivo criteria.json y devuelve los criterios de búsqueda.
    """
    try:
        with open(filepath, 'r') as file:
            criteria = json.load(file)
            return criteria.get("search_criteria", [])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filepath}.")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo {filepath} no tiene un formato JSON válido.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {filepath}: {e}")
        return []

def format_query(query_type, query_value):
    """
    Formatea la consulta para UrlScan.io asegurando la sintaxis correcta.
    """
    if query_type in ["url", "domain", "ip"]:
        return f"{query_type}:\"{query_value}\""
    return f"{query_type}:{query_value}"

def search_urlscan(api_key, query, max_results):
    """
    Realiza una búsqueda en la API de UrlScan.io según el criterio especificado.
    """
    url = "https://urlscan.io/api/v1/search/"
    headers = {
        'API-Key': api_key,
        'Content-Type': 'application/json'
    }
    params = {
        'q': query,
        'size': max_results
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error en la solicitud: {response.status_code}, {response.text}")
        return []

def save_results(output_folder, output_title, results):
    """
    Guarda los resultados en un archivo JSON.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{output_title}_{timestamp}.json"
    filepath = os.path.join(output_folder, filename)
    with open(filepath, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"Resultados guardados en {filepath}")

def main():
    config = read_config()
    if not config:
        return
    
    api_key = config.get("UserKey")
    output_folder = config.get("output_folder", "./resultados")
    output_title = config.get("output_tittle", "Resultados_busqueda")
    test_mode = config.get("test_mode", 0)
    max_results = config.get("Max_results", 10)
    
    criteria = read_search_criteria()
    if not criteria:
        return
    
    all_results = []
    for item in criteria:
        query = format_query(item['type'], item['value'])
        if test_mode:
            print(f"Realizando búsqueda para: {query}")
        results = search_urlscan(api_key, query, max_results)
        all_results.extend(results)
    
    save_results(output_folder, output_title, all_results)
    
if __name__ == "__main__":
    main()