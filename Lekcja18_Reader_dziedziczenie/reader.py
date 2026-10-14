# Zadanie z lekcji 18 - dziedziczenie, kompozycja, wyjatki
# Program czyta plik (csv, json, txt albo pickle), robi w nim zmiany z terminala,
# wypisuje wynik na ekran i zapisuje do nowego pliku w wybranym formacie
#
# Odpalanie:
#   python reader.py in.json out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0

import csv  # wbudowany modul do plikow csv
import json  # wbudowany modul do plikow json
import os  # modul do sciezek i plikow na dysku
import pickle  # modul do zapisu obiektow pythona w pliku binarnym
import sys  # z tond bierzemy argumenty z terminala (sys.argv)


class FileHandler:  # klasa bazowa, taki "rodzic" dla wszystkich formatow
    def __init__(self, sciezka):  # przy tworzeniu podajemy sciezke do pliku
        self.sciezka = sciezka  # zapamietujemy sciezke
        self.dane = []  # tu beda wiersze pliku, lista list

    def wczytaj(self):  # czytanie pliku, kazdy format robi to po swojemu
        raise NotImplementedError  # w rodzicu nie ma kodu, dzieci musza to nadpisac

    def zapisz(self, dane):  # zapis pliku, tez kazdy format osobno
        raise NotImplementedError  # to samo, nadpisuja klasy pochodne

    def zastosuj_zmiany(self, zmiany):  # ta metoda jest wspolna dla wszystkich, dlatego siedzi w rodzicu
        for zmiana in zmiany:  # lecimy po kazdej zmianie typu "0,0,gitara"
            try:  # zmiana moze byc zle wpisana
                x, y, wartosc = zmiana.split(",", 2)  # dzielimy na kolumne, wiersz i wartosc (max 2 ciecia)
                x, y = int(x), int(y)  # zamieniamy kolumne i wiersz na liczby
                self.dane[y][x] = wartosc  # podmieniamy komorke, y to wiersz a x to kolumna
            except ValueError:  # jak sie nie dalo podzielic albo nie liczba
                print("Pominieto zla zmiane '{}' (format: x,y,wartosc)".format(zmiana))  # mowimy co jest nie tak
            except IndexError:  # jak wiersz albo kolumna wychodzi poza plik
                print("Pominieto zmiane '{}' - poza zakresem pliku".format(zmiana))  # tez mowimy i lecimy dalej

    def wyswietl(self):  # wypisanie zawartosci w terminalu
        for wiersz in self.dane:  # kazdy wiersz
            print(",".join(str(k) for k in wiersz))  # sklejamy komorki przecinkami i drukujemy


class CsvHandler(FileHandler):  # klasa do csv, dziedziczy po FileHandler
    def wczytaj(self):  # nadpisujemy czytanie
        with open(self.sciezka, newline="", encoding="utf-8") as fd:  # otwieramy plik, newline="" tak kaze modul csv
            self.dane = [wiersz for wiersz in csv.reader(fd)]  # czytamy wszystkie wiersze do listy

    def zapisz(self, dane):  # nadpisujemy zapis
        with open(self.sciezka, "w", newline="", encoding="utf-8") as fd:  # otwieramy do pisania
            csv.writer(fd).writerows(dane)  # zapisujemy wszystkie wiersze naraz


class JsonHandler(FileHandler):  # klasa do json
    def wczytaj(self):  # czytanie json
        with open(self.sciezka, encoding="utf-8") as fd:  # otwieramy plik
            self.dane = [[str(k) for k in wiersz] for wiersz in json.load(fd)]  # wczytujemy i robimy ze wszystkiego tekst

    def zapisz(self, dane):  # zapis json
        with open(self.sciezka, "w", encoding="utf-8") as fd:  # otwieramy do pisania
            json.dump(dane, fd, ensure_ascii=False, indent=2)  # zapisujemy ladnie z wcieciami, polskie znaki zostaja


class TxtHandler(FileHandler):  # klasa do zwyklego txt
    SEP = "\t"  # w txt rozdzielamy kolumny tabulatorem

    def wczytaj(self):  # czytanie txt
        with open(self.sciezka, encoding="utf-8") as fd:  # otwieramy plik
            self.dane = [linia.rstrip("\n").split(self.SEP) for linia in fd if linia.strip()]  # kazda niepusta linia to wiersz

    def zapisz(self, dane):  # zapis txt
        with open(self.sciezka, "w", encoding="utf-8") as fd:  # otwieramy do pisania
            for wiersz in dane:  # kazdy wiersz
                fd.write(self.SEP.join(str(k) for k in wiersz) + "\n")  # sklejamy tabulatorem i dajemy enter


class PickleHandler(FileHandler):  # klasa do pickle
    def wczytaj(self):  # czytanie pickle
        with open(self.sciezka, "rb") as fd:  # "rb" czyli czytanie binarne, pickle to nie tekst
            self.dane = pickle.load(fd)  # wczytujemy liste z pliku

    def zapisz(self, dane):  # zapis pickle
        with open(self.sciezka, "wb") as fd:  # "wb" czyli pisanie binarne
            pickle.dump(dane, fd)  # wrzucamy liste do pliku


HANDLERY = {  # slownik: rozszerzenie pliku -> jaka klasa go obsluguje
    ".csv": CsvHandler,  # csv
    ".json": JsonHandler,  # json
    ".txt": TxtHandler,  # txt
    ".pickle": PickleHandler,  # pickle
}  # koniec slownika


def utworz_handler(sciezka):  # funkcja wybiera klase po koncowce pliku
    rozszerzenie = os.path.splitext(sciezka)[1].lower()  # wyciagamy koncowke np ".json" i robimy male litery
    if rozszerzenie not in HANDLERY:  # jak takiego formatu nie obslugujemy
        raise ValueError("Nieobslugiwany format: '{}'. Dozwolone: {}".format(  # rzucamy blad z wyjasnieniem
            rozszerzenie, ", ".join(HANDLERY)))  # i podajemy jakie formaty sa dozwolone
    return HANDLERY[rozszerzenie](sciezka)  # tworzymy obiekt odpowiedniej klasy i go oddajemy


def main(argv):  # glowna funkcja, dostaje argumenty z terminala
    if len(argv) < 3:  # jak ktos nie podal conajmniej dwoch plikow
        print("Uzycie: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> ...")  # mowimy jak uzywac
        return  # i konczymy

    plik_we, plik_wy, zmiany = argv[1], argv[2], argv[3:]  # rozbieramy argumenty: wejscie, wyjscie, reszta to zmiany

    try:  # sprawdzamy czy formaty sa obslugiwane
        wejscie = utworz_handler(plik_we)  # obiekt do pliku wejsciowego
        wyjscie = utworz_handler(plik_wy)  # obiekt do pliku wyjsciowego
    except ValueError as blad:  # zly format
        print(blad)  # wypisujemy co nie tak
        return  # konczymy

    if not os.path.isfile(plik_we):  # jak pliku wejsciowego nie ma na dysku
        katalog = os.path.dirname(os.path.abspath(plik_we))  # bierzemy folder gdzie mial byc
        print("Nie ma pliku '{}'. Pliki w katalogu {}:".format(plik_we, katalog))  # mowimy ze go nie ma
        for nazwa in os.listdir(katalog):  # i pokazujemy co wogole jest w tym folderze
            print(" -", nazwa)  # kazdy plik w osobnej linijce
        return  # konczymy

    try:  # czytanie moze sie wywalic jak plik jest zepsuty
        wejscie.wczytaj()  # czytamy plik, odpali sie metoda z odpowiedniej klasy
    except (OSError, json.JSONDecodeError, pickle.UnpicklingError) as blad:  # zepsuty albo nie do odczytu
        print("Nie udalo sie odczytac pliku: {}".format(blad))  # info dla uzytkownika
        return  # konczymy

    wejscie.zastosuj_zmiany(zmiany)  # robimy zmiany, metoda z rodzica
    wejscie.wyswietl()  # pokazujemy wynik w terminalu
    wyjscie.zapisz(wejscie.dane)  # zapisujemy dane do pliku wyjsciowego w jego formacie
    print("\nZapisano do: {}".format(plik_wy))  # potwierdzenie ze sie udalo


if __name__ == "__main__":  # tylko jak odpalamy ten plik bezposrednio
    main(sys.argv)  # przekazujemy argumenty z terminala do main
