from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import json
import os

KEY_DB_PATH = "public_keys/public_keys.json"

def load_public_keys():
    if not os.path.exists(KEY_DB_PATH):
        return []
    with open(KEY_DB_PATH, 'r') as f:
        return json.load(f)

def save_public_keys(keys):
    with open(KEY_DB_PATH, 'w') as f:
        json.dump(keys, f, indent=2)

def get_unused_public_key():
    keys = load_public_keys()
    if not keys:
        raise Exception("Keine öffentlichen Schlüssel verfügbar.")
    key_entry = keys.pop(0)
    save_public_keys(keys)
    rsa_key = RSA.import_key(key_entry['pem'])
    return key_entry['id'], rsa_key

def encrypt_aes_key_with_rsa(aes_key: bytes, rsa_key):
    cipher = PKCS1_OAEP.new(rsa_key)
    return cipher.encrypt(aes_key)
