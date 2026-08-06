# Prosty system ksiegowy / magazyn - zadanie z lekcji 5
# Uzywamy tego, co bylo na lekcji: listy, krotki, zbiory i slowniki.

# tu trzymamy kase firmy - na start pusty portfel
konto = 0.0

# magazyn to slownik: nazwa produktu -> slownik z cena i iloscia
# np. {"rower": {"cena": 100.0, "ilosc": 3}}
magazyn = {}

# tu wpada kazda operacja saldo/sprzedaz/zakup, zeby pozniej dalo sie ja podejrzec
historia = []

# zbior komend - w zbiorze sprawdzanie "czy jest" jest szybkie i nie ma powtorek
KOMENDY = {"saldo", "sprzedaz", "sprzedaż", "zakup", "konto", "lista", "magazyn", "przeglad", "przegląd", "koniec"}


def pokaz_komendy():
    # wypisujemy sciage z komendami, zeby user nie musial zgadywac
    print()
    print("Dostepne komendy:")
    for komenda in ["saldo", "sprzedaz", "zakup", "konto", "lista", "magazyn", "przeglad", "koniec"]:
        print(" - {}".format(komenda))


def podaj_liczbe(pytanie, tylko_calkowita=False, tylko_dodatnia=True):
    # pytamy uzytkownika o liczbe tak dlugo, az wklepie cos sensownego
    while True:
        tekst = input(pytanie).strip().replace(",", ".")  # przecinek tez lykamy jak kropke
        try:
            if tylko_calkowita:
                liczba = int(tekst)   # sztuk nie da sie miec pol
            else:
                liczba = float(tekst)  # ceny moga byc z groszami
        except ValueError:
            # ktos wpisal literki zamiast cyfr - prosimy jeszcze raz
            print("To nie jest liczba. Sprobuj jeszcze raz.")
            continue

        if tylko_dodatnia and liczba <= 0:
            # zero albo minus nie ma tu sensu (cena, sztuki)
            print("Wartosc musi byc wieksza od zera.")
            continue

        return liczba


def komenda_saldo():
    # doladowanie albo sciagniecie kasy z konta - tu minus JEST dozwolony
    global konto
    kwota = podaj_liczbe("Podaj kwote (minus = wyplata): ", tylko_dodatnia=False)

    if konto + kwota < 0:
        # nie pozwalamy zejsc pod kreske
        print("Nie mozna wykonac - na koncie zostaloby {:.2f}.".format(konto + kwota))
        return

    konto = konto + kwota
    historia.append(("saldo", "-", kwota, 1))  # krotka: co, produkt, kwota, sztuki
    print("Konto po operacji: {:.2f}".format(konto))


def komenda_sprzedaz():
    # sprzedajemy towar: z magazynu ubywa, na koncie przybywa
    global konto
    nazwa = input("Podaj nazwe produktu: ").strip().lower()

    if nazwa not in magazyn:
        # nie mozna sprzedac czegos, czego nie ma na polce
        print("Produktu '{}' nie ma w magazynie.".format(nazwa))
        return

    cena = podaj_liczbe("Podaj cene za sztuke: ")
    sztuki = podaj_liczbe("Podaj liczbe sztuk: ", tylko_calkowita=True)

    if sztuki > magazyn[nazwa]["ilosc"]:
        # wiecej niz mamy nie sprzedamy
        print("Za malo towaru. W magazynie jest tylko {} szt.".format(magazyn[nazwa]["ilosc"]))
        return

    magazyn[nazwa]["ilosc"] = magazyn[nazwa]["ilosc"] - sztuki  # zdejmujemy z polki
    konto = konto + cena * sztuki                               # kasa wpada na konto

    if magazyn[nazwa]["ilosc"] == 0:
        del magazyn[nazwa]  # jak sie skonczylo, to wywalamy pozycje ze slownika

    historia.append(("sprzedaz", nazwa, cena, sztuki))
    print("Sprzedano {} szt. '{}'. Konto: {:.2f}".format(sztuki, nazwa, konto))


def komenda_zakup():
    # kupujemy towar: z konta ubywa, w magazynie przybywa
    global konto
    nazwa = input("Podaj nazwe produktu: ").strip().lower()

    if not nazwa:
        print("Nazwa nie moze byc pusta.")
        return

    cena = podaj_liczbe("Podaj cene za sztuke: ")
    sztuki = podaj_liczbe("Podaj liczbe sztuk: ", tylko_calkowita=True)

    koszt = cena * sztuki
    if koszt > konto:
        # nie kupujemy na kreske - konto nie moze zejsc na minus
        print("Za malo kasy. Potrzeba {:.2f}, a na koncie jest {:.2f}.".format(koszt, konto))
        return

    konto = konto - koszt  # placimy

    if nazwa in magazyn:
        magazyn[nazwa]["ilosc"] = magazyn[nazwa]["ilosc"] + sztuki  # dokladamy do tego, co juz jest
        magazyn[nazwa]["cena"] = cena                               # zapamietujemy ostatnia cene zakupu
    else:
        magazyn[nazwa] = {"cena": cena, "ilosc": sztuki}            # nowy produkt na polce

    historia.append(("zakup", nazwa, cena, sztuki))
    print("Kupiono {} szt. '{}'. Konto: {:.2f}".format(sztuki, nazwa, konto))


def komenda_konto():
    # zwykly podglad ile jest kasy
    print("Stan konta: {:.2f}".format(konto))


def komenda_lista():
    # caly magazyn od gory do dolu
    if not magazyn:
        # pusty slownik w ifie zachowuje sie jak False
        print("Magazyn jest pusty.")
        return

    print("Stan magazynu:")
    for nazwa, dane in magazyn.items():
        # items() daje pary (klucz, wartosc) - wygodne w petli
        print(" - {}: {} szt. po {:.2f} (razem {:.2f})".format(
            nazwa, dane["ilosc"], dane["cena"], dane["ilosc"] * dane["cena"]))


def komenda_magazyn():
    # podglad jednego konkretnego produktu
    nazwa = input("Podaj nazwe produktu: ").strip().lower()

    if nazwa not in magazyn:
        print("Produktu '{}' nie ma w magazynie.".format(nazwa))
        return

    dane = magazyn[nazwa]
    print("{}: {} szt. po {:.2f}".format(nazwa, dane["ilosc"], dane["cena"]))


def komenda_przeglad():
    # wyciag z historii operacji od numeru do numeru
    if not historia:
        print("Nie ma jeszcze zadnych zapisanych operacji.")
        return

    od_tekst = input("Od (Enter = od poczatku): ").strip()
    do_tekst = input("Do (Enter = do konca): ").strip()

    try:
        # pusty Enter oznacza skrajna wartosc, czyli poczatek albo koniec listy
        od = 1 if od_tekst == "" else int(od_tekst)
        do = len(historia) if do_tekst == "" else int(do_tekst)
    except ValueError:
        print("Zakres trzeba podac liczbami.")
        return

    if od < 1 or do > len(historia) or od > do:
        # zakres poza lista - mowimy ile w ogole mamy zapisanych operacji
        print("Zly zakres. Zapisanych operacji: {} (od 1 do {}).".format(len(historia), len(historia)))
        return

    # enumerate daje nam numerek do kazdej operacji, start=1 zeby liczyc po ludzku od 1
    for numer, wpis in enumerate(historia, start=1):
        if od <= numer <= do:
            rodzaj, nazwa, kwota, sztuki = wpis  # rozpakowanie krotki na 4 zmienne
            if rodzaj == "saldo":
                print("{}. saldo: {:+.2f}".format(numer, kwota))
            else:
                print("{}. {}: {} - {} szt. po {:.2f} (razem {:.2f})".format(
                    numer, rodzaj, nazwa, sztuki, kwota, kwota * sztuki))


# --- glowna petla programu - kreci sie az do komendy "koniec" ---
print("=== Prosty system ksiegowy / magazyn ===")

while True:
    pokaz_komendy()
    komenda = input("Wpisz komende: ").strip().lower()

    if komenda not in KOMENDY:
        # nieznana komenda - nie wywalamy programu, tylko grzecznie prosimy o poprawna
        print("Nie znam takiej komendy.")
        continue

    if komenda == "saldo":
        komenda_saldo()
    elif komenda in ("sprzedaz", "sprzedaż"):
        komenda_sprzedaz()
    elif komenda == "zakup":
        komenda_zakup()
    elif komenda == "konto":
        komenda_konto()
    elif komenda == "lista":
        komenda_lista()
    elif komenda == "magazyn":
        komenda_magazyn()
    elif komenda in ("przeglad", "przegląd"):
        komenda_przeglad()
    elif komenda == "koniec":
        # jedyne wyjscie z petli
        print("Do zobaczenia.")
        break
