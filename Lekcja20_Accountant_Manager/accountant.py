# Zadanie z lekcji 20 - dekoratory i SOLID
# Ten sam program do firmy co wczesniej (saldo, zakup, sprzedaz itd.) i dalej zapis do pliku
# Nowe jest to ze komendy podpinamy do klasy Manager dekoratorem @manager.assign
# i odpalamy przez manager.execute. Nie ma zadnych zmiennych globalnych, wszystko siedzi w obiekcie

import json  # stan firmy trzymamy w jednym pliku json

KOMENDY = ["saldo", "sprzedaz", "zakup", "konto", "lista", "magazyn", "przeglad", "koniec"]  # lista komend do wyswietlania (to stala, nie zmienna)


class Manager:  # klasa ktora trzyma wszystkie dane i komendy
    def __init__(self, plik="stan_firmy.json"):  # odpala sie przy tworzeniu managera
        self.plik = plik  # nazwa pliku z zapisem
        self.actions = {}  # slownik: nazwa komendy -> funkcja ktora ja robi
        self.konto = 0.0  # stan konta na start
        self.magazyn = {}  # magazyn: {nazwa: {"cena": ..., "ilosc": ...}}
        self.historia = []  # lista wszystkich operacji do komendy przeglad
        self.dziala = True  # flaga, jak zmienimy na False to petla sie skonczy

    def assign(self, name):  # dekorator z parametrem, podpina funkcje pod nazwe komendy
        def decorate(cb):  # dostajemy funkcje ktora jest pod @manager.assign
            self.actions[name] = cb  # zapisujemy ja w slowniku pod nazwa komendy
            return cb  # oddajemy funkcje bez zmian zeby dalej dzialala normalnie
        return decorate  # assign oddaje dekorator, tak to dziala z parametrem

    def execute(self, name, *args, **kwargs):  # odpala komende po nazwie
        if name not in self.actions:  # jak nie ma takiej komendy w slowniku
            print("Nie znam takiej komendy.")  # mowimy ze nie znamy
            return None  # i nic nie robimy
        return self.actions[name](self, *args, **kwargs)  # odpalamy funkcje i dajemy jej siebie (managera)

    def wczytaj(self):  # czytanie stanu z pliku
        try:  # pliku moze nie byc albo moze byc zepsuty
            with open(self.plik, "r", encoding="utf-8") as fd:  # otwieramy plik
                dane = json.load(fd)  # wczytujemy slownik z json
            self.konto = float(dane.get("konto", 0))  # konto, jak nie ma to zero
            self.magazyn = dane.get("magazyn", {})  # magazyn, jak nie ma to pusty
            self.historia = dane.get("historia", [])  # historia, jak nie ma to pusta
        except FileNotFoundError:  # pierwszy start
            pass  # startujemy od zera
        except (json.JSONDecodeError, ValueError):  # plik zepsuty
            print("Plik {} jest uszkodzony - startujemy od zera.".format(self.plik))  # info i lecimy dalej

    def zapisz(self):  # zapis calego stanu do pliku
        with open(self.plik, "w", encoding="utf-8") as fd:  # otwieramy do pisania
            json.dump({"konto": self.konto, "magazyn": self.magazyn,  # wrzucamy konto i magazyn
                       "historia": self.historia}, fd, ensure_ascii=False, indent=2)  # i historie, ladnie sformatowane


def podaj_liczbe(pytanie, calkowita=False, dodatnia=True):  # pytamy o liczbe az ktos poda dobra
    while True:  # do skutku
        tekst = input(pytanie).strip().replace(",", ".")  # czytamy i zamieniamy przecinek na kropke
        try:  # proba zamiany na liczbe
            liczba = int(tekst) if calkowita else float(tekst)  # sztuki calkowite, kwoty z groszami
        except ValueError:  # literki zamiast cyfr
            print("To nie jest liczba. Sprobuj jeszcze raz.")  # info
            continue  # pytamy znowu
        if dodatnia and liczba <= 0:  # jak ma byc dodatnia a nie jest
            print("Wartosc musi byc wieksza od zera.")  # info
            continue  # pytamy znowu
        return liczba  # dobra liczba, oddajemy


def zarejestruj_akcje(manager):  # tu podpinamy wszystkie komendy do managera, w funkcji zeby nie bylo globali

    @manager.assign("saldo")  # podpinamy funkcje pod komende "saldo"
    def saldo(m):  # m to nasz manager
        kwota = podaj_liczbe("Podaj kwote (minus = wyplata): ", dodatnia=False)  # tu minus jest dozwolony
        if m.konto + kwota < 0:  # jak po operacji bylby debet
            print("Nie mozna wykonac - konto zeszloby pod kreske.")  # nie pozwalamy
            return  # koniec komendy
        m.konto += kwota  # zmieniamy konto
        m.historia.append({"rodzaj": "saldo", "kwota": kwota})  # zapisujemy w historii
        m.zapisz()  # od razu zapis do pliku
        print("Konto po operacji: {:.2f}".format(m.konto))  # pokazujemy nowy stan

    @manager.assign("sprzedaz")  # komenda sprzedaz
    def sprzedaz(m):  # sprzedajemy towar
        nazwa = input("Nazwa produktu: ").strip().lower()  # pytamy o nazwe, male litery
        if nazwa not in m.magazyn:  # jak takiego nie mamy
            print("Produktu '{}' nie ma w magazynie.".format(nazwa))  # info
            return  # koniec
        cena = podaj_liczbe("Cena za sztuke: ")  # za ile sprzedajemy
        ilosc = podaj_liczbe("Liczba sztuk: ", calkowita=True)  # ile sztuk
        if ilosc > m.magazyn[nazwa]["ilosc"]:  # jak chcemy sprzedac wiecej niz mamy
            print("Za malo towaru. W magazynie: {} szt.".format(m.magazyn[nazwa]["ilosc"]))  # info
            return  # koniec
        m.magazyn[nazwa]["ilosc"] -= ilosc  # zdejmujemy z magazynu
        if m.magazyn[nazwa]["ilosc"] == 0:  # jak sie skonczyl
            del m.magazyn[nazwa]  # usuwamy produkt z magazynu
        m.konto += cena * ilosc  # kasa wpada na konto
        m.historia.append({"rodzaj": "sprzedaz", "produkt": nazwa, "cena": cena, "ilosc": ilosc})  # wpis do historii
        m.zapisz()  # zapis do pliku
        print("Sprzedano. Konto: {:.2f}".format(m.konto))  # potwierdzenie

    @manager.assign("zakup")  # komenda zakup
    def zakup(m):  # kupujemy towar
        nazwa = input("Nazwa produktu: ").strip().lower()  # nazwa produktu
        if not nazwa:  # pusta nazwa
            print("Nazwa nie moze byc pusta.")  # nie przepuszczamy
            return  # koniec
        cena = podaj_liczbe("Cena za sztuke: ")  # cena
        ilosc = podaj_liczbe("Liczba sztuk: ", calkowita=True)  # ilosc
        koszt = cena * ilosc  # ile to bedzie kosztowac razem
        if koszt > m.konto:  # jak nie stac nas
            print("Za malo srodkow. Potrzeba {:.2f}, jest {:.2f}.".format(koszt, m.konto))  # info
            return  # koniec, konto nie moze byc na minusie
        m.konto -= koszt  # placimy
        if nazwa in m.magazyn:  # jak juz taki produkt mamy
            m.magazyn[nazwa]["ilosc"] += ilosc  # dokladamy sztuki
            m.magazyn[nazwa]["cena"] = cena  # i zapamietujemy ostatnia cene
        else:  # nowy produkt
            m.magazyn[nazwa] = {"cena": cena, "ilosc": ilosc}  # dodajemy do magazynu
        m.historia.append({"rodzaj": "zakup", "produkt": nazwa, "cena": cena, "ilosc": ilosc})  # historia
        m.zapisz()  # zapis
        print("Kupiono. Konto: {:.2f}".format(m.konto))  # potwierdzenie

    @manager.assign("konto")  # komenda konto
    def konto(m):  # pokazuje stan konta
        print("Stan konta: {:.2f}".format(m.konto))  # dwa miejsca po przecinku

    @manager.assign("lista")  # komenda lista
    def lista(m):  # pokazuje caly magazyn
        if not m.magazyn:  # pusty slownik
            print("Magazyn jest pusty.")  # info
            return  # koniec
        for nazwa, d in m.magazyn.items():  # kazdy produkt
            print(" - {}: {} szt. po {:.2f}".format(nazwa, d["ilosc"], d["cena"]))  # nazwa, ilosc, cena

    @manager.assign("magazyn")  # komenda magazyn
    def magazyn(m):  # pokazuje jeden produkt
        nazwa = input("Nazwa produktu: ").strip().lower()  # pytamy o nazwe
        if nazwa not in m.magazyn:  # nie ma
            print("Produktu '{}' nie ma w magazynie.".format(nazwa))  # info
            return  # koniec
        d = m.magazyn[nazwa]  # bierzemy dane produktu
        print("{}: {} szt. po {:.2f}".format(nazwa, d["ilosc"], d["cena"]))  # wypisujemy

    @manager.assign("przeglad")  # komenda przeglad
    def przeglad(m):  # pokazuje historie od do
        if not m.historia:  # nic jeszcze nie bylo
            print("Brak zapisanych operacji.")  # info
            return  # koniec
        od_t = input("Od (Enter = od poczatku): ").strip()  # od ktorej operacji
        do_t = input("Do (Enter = do konca): ").strip()  # do ktorej
        try:  # zamiana na liczby
            od = 1 if od_t == "" else int(od_t)  # pusty enter to od pierwszej
            do = len(m.historia) if do_t == "" else int(do_t)  # pusty enter to do ostatniej
        except ValueError:  # literki
            print("Zakres trzeba podac liczbami.")  # info
            return  # koniec
        if od < 1 or do > len(m.historia) or od > do:  # zakres poza historia
            print("Zly zakres. Zapisanych operacji: {} (od 1 do {}).".format(  # mowimy ile jest operacji
                len(m.historia), len(m.historia)))  # zeby uzytkownik wiedzial co wybrac
            return  # koniec
        for nr, op in enumerate(m.historia[od - 1:do], start=od):  # wycinamy kawalek listy i numerujemy od "od"
            if op["rodzaj"] == "saldo":  # operacja na saldzie
                print("{}. saldo: {:+.2f}".format(nr, op["kwota"]))  # plus albo minus przed kwota
            else:  # zakup albo sprzedaz
                print("{}. {}: {} - {} szt. po {:.2f}".format(  # ladny opis
                    nr, op["rodzaj"], op["produkt"], op["ilosc"], op["cena"]))  # numer, rodzaj, produkt, ilosc, cena

    @manager.assign("koniec")  # komenda koniec
    def koniec(m):  # zamykanie programu
        m.zapisz()  # ostatni zapis tak napewno
        m.dziala = False  # zmieniamy flage, petla w main sie zatrzyma
        print("Zapisano. Do zobaczenia.")  # pozegnanie


def main():  # glowna funkcja
    manager = Manager()  # tworzymy managera, jest zmienna lokalna a nie globalna
    zarejestruj_akcje(manager)  # podpinamy wszystkie komendy
    manager.wczytaj()  # wczytujemy stan z pliku

    aliasy = {"sprzedaż": "sprzedaz", "przegląd": "przeglad"}  # zeby dzialalo tez z polskimi literami

    while manager.dziala:  # kreci sie dopuki ktos nie wpisze koniec
        print("\nDostepne komendy: " + ", ".join(KOMENDY))  # pokazujemy komendy
        komenda = input("Wpisz komende: ").strip().lower()  # czytamy komende
        manager.execute(aliasy.get(komenda, komenda))  # zamieniamy alias jak trzeba i odpalamy przez execute


if __name__ == "__main__":  # tylko jak odpalamy ten plik bezposrednio
    main()  # start programu
