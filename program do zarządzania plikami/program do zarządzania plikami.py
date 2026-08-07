# Zadanie: czytanie pliku CSV, naniesienie zmian, wyswietlenie i zapis do nowego pliku.
#
# Uruchomienie z terminala:
#   python reader.py in.csv out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
#
# Kazda zmiana to "kolumna,wiersz,wartosc", liczone od 0.

import sys   # sys.argv - lista argumentow wpisanych w terminalu
import csv   # gotowy czytacz i pisacz plikow csv
import os    # os.path - sprawdzanie sciezek, dziala i na Windowsie i na Linuksie

# sys.argv[0] to nazwa programu, dlatego prawdziwe argumenty zaczynaja sie od 1
if len(sys.argv) < 3:
    print("Uzycie: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> ... <zmiana_n>")
    sys.exit(1)

plik_wejsciowy = sys.argv[1]
plik_wyjsciowy = sys.argv[2]
zmiany = sys.argv[3:]     # wszystko od trzeciego argumentu w gore to lista zmian

# sprawdzamy, czy w ogole jest z czego czytac
if not os.path.exists(plik_wejsciowy):
    print("Nie znalazlem pliku '{}'.".format(plik_wejsciowy))
    sys.exit(1)

if os.path.isdir(plik_wejsciowy):
    print("'{}' to katalog, a nie plik.".format(plik_wejsciowy))
    sys.exit(1)

# 1. Odczyt pliku do tabelki: tabela[wiersz][kolumna]
tabela = []
with open(plik_wejsciowy, "r", newline="", encoding="utf-8") as plik:
    czytacz = csv.reader(plik)
    for wiersz in czytacz:
        tabela.append(wiersz)

# 2. Nakladanie zmian po kolei
for zmiana in zmiany:
    czesci = zmiana.split(",", 2)      # dzielimy tylko na dwoch pierwszych przecinkach

    if len(czesci) != 3:
        print("Pomijam '{}' - zmiana musi byc w formie kolumna,wiersz,wartosc".format(zmiana))
        continue

    try:
        kolumna = int(czesci[0])
        wiersz = int(czesci[1])
    except ValueError:
        print("Pomijam '{}' - wspolrzedne musza byc liczbami".format(zmiana))
        continue

    wartosc = czesci[2]

    if kolumna < 0 or wiersz < 0:
        print("Pomijam '{}' - wspolrzedne nie moga byc ujemne".format(zmiana))
        continue

    if wiersz >= len(tabela) or kolumna >= len(tabela[wiersz]):
        print("Pomijam '{}' - takiego miejsca nie ma w tabeli".format(zmiana))
        continue

    tabela[wiersz][kolumna] = wartosc  # podmiana jednej komorki

# 3. Wyswietlenie zawartosci w terminalu
for wiersz in tabela:
    print(",".join(wiersz))

# 4. Zapis do pliku wyjsciowego
with open(plik_wyjsciowy, "w", newline="", encoding="utf-8") as plik:
    pisacz = csv.writer(plik)
    for wiersz in tabela:
        pisacz.writerow(wiersz)

print()
print("Zapisano do pliku: {}".format(os.path.abspath(plik_wyjsciowy)))
