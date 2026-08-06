# System księgowy / magazyn — zapis do plików (lekcja 6)

Rozwinięcie zadania z lekcji 5. Konto, magazyn i historia operacji są zapisywane do plików tekstowych, więc po zamknięciu programu nic nie ginie — a historia rośnie z każdym kolejnym uruchomieniem.

## Uruchomienie

```bash
python magazyn.py
```

## Pliki projektu

| Plik | Co w nim jest |
|---|---|
| `magazyn.py` | główny program — komendy i logika |
| `dane.py` | cała „papierologia": zapis i odczyt plików |
| `konto.txt` | stan konta (jedna liczba, nadpisywany) |
| `magazyn.txt` | po jednej linii na produkt: `nazwa;cena;ilosc` |
| `historia.txt` | po jednej linii na operację: `rodzaj;produkt;kwota;sztuki` (dopisywana na koniec) |

Pliki `.txt` tworzą się same przy pierwszym uruchomieniu — jeśli ich nie ma, program startuje z zerowym kontem i pustym magazynem.

## Komendy

| Komenda | Co robi |
|---|---|
| `saldo` | dodaje lub odejmuje kwotę z konta (minus = wypłata) |
| `sprzedaz` | zdejmuje towar z magazynu i dopisuje kasę na konto |
| `zakup` | dokłada towar do magazynu i zdejmuje kasę z konta (konto nie może zejść na minus) |
| `konto` | pokazuje stan konta |
| `lista` | pokazuje cały magazyn z cenami i ilościami |
| `magazyn` | pokazuje stan jednego produktu |
| `przeglad` | wypisuje historię operacji od–do, razem z poprzednich uruchomień |
| `koniec` | zapisuje stan i kończy program |

## Co jest wykorzystane z lekcji

- **import lokalnych plików** — `from dane import ...`, logika oddzielona od obsługi plików
- **czytanie plików** — `with open(...)`, `read()`, iteracja po liniach w pętli `for`
- **pisanie plików** — tryb `"w"` (nadpisanie: konto, magazyn) i `"a"` (dopisanie: historia), `write()` i `writelines()`
- **obsługa braku pliku** — `try / except FileNotFoundError`, czyli pierwsze uruchomienie działa bez żadnych plików
- z lekcji 5: listy, krotki, zbiory, słowniki, `enumerate`, walidacja typów
