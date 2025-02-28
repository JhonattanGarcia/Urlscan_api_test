import json
import requests
import os
import csv
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

def save_results(output_folder, output_title, results, save_json, save_csv):
    """
    Guarda los resultados en un archivo JSON y/o CSV según configuración.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    
    if save_json:
        json_filepath = os.path.join(output_folder, f"{output_title}_{timestamp}.json")
        with open(json_filepath, 'w') as file:
            json.dump(results, file, indent=4)
        print(f"Resultados guardados en {json_filepath}")
    
    if save_csv:
        csv_filepath = os.path.join(output_folder, f"{output_title}_{timestamp}.csv")
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["_id", "sort", "page_url", "task_url", "stats", "brand"])
            for result in results:
                writer.writerow([
                    result.get("_id", ""),
                    result.get("sort", ""),
                    result.get("page", {}).get("url", ""),
                    result.get("task", {}).get("url", ""),
                    json.dumps(result.get("stats", {})),
                    result.get("brand", "")
                ])
        print(f"Resultados guardados en {csv_filepath}")

def main():
    config = read_config()
    if not config:
        return
    
    api_key = config.get("UserKey")
    output_folder = config.get("output_folder", "./resultados")
    output_title = config.get("output_tittle", "Resultados_busqueda")
    test_mode = config.get("test_mode", 0)
    max_results = config.get("Max_results", 10)
    save_json = config.get("Result_json", 1)
    save_csv = config.get("Result_csv", 1)
    
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
    
    save_results(output_folder, output_title, all_results, save_json, save_csv)
    
if __name__ == "__main__":
    main()
