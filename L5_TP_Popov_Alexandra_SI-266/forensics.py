#TODO: B1
def tip_real(cale):
    cap = open(cale, "rb").read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return cap.hex()


print(tip_real("probe/foto.jpg"))

#TODO: B2
import re

date = open("probe/ascuns.png", "rb").read()

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

#TODO: B3
from PIL import Image
from PIL.ExifTags import TAGS

exif = Image.open("probe/foto.jpg")._getexif() or {}

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps = exif.get(34853)

if gps:
    lat = gps[2]
    lon = gps[4]

    latitudine = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / 3600
    longitudine = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / 3600

    if gps[1] == "S":
        latitudine = -latitudine
    if gps[3] == "W":
        longitudine = -longitudine

    print("Latitudine:", latitudine)
    print("Longitudine:", longitudine)

#TODO: B4
date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")

if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("Arhiva extrasa de la octetul", i)