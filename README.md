# WhistleDrop

Projekt im Rahmen der Vorlesung Cyberspionage.

## Voraussetzungen
Python mit den Bibliotheken
- pycryptodome
- flask

## Verwendung
**Server starten**
```
python app.py
```

**Entschlüsseln**
extra Terminal öffnen und folgendes ausführen:
```
python auto_decrypt.py
```
Die entschlüsselte Datei befindet sich nun im "downloads" Ordner

## Wie funktioniert die Verschlüsselung?
### Schlüsselerzeugung
Beim Start von `app.py` wird mit `generate_keys.py` ein Satz von RSA-Schlüsselpaaren erzeugt:
- Öffentliche Schlüssel werden im JSON-Format (public_keys.json) gespeichert
- Private Schlüssel bleiben beim/die Journalist:in (journalist_private/)

### Datei-Upload & Verschlüsselung
Wenn eine Datei hochgeladen wird:
1. Es wird ein zufälliger AES-Schlüssel erzeugt
2. Die Datei wird mit AES-256 im GCM-Modus verschlüsselt
3. Der AES-Schlüssel wird mit einem öffentlichen RSA-Schlüssel verschlüsselt
4. Die verschlüsselte Datei (uuid.dateiendung.enc) wird im uploads/-Ordner gespeichert
5. Der verschlüsselte AES-Schlüssel (uuid.dateiendung.key.enc) wird im public_keys/-Ordner gespeichert
6. Der verwendete öffentliche Schlüssel wird aus der Liste entfernt → One-Time-Pad-Prinzip

### Entschlüsselung
Nach Ausführung von `python auto_decrypt.py` passiert folgendes:
1. Das Skript liest alle .enc-Dateien
2. entschlüsselt den AES-Schlüssel mit den privaten RSA-Schlüsseln
3. entschlüsselt die Datei im AES-GCM-Modus
4. speichert die Datei im Ordner downloads/ mit korrekter Dateiendung