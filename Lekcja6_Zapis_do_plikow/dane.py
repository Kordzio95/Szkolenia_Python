# Ten plik zajmuje sie tylko papierologia: zapisem i odczytem z plikow tekstowych.
# Glowny program (magazyn.py) sobie to importuje i nie musi wiedziec, jak to dziala w srodku.

# nazwy plikow trzymamy w jednym miejscu - jak trzeba zmienic, to tylko tutaj
PLIK_KONTO = "konto.txt"
PLIK_MAGAZYN = "magazyn.txt"
PLIK_HISTORIA = "historia.txt"

# czym rozdzielamy dane w linii - taki nasz separator, jak w kolumnach
SEP = ";"


def wczytaj_konto():
    # probujemy odczytac stan konta z pliku, a jak pliku nie ma - startujemy od zera
    try:
        with open(PLIK_KONTO, "r", encoding="utf-8") as fd:
            tekst = fd.read().strip()  # read() bierze caly plik jako jeden ciag znakow
    except FileNotFoundError:
        # pierwsze uruchomienie programu - nie ma jeszcze zadnych plikow
        return 0.0

    try:
        return float(tekst)
    except ValueError:
        # ktos grzebal w pliku i wpisal bzdury - lepiej zaczac od zera niz sie wywalic
        print("Uwaga: plik {} jest uszkodzony, zaczynam od zera.".format(PLIK_KONTO))
        return 0.0


def zapisz_konto(konto):
    # "w" czyli nadpisujemy - stan konta jest jeden, wiec starego nie trzymamy
    with open(PLIK_KONTO, "w", encoding="utf-8") as fd:
        fd.write("{:.2f}".format(konto))


def wczytaj_magazyn():
    # kazda linia w pliku to jeden produkt: nazwa;cena;ilosc
    magazyn = {}

    try:
        with open(PLIK_MAGAZYN, "r", encoding="utf-8") as fd:
            for linia in fd:
                linia = linia.strip()
                if not linia:
                    continue  # pusta linia - pomijamy

                czesci = linia.split(SEP)  # rozcinamy linie na kawalki po sredniku
                if len(czesci) != 3:
                    continue  # linia nie trzyma sie formatu - olewamy ja

                nazwa, cena, ilosc = czesci  # rozpakowanie listy na trzy zmienne
                try:
                    magazyn[nazwa] = {"cena": float(cena), "ilosc": int(ilosc)}
                except ValueError:
                    continue  # cena albo ilosc to nie liczby - pomijamy ten wiersz
    except FileNotFoundError:
        return {}  # nie ma pliku, czyli magazyn na start pusty

    return magazyn


def zapisz_magazyn(magazyn):
    # przepisujemy caly magazyn od nowa, linia na produkt
    linie = []
    for nazwa, dane in magazyn.items():
        linie.append("{}{}{:.2f}{}{}\n".format(nazwa, SEP, dane["cena"], SEP, dane["ilosc"]))

    with open(PLIK_MAGAZYN, "w", encoding="utf-8") as fd:
        fd.writelines(linie)  # writelines bierze cala liste ciagow na raz


def wczytaj_historie():
    # historia to lista krotek (rodzaj, produkt, kwota, sztuki)
    historia = []

    try:
        with open(PLIK_HISTORIA, "r", encoding="utf-8") as fd:
            for linia in fd:
                linia = linia.strip()
                if not linia:
                    continue

                czesci = linia.split(SEP)
                if len(czesci) != 4:
                    continue

                rodzaj, nazwa, kwota, sztuki = czesci
                try:
                    historia.append((rodzaj, nazwa, float(kwota), int(sztuki)))
                except ValueError:
                    continue
    except FileNotFoundError:
        return []  # jeszcze nic nie bylo robione

    return historia


def dopisz_do_historii(wpis):
    # "a" czyli dopisujemy na koniec pliku - dzieki temu historia rosnie
    # z uruchomienia na uruchomienie i nic starego nie ginie
    rodzaj, nazwa, kwota, sztuki = wpis
    with open(PLIK_HISTORIA, "a", encoding="utf-8") as fd:
        fd.write("{}{}{}{}{:.2f}{}{}\n".format(rodzaj, SEP, nazwa, SEP, kwota, SEP, sztuki))
