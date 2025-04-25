from flask import Flask, render_template, request, redirect, flash
import os
from rsa_utils import get_unused_public_key, encrypt_aes_key_with_rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from uuid import uuid4
import subprocess

UPLOAD_FOLDER = "uploads/"
KEY_FOLDER = "public_keys/"

app = Flask(__name__)
app.secret_key = "test_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(KEY_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            flash("Keine Datei ausgewählt.")
            return redirect(request.url)

        file_content = file.read()
        aes_key = get_random_bytes(32)
        nonce = get_random_bytes(12)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(file_content)

        key_id, rsa_key = get_unused_public_key()
        encrypted_aes_key = encrypt_aes_key_with_rsa(aes_key, rsa_key)

        file_id = str(uuid4())
        
        # Extrahiere die Dateiendung der Originaldatei
        file_name, file_extension = os.path.splitext(file.filename)
        
        # Speichere die verschlüsselte Datei mit der Originalendung
        encrypted_file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}{file_extension}.enc")
        with open(encrypted_file_path, "wb") as f:
            f.write(nonce + tag + ciphertext)
        
        # Speichere den verschlüsselten AES-Schlüssel mit der Originalendung
        encrypted_key_path = os.path.join(KEY_FOLDER, f"{file_id}{file_extension}.key.enc")
        with open(encrypted_key_path, "wb") as f:
            f.write(encrypted_aes_key)

        flash(f"✅ Datei erfolgreich hochgeladen und verschlüsselt (ID: {file_id})")
        return redirect("/")
    
    return render_template("upload.html")


if __name__ == "__main__":
    subprocess.run(["python3", "generate_keys.py"], check=True)
    app.run(debug=True)
