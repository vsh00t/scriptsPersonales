import csv
import re
import sys

def extract_urls_from_csv(file_path):
    """
    Extrae todas las URLs de un archivo CSV.

    Args:
        file_path (str): Ruta al archivo CSV.

    Returns:
        list: Lista de URLs únicas encontradas en el archivo.
    """
    urls = set()  # Usamos un conjunto para evitar duplicados

    # Abrir y leer el archivo CSV
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Buscar posibles URLs en cada celda de la fila
            for cell in row:
                # Expresión regular para encontrar URLs
                url_pattern = r'https?://[\w.-]+(?:/[\w./?=%-]*)?'
                matches = re.findall(url_pattern, cell)
                urls.update(matches)  # Agregar las URLs encontradas al conjunto

    return list(urls)

def extract_subdomains(urls, base_domain):
    """
    Filtra las URLs para obtener solo aquellas que pertenecen a subdominios de un dominio base.

    Args:
        urls (list): Lista de URLs.
        base_domain (str): Dominio base para filtrar subdominios.

    Returns:
        list: Lista de subdominios únicos encontrados.
    """
    subdomains = set()

    for url in urls:
        # Extraer el dominio usando expresiones regulares
        match = re.match(r'https?://([\w.-]+)', url)
        if match:
            domain = match.group(1)
            # Verificar si es un subdominio del dominio base
            if domain.endswith(base_domain) and domain != base_domain:
                subdomains.add(domain)

    return list(subdomains)

def main():
    # Validar argumentos de línea de comandos
    if len(sys.argv) != 3:
        print("Uso: python script.py <archivo_csv> <dominio_base>")
        sys.exit(1)

    file_path = sys.argv[1]
    base_domain = sys.argv[2]

    try:
        # Extraer todas las URLs del archivo CSV
        urls = extract_urls_from_csv(file_path)

        print("URLs únicas encontradas:")
        for url in urls:
            print(url)

        # Filtrar subdominios del dominio base
        subdomains = extract_subdomains(urls, base_domain)

        print("\nSubdominios únicos encontrados:")
        for subdomain in subdomains:
            print(subdomain)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
