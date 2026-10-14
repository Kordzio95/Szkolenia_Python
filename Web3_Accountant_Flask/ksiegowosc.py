# Logika firmy (konto, magazyn, historia) wyciagnieta do osobnego pliku
# Flask tylko z tego korzysta, a sama ksiegowosc nie wie nic o stronie www
# Dane dalej siedza w plikach tak jak kaze zadanie

import json  # pliki zapisujemy w formacie json
import os  # do skladania sciezek

KATALOG = os.path.dirname(os.path.abspath(__file__))  # folder w ktorym lezy ten plik
PLIK_KONTO = os.path.join(KATALOG, "konto.json")  # plik ze stanem konta
PLIK_MAGAZYN = os.path.join(KATALOG, "magazyn.json")  # plik z magazynem
PLIK_HISTORIA = os.path.join(KATALOG, "historia.json")  # plik z historia operacji


class BladOperacji(Exception):  # nasz wlasny wyjatek, rzucamy go jak czegos nie da sie zrobic
    """Rzucamy, gdy operacji nie da sie wykonac (np. za malo srodkow)."""  # opis klasy


def _wczytaj(plik, domyslnie):  # czytanie jednego pliku json
    try:  # plik moze nie istniec
        with open(plik, "r", encoding="utf-8") as fd:  # otwieramy
            return json.load(fd)  # oddajemy to co w srodku
    except (FileNotFoundError, json.JSONDecodeError):  # brak pliku albo zepsuty
        return domyslnie  # oddajemy wartosc domyslna


def _zapisz(plik, dane):  # zapis jednego pliku json
    with open(plik, "w", encoding="utf-8") as fd:  # otwieramy do pisania
        json.dump(dane, fd, ensure_ascii=False, indent=2)  # zapisujemy ladnie


class Ksiegowosc:  # klasa z cala logika firmy
    def __init__(self):  # przy tworzeniu wczytujemy wszystko z plikow
        self.konto = float(_wczytaj(PLIK_KONTO, 0.0))  # konto, domyslnie zero
        self.magazyn = _wczytaj(PLIK_MAGAZYN, {})  # magazyn, domyslnie pusty
        self.historia = _wczytaj(PLIK_HISTORIA, [])  # historia, domyslnie pusta

    def zapisz(self):  # zapis wszystkich trzech plikow
        _zapisz(PLIK_KONTO, self.konto)  # konto
        _zapisz(PLIK_MAGAZYN, self.magazyn)  # magazyn
        _zapisz(PLIK_HISTORIA, self.historia)  # historia

    def zmiana_salda(self, wartosc):  # formularz zmiany salda
        if self.konto + wartosc < 0:  # jak by wyszedl minus
            raise BladOperacji("Saldo nie moze byc ujemne.")  # rzucamy blad, strona go pokaze
        self.konto += wartosc  # zmieniamy konto
        self.historia.append({"rodzaj": "saldo", "produkt": "", "cena": 0, "ilosc": 0,  # wpis do historii
                              "kwota": wartosc})  # z kwota zmiany
        self.zapisz()  # zapis do plikow

    def zakup(self, nazwa, cena, ilosc):  # formularz zakupu
        nazwa = nazwa.strip().lower()  # porzadkujemy nazwe
        if not nazwa:  # pusta nazwa
            raise BladOperacji("Podaj nazwe produktu.")  # blad
        if cena <= 0 or ilosc <= 0:  # zera albo minusy
            raise BladOperacji("Cena i ilosc musza byc wieksze od zera.")  # blad
        koszt = cena * ilosc  # ile placimy razem
        if koszt > self.konto:  # nie stac nas
            raise BladOperacji("Za malo srodkow: potrzeba {:.2f}, jest {:.2f}.".format(koszt, self.konto))  # blad z kwotami
        self.konto -= koszt  # zdejmujemy kase z konta
        if nazwa in self.magazyn:  # produkt juz jest
            self.magazyn[nazwa]["ilosc"] += ilosc  # dokladamy sztuki
            self.magazyn[nazwa]["cena"] = cena  # nowa cena
        else:  # nowy produkt
            self.magazyn[nazwa] = {"cena": cena, "ilosc": ilosc}  # dodajemy go
        self.historia.append({"rodzaj": "zakup", "produkt": nazwa, "cena": cena,  # wpis do historii
                              "ilosc": ilosc, "kwota": -koszt})  # kwota z minusem bo wydalismy
        self.zapisz()  # zapis

    def sprzedaz(self, nazwa, ilosc):  # formularz sprzedazy, ma tylko nazwe i ilosc
        nazwa = nazwa.strip().lower()  # porzadkujemy nazwe
        if nazwa not in self.magazyn:  # nie ma takiego towaru
            raise BladOperacji("Produktu '{}' nie ma w magazynie.".format(nazwa))  # blad
        if ilosc <= 0:  # zero albo minus
            raise BladOperacji("Ilosc musi byc wieksza od zera.")  # blad
        if ilosc > self.magazyn[nazwa]["ilosc"]:  # za malo na stanie
            raise BladOperacji("Za malo towaru. W magazynie: {} szt.".format(self.magazyn[nazwa]["ilosc"]))  # blad
        cena = self.magazyn[nazwa]["cena"]  # cene bierzemy z magazynu bo w formularzu jej nie ma
        self.magazyn[nazwa]["ilosc"] -= ilosc  # zdejmujemy z magazynu
        if self.magazyn[nazwa]["ilosc"] == 0:  # jak sie skonczyl
            del self.magazyn[nazwa]  # wywalamy z magazynu
        self.konto += cena * ilosc  # kasa na konto
        self.historia.append({"rodzaj": "sprzedaz", "produkt": nazwa, "cena": cena,  # historia
                              "ilosc": ilosc, "kwota": cena * ilosc})  # kwota na plus
        self.zapisz()  # zapis
