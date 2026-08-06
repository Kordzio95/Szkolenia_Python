# Czytacz CSV — czytanie.py

Program odczytuje plik CSV, nakłada na niego zmiany podane w linii komend, wypisuje wynik w terminalu i zapisuje do wskazanego pliku.

## Uruchomienie

```bash
python czytanie.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2> ... <zmiana_n>
```

Każda zmiana ma postać `kolumna,wiersz,wartosc` — współrzędne liczone od 0.

## Przykład

```bash
python czytanie.py in.csv out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
```

Wejście (`in.csv`):

```
drzwi,3,7,0
kanapka,12,5,1
pedzel,22,34,5
plakat,czerwony,8,kij
```

Wyjście (`out.csv`):

```
gitara,3,7,0
kanapka,12,5,kubek
pedzel,17,34,5
plakat,czerwony,8,0
```

## Obsługa błędów

Program nie wywala się na złych danych — pomija konkretną zmianę i mówi dlaczego:

| Sytuacja | Reakcja |
|---|---|
| brak pliku wejściowego | komunikat i wyjście z kodem 1 |
| podano katalog zamiast pliku | komunikat i wyjście z kodem 1 |
| za mało argumentów | wyświetla instrukcję użycia |
| zmiana bez trzech części (np. `abc`) | pomija tę zmianę |
| współrzędne nie są liczbami | pomija tę zmianę |
| współrzędne ujemne | pomija tę zmianę |
| współrzędne poza tabelą | pomija i podaje dostępny zakres |
| pusty plik wejściowy | komunikat i wyjście |

Na koniec program pisze, ile z podanych zmian faktycznie się nałożyło.

Wartość może zawierać przecinki — podział zmiany robi się tylko na dwóch pierwszych przecinkach (`split(",", 2)`).

## Co jest wykorzystane z lekcji

- **sys** — `sys.argv` (argumenty z terminala), `sys.exit()` (kod wyjścia przy błędzie)
- **csv** — `csv.reader` do czytania i `csv.writer` do zapisu, zamiast ręcznego cięcia po przecinkach
- **os / os.path** — `os.path.exists`, `os.path.isdir`, `os.path.abspath`
- `with open(...)` z `newline=""` — bez tego na Windowsie wychodzą puste linie między wierszami
- krotki, listy zagnieżdżone (`tabela[wiersz][kolumna]`), `try / except`

## Uwaga o nazwie pliku

Główny kod jest w `czytanie.py`. Obok leży `reader.py`, który tylko go odpala — dzięki temu działa też komenda dokładnie z treści zadania:

```bash
python reader.py in.csv out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
```
