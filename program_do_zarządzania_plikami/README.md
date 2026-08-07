# Program do zarządzania plikami

Program odczytuje plik CSV, nanosi na niego zmiany podane w terminalu, wypisuje wynik na ekranie
i zapisuje go do wskazanego pliku.

## Uruchomienie

```bash
python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2> ... <zmiana_n>
```

Główny kod siedzi w pliku `program_do_zarządzania_plikami.py`. Obok leży `reader.py`, który tylko go
odpala — dzięki temu działa komenda dokładnie z treści zadania, bez walki ze spacjami w nazwie pliku.
Można też uruchomić główny plik wprost:

```bash
python program_do_zarządzania_plikami.py in.csv out.csv 0,0,gitara
```

Każda zmiana ma postać `kolumna,wiersz,wartosc` — współrzędne liczone od 0.

## Przykład

```bash
python reader.py in.csv out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
```

Wejście (`in.csv`):

```
drzwi,3,7,0
kanapka,12,5,1
pedzel,22,34,5
plakat,czerwony,8,kij
```

Wynik na ekranie i w `out.csv`:

```
gitara,3,7,0
kanapka,12,5,kubek
pedzel,17,34,5
plakat,czerwony,8,0
```

## Opis kodu na chłopski rozum

```python
import sys
import csv
import os
```
Trzy wbudowane pakiety z lekcji. `sys` — bo z niego bierzemy `argv`, czyli to, co użytkownik wpisał
w terminalu. `csv` — gotowy czytacz i pisacz plików CSV, dzięki niemu nie musimy sami ciąć tekstu po
przecinkach. `os` — a dokładniej `os.path`, do sprawdzania ścieżek; działa tak samo na Windowsie
(`c:\...`) i na Linuksie (`/...`).

```python
if len(sys.argv) < 3:
    print("Uzycie: python reader.py ...")
    sys.exit(1)
```
`sys.argv[0]` to nazwa samego programu, więc prawdziwe argumenty zaczynają się od 1. Jeśli w ogóle nie
ma pliku wejściowego i wyjściowego, to nie ma o czym gadać — wypisujemy instrukcję i wychodzimy.
`sys.exit(1)` to wyjście z kodem błędu (0 znaczy "wszystko OK", cokolwiek innego — "coś padło").

```python
plik_wejsciowy = sys.argv[1]
plik_wyjsciowy = sys.argv[2]
zmiany = sys.argv[3:]
```
Pierwszy argument to plik do czytania, drugi to plik do zapisu, a `[3:]` to wycinek listy — "weź
wszystko od trzeciego elementu w górę", czyli całą listę zmian, niezależnie od tego, ile ich jest.

```python
if not os.path.exists(plik_wejsciowy):
    ...
if os.path.isdir(plik_wejsciowy):
    ...
```
`os.path.exists` mówi, czy plik w ogóle jest na dysku, a `os.path.isdir` czy przypadkiem nie podano
katalogu zamiast pliku. Lepiej dać czytelny komunikat niż pozwolić Pythonowi wysypać się błędem.

```python
tabela = []
with open(plik_wejsciowy, "r", newline="", encoding="utf-8") as plik:
    czytacz = csv.reader(plik)
    for wiersz in czytacz:
        tabela.append(wiersz)
```
`with open(...)` otwiera plik i sam go zamyka, gdy blok się skończy — nie trzeba pamiętać o `close()`.
`csv.reader` przelatuje plik linia po linii i każdą linię daje już pociętą na komórki (listę).
Wrzucamy je do listy `tabela`, więc wychodzi z tego tabelka, w której komórkę wskazujemy jako
`tabela[wiersz][kolumna]`. `newline=""` jest po to, żeby na Windowsie nie porobiły się puste linie.

```python
for zmiana in zmiany:
    czesci = zmiana.split(",", 2)
```
Lecimy po wszystkich zmianach po kolei. `split(",", 2)` dzieli tekst tylko na dwóch pierwszych
przecinkach — to ważne, bo sama wartość może mieć przecinki w środku i nie chcemy jej pociąć.

```python
    if len(czesci) != 3:
        print("Pomijam ...")
        continue
```
Jeśli po podziale nie wyszły trzy kawałki, to zmiana jest źle wpisana. `continue` przeskakuje do
następnej zmiany, zamiast wywalać cały program.

```python
    try:
        kolumna = int(czesci[0])
        wiersz = int(czesci[1])
    except ValueError:
        print("Pomijam ... wspolrzedne musza byc liczbami")
        continue
```
Współrzędne przychodzą jako tekst, więc trzeba je zamienić na liczby. Jeśli ktoś wpisze literki,
`int()` rzuca błąd `ValueError` — łapiemy go i po prostu pomijamy tę zmianę.

```python
    if kolumna < 0 or wiersz < 0:
        ...
    if wiersz >= len(tabela) or kolumna >= len(tabela[wiersz]):
        ...
```
Dwa zabezpieczenia: nie ma współrzędnych ujemnych, i nie da się wpisać wartości w miejsce, którego
w tabeli nie ma. `len(tabela)` to liczba wierszy, `len(tabela[wiersz])` to liczba kolumn w tym wierszu.
Numerujemy od 0, więc ostatni dozwolony numer to `len(...) - 1` — dlatego warunek jest z `>=`.

```python
    tabela[wiersz][kolumna] = wartosc
```
Cała robota w jednej linijce: podmieniamy jedną komórkę w tabeli.

```python
for wiersz in tabela:
    print(",".join(wiersz))
```
Wypisanie wyniku na ekran. `",".join(wiersz)` skleja komórki jednego wiersza w jeden tekst
poprzedzielany przecinkami — czyli tak, jak to wygląda w pliku CSV.

```python
with open(plik_wyjsciowy, "w", newline="", encoding="utf-8") as plik:
    pisacz = csv.writer(plik)
    for wiersz in tabela:
        pisacz.writerow(wiersz)
```
Zapis na dysk. Tryb `"w"` znaczy "pisz od nowa" (jeśli plik istniał, jego zawartość ginie).
`csv.writer` sam wstawia przecinki i sam ogarnia wartości, w których siedzi przecinek — wtedy
opakuje je w cudzysłowy.

```python
print("Zapisano do pliku: {}".format(os.path.abspath(plik_wyjsciowy)))
```
`os.path.abspath` zamienia `out.csv` na pełną ścieżkę, więc od razu widać, gdzie plik faktycznie wylądował.

## Co z lekcji zostało wykorzystane

- **sys** — `sys.argv` (argumenty z terminala), `sys.exit()` (wyjście z kodem błędu)
- **csv** — `csv.reader` i `csv.writer` zamiast ręcznego cięcia po przecinkach
- **os.path** — `exists`, `isdir`, `abspath`, czyli ścieżki niezależne od systemu
- z wcześniejszych lekcji: `for`, `continue`, `if / else`, listy zagnieżdżone, `try / except`, `.format()`

## Obsługa błędów

| Sytuacja | Reakcja programu |
|---|---|
| za mało argumentów | wypisuje instrukcję użycia i kończy z kodem 1 |
| brak pliku wejściowego | komunikat i kod 1 |
| podano katalog zamiast pliku | komunikat i kod 1 |
| zmiana bez trzech części (np. `abc`) | pomija tę zmianę, leci dalej |
| współrzędne nie są liczbami | pomija tę zmianę |
| współrzędne ujemne | pomija tę zmianę |
| współrzędne poza tabelą | pomija tę zmianę |
