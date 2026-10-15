s = "Salut"
b = s.encode()
print(b, b[0])

#TODO: A1
hex_text = b.hex()
print(hex_text)
original = bytes.fromhex(hex_text)
print(original)

#TODO: A2
import re

def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"

    if len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"

    return "necunoscut"


print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))

#TODO: A3
import base64
from urllib.parse import unquote
def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        rezultat = base64.b64decode(s)

    elif strat == "hex":
        rezultat = bytes.fromhex(s)

    elif strat == "url":
        rezultat = unquote(s).encode()

    else:
        rezultat = s.encode()

    return strat, rezultat

 #TODO: A4
def citibil(b):
    return all(32 <= c < 127 for c in b)


val = "NTM1OTU3NTk="

for _ in range(8):
    strat, b = desfa(val)

    if citibil(b):
        print("Text citibil:", b.decode())
        break

    val = b.decode()

#TODO: A5
with open("probe/xor.bin", "rb") as f:
    date = f.read()

for k in range(256):
    clar = bytes(b ^ k for b in date)

    if citibil(clar):
        print("Cheie:", k, "| Mesaj:", clar.decode())

import hashlib

# TODO: A6
tinta = open("probe/hashuri.txt").readline().strip()

print(len(tinta))

if len(tinta) == 32:
    algoritm = "md5"
elif len(tinta) == 40:
    algoritm = "sha1"
elif len(tinta) == 64:
    algoritm = "sha256"
else:
    algoritm = None

if algoritm:
    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()

        hash_calculat = hashlib.new(
            algoritm, cuv.encode()
        ).hexdigest()

        if hash_calculat == tinta:
            print("Algoritm:", algoritm)
            print("Parola gasita:", cuv)
            break
else:
    print("Algoritm necunoscut")

# TODO: A7
import argparse
import json
def main():
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        with open(a.intrare, "rb") as f:
            date = f.read()
        intrare = date.decode()
    else:
        intrare = a.intrare

    strat, rezultat = desfa(intrare)

    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump({
            "strat": strat,
            "rezultat": rezultat.decode()
        }, f, indent=4)
if __name__ == "__main__":
    main()