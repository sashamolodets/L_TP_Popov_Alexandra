# Laboratorul 5. Informații invizibile: forensics și steganografie

## LUCRAREA A (nucleu). Decoderul universal

### A4. Straturi multiple, într-o buclă
Am decodat șirul `NTM1OTU3NTk=` și am obținut `53595759`.

### A5. Spargi un XOR cu cheie de un octet
Am găsit cheia `128` și mesajul `FLAG{xor_un_octet}`.

### A6. Spargi un hash prin dicționar
Algoritmul identificat este MD5, iar parola găsită este `password`.

### A7. argparse, fișa JSON și un test
Am salvat rezultatul în `fisa.json` și am verificat funcția cu pytest. Testul a trecut (`1 passed`).

## LUCRAREA B (extindere). Forensics pe fișiere și un mesaj ascuns

### B1. Magic bytes: tipul real, nu extensia
Am identificat tipul real al fișierului `foto.jpg`: JPEG.

### B2. strings: textul citibil dintr-un binar
Am găsit fișierul `secret.txt` și mesajul `FLAG{ascuns_prin_carving}`.

### B3. Metadate EXIF și GPS din poză
Am extras modelul iPhone 13, data 14.09.2026 și coordonatele GPS: 47.016667, 28.8575.

### B4. File carving: scoți fișierul ascuns
Am extras arhiva `gasit.zip`, care conține `secret.txt` cu mesajul `FLAG{ascuns_prin_carving}`.

### B5. Ascunzi un mesaj prin LSB
Am ascuns mesajul într-o imagine și am salvat-o ca `stego.png`.

### B6. Dezvălui mesajul înapoi
Am extras mesajul `FLAG{ascuns_in_pixeli}` din imagine.