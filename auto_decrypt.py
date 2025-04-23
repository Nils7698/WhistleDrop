import os
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad

PUBLIC_KEYS_DIR = "public_keys"
PRIVATE_KEYS_DIR = "journalist_private"
UPLOADS_DIR = "uploads"
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def try_decrypt_aes_key(encrypted_key_path, private_key_path):
    try:
        with open(encrypted_key_path, "rb") as f:
            encrypted_key = f.read()

        with open(private_key_path, "rb") as f:
            private_key = RSA.import_key(f.read())

        cipher_rsa = PKCS1_OAEP.new(private_key)
        aes_key = cipher_rsa.decrypt(encrypted_key)
        return aes_key
    except Exception as e:
        return None

def decrypt_file(file_path, aes_key, output_path):
    with open(file_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)

    with open(output_path, "wb") as f:
        f.write(plaintext)

def main():
    encrypted_keys = [f for f in os.listdir(PUBLIC_KEYS_DIR) if f.endswith(".key.enc")]
    private_keys = [f for f in os.listdir(PRIVATE_KEYS_DIR) if f.endswith(".pem")]

    if not encrypted_keys:
        print("⚠️ Keine verschlüsselten Schlüssel gefunden.")
        return

    print(f"🔍 {len(encrypted_keys)} Schlüssel gefunden. Starte Entschlüsselung...")

    for key_file in encrypted_keys:
        uuid = key_file.replace(".key.enc", "")
        encrypted_file = os.path.join(UPLOADS_DIR, f"{uuid}.enc")
        if not os.path.exists(encrypted_file):
            print(f"❌ Fehlende verschlüsselte Datei für {uuid}")
            continue

        key_path = os.path.join(PUBLIC_KEYS_DIR, key_file)

        found = False  # Variable, um zu verfolgen, ob ein Schlüssel gefunden wurde
        for priv_key_file in private_keys:
            priv_key_path = os.path.join(PRIVATE_KEYS_DIR, priv_key_file)
            aes_key = try_decrypt_aes_key(key_path, priv_key_path)
            if aes_key:
                print(f"✅ Entschlüsselung erfolgreich für {uuid} mit {priv_key_file}")
                output_path = os.path.join(DOWNLOADS_DIR, f"{uuid}.pdf")
                decrypt_file(encrypted_file, aes_key, output_path)
                found = True  # Passender Schlüssel gefunden
                break

        if not found:
            print(f"❌ Kein passender privater Schlüssel für {uuid} gefunden.")

if __name__ == "__main__":
    main()
