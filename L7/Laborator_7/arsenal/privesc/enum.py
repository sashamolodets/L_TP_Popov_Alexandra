# -*- coding: utf-8 -*-
"""Laboratorul 7 - enumerare spre root. Generat din programul
de laborator, cu codul scris de student."""
import argparse, io, json, os

GTFO = {'vim.basic', 'less', 'perl', 'bash', 'awk', 'vim', 'find', 'nmap', 'cp', 'python3'}

#  PARTEA A - aduna si grupeaza
# ---------------------------------------------------------------------------

def citeste_linii(cale):
    """Sarcina 1. Citeste un fisier si intoarce LISTA randurilor folositoare.

    Fiecare rand se curata de spatiile de la capete. Se arunca randurile
    goale si cele care incep cu diez, fiindca sunt comentarii.

    citeste_linii("start/suid.txt")  ->  lista cu 14 randuri
    """
    rez = []

    with open(cale, "r", encoding="utf-8") as fisier:
        for rand in fisier:
            rand = rand.strip()

            if rand and not rand.startswith("#"):
                rez.append(rand)

    return rez



def nume(cale):
    """Sarcina 2. Intoarce numele fisierului dintr-o cale.

    Numele decide daca binarul e periculos, nu toata calea.

    nume("/usr/bin/find")  ->  "find"
    """
    rez = cale.rsplit("/",1)
    return rez[-1]



def suid_constatari(cale):
    """Sarcina 3. Din fisierul SUID face o LISTA DE DICTIONARE.

    Fiecare cale UNICA, in ordine sortata, devine o fisa cu trei campuri:
        {"cale": ..., "nume": ..., "risc": "mare" sau "normal"}
    Riscul e "mare" daca numele se afla in multimea GTFO, altfel "normal".

    Atentie: in captura o cale apare de doua ori. Fisa ei apare o data.
    """
    linii = citeste_linii(cale)
    unice = sorted(set(linii))
    rez = []

    for c in unice:
        n = nume(c)

        if n in GTFO:
            risc = "mare"
        else:
            risc = "normal"

        fisa = {
            "cale": c,
            "nume": n,
            "risc": risc
        }

        rez.append(fisa)

    return rez


def sudo_constatari(cale):
    """Sarcina 4. Din fisierul sudo face o lista de dictionare.

    Un rand are forma  utilizator : drept
    Il despachetezi intr-un tuplu de doua valori, taind la PRIMUL separator:
        user, drept = rand.split(" : ", 1)

    Fiecare rand devine:
        {"user": ..., "drept": ..., "risc": "mare" sau "normal"}
    Riscul e "mare" daca in drept apare NOPASSWD, fiindca atunci comanda
    se ruleaza fara sa se ceara parola.
    """
    linii = citeste_linii(cale)
    rez = []

    for rand in linii:
        user, drept = rand.split(" : ", 1)

        if "NOPASSWD" in drept:
            risc = "mare"
        else:
            risc = "normal"

        fisa = {
            "user": user,
            "drept": drept,
            "risc": risc
        }

        rez.append(fisa)

    return rez


def cron_constatari(cale):
    """Sarcina 5. Din crontab face o lista de dictionare.

    Un rand de crontab are cinci campuri de timp, apoi utilizatorul si
    comanda. Desparti randul in campuri cu split(), iar:
        campul 5 (al saselea) este utilizatorul
        tot ce urmeaza, lipit la loc cu spatii, este comanda

    Fiecare rand devine:  {"user": ..., "comanda": ...}
    """
    rez = []
    linii = citeste_linii(cale)

    for l in linii:
        camp = l.split()
        user = camp[5]
        comanda = " ".join(camp[6:])

        rand = {
            "user": user,
            "comanda": comanda
        }

        rez.append(rand)

    return rez


def enumereaza(dosar):
    """Sarcina 6. Aduna toate constatarile intr-un singur DICTIONAR.

    Primeste calea folderului cu capturi si intoarce un dictionar cu o
    cheie pe categorie, iar valoarea este lista de constatari:

        {"suid": [...], "sudo": [...], "cron": [...]}

    Pentru a lipi calea unui fisier de folder, foloseste os.path.join.
    """
    suid = suid_constatari(os.path.join(dosar,"suid.txt"))
    sudo = sudo_constatari(os.path.join(dosar,"sudo.txt"))
    cron = cron_constatari(os.path.join(dosar,"crontab.txt"))

    rez = {
        "suid": suid,
        "sudo": sudo,
        "cron": cron
    }
    return rez

def utilizatori_implicati(raport):
    """Sarcina 7. Intoarce MULTIMEA utilizatorilor care apar in raport.

    Sunt utilizatorii din constatarile sudo REUNITI cu cei din cron.
    Reuniunea a doua multimi se face cu operatorul  |  si arunca dublurile.

    Primeste dictionarul intors de enumereaza.
    """
    user_sudo = set()
    user_cron = set()
    for c in raport["sudo"]:
        user_sudo.add(c["user"])
    for c in raport["cron"]:
        user_cron.add(c["user"])
    rez = user_cron | user_sudo
    return rez


# ---------------------------------------------------------------------------
#  PARTEA B - ce e nou fata de un sistem curat
# ---------------------------------------------------------------------------

def cai(fisier):
    """Sarcina 8. Intoarce MULTIMEA cailor dintr-un fisier.

    Foloseste citeste_linii, pe care ai scris-o deja la sarcina 1.
    O multime arunca singura dublurile, de aceea aici iese 13, nu 14.
    """
    linii = citeste_linii(fisier)
    rez = set(linii)
    return rez


def suid_noi(acum, baza):
    """Sarcina 9. Ce e in acum, dar nu si in baza.

    Amandoua sunt multimi de cai. Rezultatul este tot o multime: fisierele
    SUID aparute fata de sistemul curat.

    Se face cu UN SINGUR operator, nu cu doua bucle una in alta.
    """
    rez = acum - baza
    return rez

def risc_pe_nume(multime_cai):
    """Sarcina 10. Fisa nume -> risc, ca DICTIONAR.

    Pentru fiecare cale din multimea primita, cheia este numele fisierului,
    iar valoarea este "mare" daca numele se afla in GTFO, altfel "normal".

    Se scrie pe un singur rand, cu dict comprehension.
    """
    rez = {nume(c): "mare" if nume(c) in GTFO else "normal"
    for c in multime_cai}
    return rez
def periculoase_noi(noi):
    """Sarcina 11. Lista cailor noi care sunt periculoase, sortata.

    Din multimea primita pastrezi doar caile al caror nume e in GTFO si le
    intorci ca lista, in ordine sortata.
    """
    rez = []
    for c in noi:
        if nume(c) in GTFO:
            rez.append(c)
    return sorted(rez)





# ===========================================================================
#
#   Sub randul urmator incepe programul care te verifica.
#   Nu e nevoie sa intelegi codul de mai jos si nu il modifica.
#
# ===========================================================================
#  


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print("%s: %d gasite, %d cu risc mare" % (categorie, len(lista), len(mari)))
    useri = utilizatori_implicati(raport)
    print("utilizatori implicati:", ", ".join(sorted(useri)))
    with io.open("enum.json", "w", encoding="utf-8") as fis:
        json.dump(raport, fis, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
