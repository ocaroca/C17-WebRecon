import os
import requests
import hashlib

# Ruta al archivo con las URLs
RUTA_ARCHIVO_URLS = "urls.txt"
# Directorio donde se guardan las versiones previas
DIRECTORIO_DATOS = "datos_webs"
# Comando para notificar
COMANDO_NOTIFY = "notify"

def leer_urls(archivo):
    """Lee las URLs de un archivo de texto"""
    with open(archivo, "r") as f:
        return [line.strip() for line in f if line.strip()]

def obtener_html(url):
    """Descarga el contenido HTML de una URL"""
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.text
    except requests.RequestException as e:
        print(f"Error al descargar {url}: {e}")
        return None

def obtener_hash(contenido):
    """Calcula un hash del contenido para detectar cambios"""
    return hashlib.sha256(contenido.encode('utf-8')).hexdigest()

def verificar_cambios(url):
    """Verifica si hubo cambios en la URL"""
    if not os.path.exists(DIRECTORIO_DATOS):
        os.makedirs(DIRECTORIO_DATOS)
    
    archivo_hash = os.path.join(DIRECTORIO_DATOS, f"{hashlib.md5(url.encode()).hexdigest()}.txt")
    html_actual = obtener_html(url)
    
    if html_actual is None:
        return False  # No se pudo descargar la página

    hash_actual = obtener_hash(html_actual)
    
    # Si no hay archivo previo, lo guardamos y consideramos que no hay cambios
    if not os.path.exists(archivo_hash):
        with open(archivo_hash, "w") as f:
            f.write(hash_actual)
        return False

    # Leemos el hash anterior
    with open(archivo_hash, "r") as f:
        hash_anterior = f.read().strip()

    # Comparamos los hashes
    if hash_actual != hash_anterior:
        # Guardamos el nuevo hash
        with open(archivo_hash, "w") as f:
            f.write(hash_actual)
        return True

    return False

def main():
    urls = leer_urls(RUTA_ARCHIVO_URLS)
    for url in urls:
        if verificar_cambios(url):
            os.system(f'echo "Cambios detectados en {url}" | {COMANDO_NOTIFY}')

if __name__ == "__main__":
    main()