# Czytacz i poprawiacz plikow CSV - zadanie z lekcji o wbudowanych pakietach.
#
# Uruchamiamy z terminala tak:
#   python czytanie.py in.csv out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
#
# Kazda zmiana to "kolumna,wiersz,wartosc", a numerujemy od 0 (jak w liscie).

import sys   # tu siedzi argv, czyli to, co user wpisal w terminalu
import csv   # gotowy czytacz i pisacz plikow csv - nie musimy sami ciac po przecinkach
import os    # do sprawdzania, czy plik w ogole istnieje


def wczytaj_csv(sciezka):
    # wczytujemy caly plik do listy wierszy, a kazdy wiersz to lista komorek
    # czyli robi sie taka tabelka: tabela[wiersz][kolumna]
    tabela = []
    with open(sciezka, "r", newline="", encoding="utf-8") as fd:
        czytacz = csv.reader(fd)
        for wiersz in czytacz:
            tabela.append(wiersz)
    return tabela


def zapisz_csv(sciezka, tabela):
    # zapisujemy tabelke z powrotem na dysk, wiersz po wierszu
    # newline="" jest wazne, inaczej na Windowsie wyskocza puste linie miedzy wierszami
    with open(sciezka, "w", newline="", encoding="utf-8") as fd:
        pisacz = csv.writer(fd)
        for wiersz in tabela:
            pisacz.writerow(wiersz)


def pokaz_tabele(tabela):
    # wypisujemy zawartosc na ekran - tak jak wyglada w pliku, po przecinkach
    for wiersz in tabela:
        print(",".join(wiersz))


def rozbierz_zmiane(tekst):
    # rozkladamy "3,1,kubek" na kolumne, wiersz i wartosc
    # dzielimy tylko na 2 przecinkach, bo sama wartosc tez moze miec przecinki w sobie
    czesci = tekst.split(",", 2)

    if len(czesci) != 3:
        # ktos podal zmiane bez wszystkich trzech kawalkow
        print("Pomijam '{}' - zmiana musi byc w formie kolumna,wiersz,wartosc".format(tekst))
        return None

    try:
        kolumna = int(czesci[0])
        wiersz = int(czesci[1])
    except ValueError:
        # wspolrzedne to musza byc liczby, a nie literki
        print("Pomijam '{}' - wspolrzedne musza byc liczbami.".format(tekst))
        return None

    if kolumna < 0 or wiersz < 0:
        # liczymy od 0 do gory, minusow nie obslugujemy
        print("Pomijam '{}' - wspolrzedne nie moga byc ujemne.".format(tekst))
        return None

    return kolumna, wiersz, czesci[2]  # zwracamy krotke z trzema rzeczami


def zastosuj_zmiane(tabela, kolumna, wiersz, wartosc, opis):
    # wkladamy nowa wartosc w wyznaczone miejsce, ale najpierw sprawdzamy, czy takie miejsce istnieje
    if wiersz >= len(tabela):
        print("Pomijam '{}' - w pliku jest tylko {} wierszy (0-{}).".format(
            opis, len(tabela), len(tabela) - 1))
        return False

    if kolumna >= len(tabela[wiersz]):
        print("Pomijam '{}' - wiersz {} ma tylko {} kolumn (0-{}).".format(
            opis, wiersz, len(tabela[wiersz]), len(tabela[wiersz]) - 1))
        return False

    tabela[wiersz][kolumna] = wartosc  # samo podmienienie komorki
    return True


# --- tu startuje program ---

# argv[0] to nazwa skryptu, dlatego prawdziwe argumenty licza sie od 1
if len(sys.argv) < 3:
    # bez pliku wejsciowego i wyjsciowego nie ma o czym gadac
    print("Uzycie: python czytanie.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> ... <zmiana_n>")
    print("Przyklad: python czytanie.py in.csv out.csv 0,0,gitara 3,1,kubek")
    sys.exit(1)  # kod inny niz 0 mowi systemowi, ze cos poszlo nie tak

plik_wejsciowy = sys.argv[1]
plik_wyjsciowy = sys.argv[2]
zmiany = sys.argv[3:]  # wszystko od trzeciego argumentu to lista zmian

if not os.path.exists(plik_wejsciowy):
    # nie ma z czego czytac - konczymy z jasnym komunikatem, zamiast sypac bledem Pythona
    print("Nie znalazlem pliku '{}'.".format(plik_wejsciowy))
    sys.exit(1)

if os.path.isdir(plik_wejsciowy):
    # ktos podal katalog zamiast pliku
    print("'{}' to katalog, a nie plik.".format(plik_wejsciowy))
    sys.exit(1)

try:
    tabela = wczytaj_csv(plik_wejsciowy)
except OSError as blad:
    # np. brak uprawnien do pliku
    print("Nie udalo sie odczytac pliku: {}".format(blad))
    sys.exit(1)

if not tabela:
    # pusta lista w ifie zachowuje sie jak False
    print("Plik '{}' jest pusty - nie ma czego zmieniac.".format(plik_wejsciowy))
    sys.exit(1)

# przelatujemy po wszystkich zmianach po kolei i probujemy je nalozyc
udane = 0
for zmiana_tekst in zmiany:
    rozebrana = rozbierz_zmiane(zmiana_tekst)
    if rozebrana is None:
        continue  # ta zmiana byla zepsuta, lecimy do nastepnej

    kolumna, wiersz, wartosc = rozebrana  # rozpakowanie krotki na trzy zmienne
    if zastosuj_zmiane(tabela, kolumna, wiersz, wartosc, zmiana_tekst):
        udane = udane + 1

# pokazujemy wynik na ekranie
print()
print("Zawartosc po zmianach ({} z {} zmian nalozonych):".format(udane, len(zmiany)))
pokaz_tabele(tabela)

# i odkladamy na dysk
try:
    zapisz_csv(plik_wyjsciowy, tabela)
except OSError as blad:
    print("Nie udalo sie zapisac pliku: {}".format(blad))
    sys.exit(1)

print()
print("Zapisano do: {}".format(os.path.abspath(plik_wyjsciowy)))
