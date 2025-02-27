import json
import os
import argparse
import re

# Configurar los argumentos de línea de comandos
parser = argparse.ArgumentParser(description="Extraer nombres y contar objetos desde archivos JSON.")
parser.add_argument("directory", help="Directorio donde se encuentran los archivos JSON.")
parser.add_argument("--output_format", choices=["column", "comma"], default="column",
                    help="Formato de salida: 'column' para una lista en columna o 'comma' para una lista separada por comas.")
args = parser.parse_args()

# Patrones para identificar los archivos correspondientes
patterns = {
    "usuarios": re.compile(r".*_users\.json$"),
    "grupos": re.compile(r".*_groups\.json$"),
    "computadores": re.compile(r".*_computers\.json$"),
    "ous": re.compile(r".*_ous\.json$"),
    "gpos": re.compile(r".*_gpos\.json$")
}

# Inicializar contadores
counts = {
    "usuarios": 0,
    "grupos": 0,
    "computadores": 0,
    "ous": 0,
    "gpos": 0
}

# Buscar archivos XXXX_users.json y XXXX_computers.json en el directorio
user_files = []
computer_files = []
pattern_users = re.compile(r"\d+_users\.json$")
pattern_computers = re.compile(r"\d+_computers\.json$")

for file in os.listdir(args.directory):
    if pattern_users.match(file):
        user_files.append(os.path.join(args.directory, file))
    elif pattern_computers.match(file):
        computer_files.append(os.path.join(args.directory, file))

if not user_files and not computer_files:
    print("No se encontraron archivos XXXX_users.json o XXXX_computers.json en el directorio especificado.")
    exit(1)

# Función para extraer nombres desde un archivo JSON
def extract_names(file_path, key):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [item['Properties'][key] for item in data['data'] if 'Properties' in item and key in item['Properties']]
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return []

# Función para contar elementos en un archivo JSON
def count_elements(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return len(data['data'])
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return 0

# Procesar cada archivo en el directorio para contar objetos
for file in os.listdir(args.directory):
    for key, pattern in patterns.items():
        if pattern.match(file):
            file_path = os.path.join(args.directory, file)
            counts[key] += count_elements(file_path)

# Extraer nombres de computadoras
computer_names = []
for computer_file in computer_files:
    computer_names.extend(extract_names(computer_file, "name"))

# Extraer nombres de usuarios
user_names = []
for user_file in user_files:
    user_names.extend(extract_names(user_file, "name"))

# Formatear la salida según el formato especificado
if args.output_format == "column":
    computer_output_content = "\n".join(computer_names)  # Una computadora por línea
    user_output_content = "\n".join(user_names)  # Un usuario por línea
else:  # args.output_format == "comma"
    computer_output_content = ",".join(computer_names)  # Computadoras separadas por comas
    user_output_content = ",".join(user_names)  # Usuarios separados por comas

# Guardar la salida en archivos separados
computer_output_file = os.path.join(args.directory, "computer_names_output.txt")
user_output_file = os.path.join(args.directory, "user_names_output.txt")

with open(computer_output_file, 'w') as file:
    file.write(computer_output_content)

with open(user_output_file, 'w') as file:
    file.write(user_output_content)

print(f"Se han extraído {len(computer_names)} nombres de computadoras y se han guardado en '{computer_output_file}'.")
print(f"Se han extraído {len(user_names)} nombres de usuarios y se han guardado en '{user_output_file}'.")

# Guardar el resumen en un archivo de texto
resumen_file = os.path.join(args.directory, "resumen.txt")
with open(resumen_file, 'w') as resumen:
    resumen.write("Resumen de Objetos Contados:\n")
    resumen.write(f"Usuarios: {counts['usuarios']}\n")
    resumen.write(f"Grupos: {counts['grupos']}\n")
    resumen.write(f"Computadores: {counts['computadores']}\n")
    resumen.write(f"OUs: {counts['ous']}\n")
    resumen.write(f"GPOs: {counts['gpos']}\n")

print(f"Resumen guardado en '{resumen_file}'.")
