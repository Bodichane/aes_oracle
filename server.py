from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
from flask import Flask, jsonify, request


key = get_random_bytes(16)
mac_key = get_random_bytes(32)
iv = get_random_bytes(16)

app = Flask(__name__)

@app.route("/get_challenge", methods=['GET'])
def get_challenge():
    message = b"Hello World"
    ct_bytes = encrypt_cbc(message)
    ct_hex = ct_bytes.hex()
    mac_bytes = HMAC.new(mac_key, ct_bytes, digestmod=SHA256)
    mac_hex = mac_bytes.digest().hex()

    return jsonify({"ciphertext": ct_hex, "mac": mac_hex})


def encrypt_cbc(message):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(message, 16))

def decrypt_cbc(ct):
    iv_received = ct[:16]
    block = ct[16:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv_received)
    return unpad(cipher.decrypt(block), 16)

@app.route("/oracle", methods=['POST'])
def oracle():
    data = request.get_json()
    ct_hex = data.get('ciphertext')
    mac_hex = data.get('mac')

    ct_bytes = bytes.fromhex(ct_hex)
    mac_bytes = bytes.fromhex(mac_hex)

    mac_object = HMAC.new(mac_key, ct_bytes, digestmod=SHA256)
    try: 
        mac_object.verify(mac_bytes)
    except ValueError:
        return "Invalid HMAC, altered message", 403
    
    try:
        decrypt_cbc(ct_bytes)
        return "OK", 200
    except ValueError:
        return "Invalid Padding", 400



if __name__ == '__main__':
    app.run(debug=True, port=5000)
