from cryptography.fernet import Fernet
import base64

def encrypt_code():
    # Generar una nueva clave
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    
    # Leer el código original
    with open('windows_optimizer.py', 'r', encoding='utf-8') as file:
        code = file.read()
    
    # Encriptar el código
    encrypted_code = cipher_suite.encrypt(code.encode())
    
    # Guardar la clave y el código encriptado
    with open('key.txt', 'wb') as file:
        file.write(key)
    
    with open('encrypted_code.txt', 'wb') as file:
        file.write(encrypted_code)
    
    print(f"Clave generada: {key.decode()}")
    print("Código encriptado guardado en 'encrypted_code.txt'")

if __name__ == "__main__":
    encrypt_code() 