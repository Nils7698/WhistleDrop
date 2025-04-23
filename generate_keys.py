from Crypto.PublicKey import RSA
import os
import json

KEY_DIR = "public_keys"
PRIVATE_DIR = "journalist_private"
os.makedirs(KEY_DIR, exist_ok=True)
os.makedirs(PRIVATE_DIR, exist_ok=True)

KEY_DB_PATH = os.path.join(KEY_DIR, "public_keys.json")

def generate_keypair(key_id):
    key = RSA.generate(2048)
    private_pem = key.export_key().decode()
    public_pem = key.publickey().export_key().decode()

    # Privater Schlüssel: bleibt beim Journalisten
    with open(os.path.join(PRIVATE_DIR, f"{key_id}_private.pem"), "w") as f:
        f.write(private_pem)

    return {
        "id": key_id,
        "pem": public_pem
    }

def main():
    keys = []
    for i in range(5):  # 5 Schlüssel erzeugen
        key_id = f"journalist-key-{i}"
        key_entry = generate_keypair(key_id)
        keys.append(key_entry)

    with open(KEY_DB_PATH, "w") as f:
        json.dump(keys, f, indent=2)
    print("✅ Schlüssel generiert.")

if __name__ == "__main__":
    main()
