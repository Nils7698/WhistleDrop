import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

# Verzeichnisse
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
        print(f"❌ Fehler beim Entschlüsseln des AES-Schlüssels mit {private_key_path}: {e}")
        return None

def decrypt_file(file_path, aes_key, output_path):
    try:
        with open(file_path, "rb") as f:
            nonce = f.read(12)
            tag = f.read(16)
            ciphertext = f.read()
        cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag)
        with open(output_path, "wb") as f:
            f.write(plaintext)
        print(f"✅ Datei erfolgreich entschlüsselt: {output_path}")
    except Exception as e:
        print(f"❌ Fehler beim Entschlüsseln der Datei {file_path}: {e}")

def main():
    encrypted_files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith(".enc")]
    private_keys = [f for f in os.listdir(PRIVATE_KEYS_DIR) if f.endswith(".pem")]

    if not encrypted_files:
        print("⚠️ Keine verschlüsselten Dateien gefunden.")
        return

    print(f"🔍 {len(encrypted_files)} verschlüsselte Dateien gefunden. Starte Entschlüsselung...")

    for enc_file in encrypted_files:
        file_id_with_ext = enc_file.replace(".enc", "")
        file_ext = os.path.splitext(file_id_with_ext)[1]  # z.B. ".pdf"
        uuid = os.path.splitext(file_id_with_ext)[0]      # Nur UUID ohne Endung

        encrypted_file_path = os.path.join(UPLOADS_DIR, enc_file)
        key_file_name = f"{uuid}{file_ext}.key.enc"
        key_path = os.path.join(PUBLIC_KEYS_DIR, key_file_name)

        if not os.path.exists(key_path):
            print(f"❌ Kein Schlüssel gefunden für {enc_file}")
            continue

        found = False
        for priv_key_file in private_keys:
            priv_key_path = os.path.join(PRIVATE_KEYS_DIR, priv_key_file)
            aes_key = try_decrypt_aes_key(key_path, priv_key_path)
            if aes_key:
                output_file_path = os.path.join(DOWNLOADS_DIR, f"{uuid}{file_ext}")
                decrypt_file(encrypted_file_path, aes_key, output_file_path)
                found = True
                break

        if not found:
            print(f"❌ Kein passender privater Schlüssel für {enc_file} gefunden.")

if __name__ == "__main__":
    main()
