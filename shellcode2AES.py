import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

KEY = b'0123456789ABCDEF0123456789ABCDEF'
IV = b'1234567890ABCDEF'  

def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data  # Solo devolvemos el dato cifrado sin el IV

def convert_to_hex_representation(filename):
    try:
        with open(filename, 'rb') as file:
            shell_data = file.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)

    encrypted_data = encrypt_data(shell_data)
    shell_coded = ''.join([f"{byte:02x}" for byte in encrypted_data])
    return shell_coded

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <raw payload file>")
        sys.exit(1)

    result = convert_to_hex_representation(sys.argv[1])
    print(result)
