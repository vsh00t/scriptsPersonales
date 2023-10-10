import sys

def convert_to_hex_representation(filename):
    try:
        with open(filename, 'rb') as file:
            shell_data = file.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)

    shell_coded = ''.join([f"\\x{byte:02x}" for byte in shell_data])
    return "0" + ",0".join(shell_coded.split("\\")[1:])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <raw payload file>")
        sys.exit(1)

    result = convert_to_hex_representation(sys.argv[1])
    print(result)
