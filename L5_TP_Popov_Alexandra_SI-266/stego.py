#TODO: B5
from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj)

biti += "00000000"

canale = [c for pixel in px for c in pixel]

for i, bit in enumerate(biti):
    canale[i] = (canale[i] & ~1) | int(bit)

px_nou = [tuple(canale[i:i+3]) for i in range(0, len(canale), 3)]

img.putdata(px_nou)
img.save("stego.png")

#TODO: B6
px = list(Image.open("stego.png").convert("RGB").get_flattened_data())

biti = ""
for (r, g, b) in px:
    biti += str(r & 1) + str(g & 1) + str(b & 1)

mesaj_decodat = ""

for i in range(0, len(biti), 8):
    octet = biti[i:i+8]

    if len(octet) < 8:
        break

    caracter = int(octet, 2)

    if caracter == 0:
        break

    mesaj_decodat += chr(caracter)

print("Mesaj extras:", mesaj_decodat)