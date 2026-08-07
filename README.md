# Szkolenie Python — zadania

Zadania z kursu Pythona, każda lekcja w osobnym folderze. Kod komentowany prostym językiem.

## Spis lekcji

| Folder | Zadanie | Uruchomienie |
|---|---|---|
| [Lekcja5_System_ksiegowy](Lekcja5_System_ksiegowy) | Prosty system księgowy / magazyn — konto, sprzedaż, zakup, przegląd historii | `python magazyn.py` |
| [Lekcja6_Zapis_do_plikow](Lekcja6_Zapis_do_plikow) | To samo, ale konto, magazyn i historia zapisywane do plików tekstowych | `python magazyn.py` |
| [Lekcja7_Czytanie_CSV](Lekcja7_Czytanie_CSV) | Odczyt pliku CSV, nałożenie zmian z linii komend i zapis do nowego pliku | `python czytanie.py in.csv out.csv 0,0,gitara` |
| [Zadanie_Ciag_Collatza](Zadanie_Ciag_Collatza) | Długość ciągu Collatza dla liczby od 1 do 100 (if/else, while) | `python Ciąg_Coltza.py` |
| [Zadanie_Czytanie_CSV](Zadanie_Czytanie_CSV) | Odczyt CSV, zmiany z linii komend, wypisanie i zapis do nowego pliku | `python reader.py in.csv out.csv 0,0,gitara` |

W każdym folderze jest własne README z opisem komend i tym, co z danej lekcji zostało wykorzystane.

## Co ćwiczone w kolejnych lekcjach

- **Lekcja 5** — listy, krotki, zbiory, słowniki, `enumerate`, walidacja danych wejściowych
- **Lekcja 6** — import własnych plików (`from dane import ...`), czytanie i pisanie plików (`open`, tryby `w` i `a`), `try / except FileNotFoundError`
- **Lekcja 7** — wbudowane pakiety: `sys` (argumenty z terminala), `csv` (reader i writer), `os.path` (ścieżki niezależne od systemu)
- **Ciąg Collatza** — instrukcja warunkowa `if / else`, pętla `while`, reszta z dzielenia `%`, dzielenie całkowite `//`
- **Czytanie CSV** — wbudowane pakiety `sys`, `csv`, `os.path`, argumenty z terminala, `try / except`

## Jak odpalić u siebie

```bash
git clone https://github.com/Kordzio95/Szkolenia_Python.git
cd Szkolenia_Python/Lekcja7_Czytanie_CSV
python czytanie.py in.csv out.csv 0,0,gitara
```

Pliki z danymi (`konto.txt`, `magazyn.txt`, `historia.txt`, `out.csv`) nie są trzymane w repo — tworzą się same przy uruchomieniu programów.
