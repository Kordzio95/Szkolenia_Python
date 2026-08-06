# Prosty system księgowy / magazyn — lekcja 5

Zadanie z kursu Pythona. Program w konsoli rejestruje operacje na koncie firmy i pilnuje stanu magazynu.

## Uruchomienie

```bash
python magazyn.py
```

## Komendy

| Komenda | Co robi |
|---|---|
| `saldo` | dodaje lub odejmuje kwotę z konta (minus = wypłata) |
| `sprzedaz` | zdejmuje towar z magazynu i dopisuje kasę na konto |
| `zakup` | dokłada towar do magazynu i zdejmuje kasę z konta (konto nie może zejść na minus) |
| `konto` | pokazuje stan konta |
| `lista` | pokazuje cały magazyn z cenami i ilościami |
| `magazyn` | pokazuje stan jednego produktu |
| `przeglad` | wypisuje historię operacji od–do (pusty Enter = od początku / do końca) |
| `koniec` | kończy program |

## Co jest wykorzystane z lekcji

- **listy** — historia operacji
- **krotki** — pojedynczy wpis historii `(rodzaj, produkt, kwota, sztuki)` i rozpakowanie na zmienne
- **zbiory** — zestaw dostępnych komend (szybkie `in`, brak powtórek)
- **słowniki** — magazyn `nazwa -> {"cena": ..., "ilosc": ...}`, iteracja przez `.items()`
- **enumerate** — numerowanie operacji w przeglądzie od 1
- walidacja danych wejściowych (`try/except ValueError`, typy `int` / `float`, brak wartości ujemnych tam, gdzie nie mają sensu)
