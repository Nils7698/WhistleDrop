from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad
import sys
import os

def decrypt_aes_key(encrypted_key_path, private_key_path):
    with open(encrypted_key_path, "rb") as f:
        encrypted_key = f.read()

    with open(private_key_path, "rb") as f:
        private_key = RSA.import_key(f.read())

    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_key)
    return aes_key

def decrypt_file(encrypted_file_path, aes_key, output_path):
    with open(encrypted_file_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)

    with open(output_path, "wb") as f:
        f.write(plaintext)

    print(f"✅ Datei entschlüsselt: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("⚠️  Nutzung: python decrypt_file.py <aes_key.enc> <private.pem> <input.enc> <output>")
        sys.exit(1)

    aes_key_file = sys.argv[1]
    private_key_file = sys.argv[2]
    encrypted_data_file = sys.argv[3]
    output_file = sys.argv[4]

    aes_key = decrypt_aes_key(aes_key_file, private_key_file)
    decrypt_file(encrypted_data_file, aes_key, output_file)