from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

key = get_random_bytes(16)
iv = get_random_bytes(16)

def encrypt_cbc(message):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(message, 16))

def decrypt_cbc(ct):
    iv_received = ct[:16]
    bloc = ct[16:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv_received)
    return unpad(cipher.decrypt(bloc), 16)

def oracle(ct):
    try:
        decrypt_cbc(ct)
        return True
    except ValueError:
        return False

def last_byte_attack(ct): 
    iv_received = ct[:16]
    bloc = ct[16:]

    for x in range(256):      
        iv_test = bytearray(iv_received)
        iv_test[-1] = x
        if oracle(bytes(iv_test) + bloc):     
            return (x ^ 0x01) ^ iv_received[-1]

    print("None x find")
    return None


ct = encrypt_cbc(b"Hello World")
last_byte = last_byte_attack(ct)
print(f"last_byte = {last_byte}")
print(f"last_byte = {chr(last_byte)}")

