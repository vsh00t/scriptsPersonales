import sys
import yaml

def parse_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def generate_openapi(urls):
    openapi = {
        'openapi': '3.0.0',
        'info': {
            'title': 'Example API',
            'description': 'API generated from URL list',
            'version': '1.0.0'
        },
        'servers': [],
        'paths': {}
    }

    # Extract the base URL from the first URL in the list
    base_url = urls[0].split('/')[2]
    openapi['servers'].append({'url': f'https://{base_url}'})

    for url in urls:
        # Extract the path and method (assuming GET for simplicity)
        path = url.replace(f'https://{base_url}', '')
        if path not in openapi['paths']:
            openapi['paths'][path] = {}

        openapi['paths'][path]['get'] = {
            'summary': f'GET {path}',
            'responses': {
                '200': {
                    'description': 'Successful response'
                }
            }
        }

    return openapi

def main(file_path):
    urls = parse_urls(file_path)
    openapi = generate_openapi(urls)

    with open('openapi.yaml', 'w') as file:
        yaml.dump(openapi, file, sort_keys=False)
    print("OpenAPI definition generated successfully in 'openapi.yaml'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generateOpenAPI.py <path_to_url_file>") # el archivo contiene las url obtenidas desde burpsuite. 
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
