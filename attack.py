import requests


def oracle(ct_bytes):
    ct_hex = ct_bytes.hex()
    payload = {"ciphertext": ct_hex}
    reponse = requests.post("http://127.0.0.1:5000/oracle", json=payload)
    
    if reponse.status_code == 200:
        return True
    else:
        return False

def attack_block(ct):
    iv_received = bytearray(ct[:16])
    block = ct[16:]

    intermediaires = [0] * 16

    for i in range(1, 17):
        iv_test = iv_received[: ]

        for j in range(1, i):
            iv_test[-j] = intermediaires[-j] ^ i

        for x in range(256):
            iv_test[-i] = x

            if i == 1 and x == iv_received[-1]:
                continue

            if oracle(bytes(iv_test) + block):
                intermediaires[-i] = x ^ i
                break
        else:
            if i == 1:
                intermediaires[-1] = iv_received[-1] ^ 1

    pt = bytes([intermediaires[k] ^ iv_received[k] for k in range(16)])
    return pt


data = requests.get("http://127.0.0.1:5000/get_challenge").json()
ct_hex = data.get('ciphertext')
ct_bytes = bytes.fromhex(ct_hex)
pt = attack_block(ct_bytes)

print("Result of the attack:", pt)