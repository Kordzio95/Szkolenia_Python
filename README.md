# Szkolenie Python — zadania

Zadania z kursu Pythona, każda lekcja w osobnym folderze. Kod komentowany prostym językiem.

## Spis lekcji

| Folder | Zadanie | Uruchomienie |
|---|---|---|
| [Lekcja5_System_ksiegowy](Lekcja5_System_ksiegowy) | Prosty system księgowy / magazyn — konto, sprzedaż, zakup, przegląd historii | `python magazyn.py` |
| [Lekcja6_Zapis_do_plikow](Lekcja6_Zapis_do_plikow) | To samo, ale konto, magazyn i historia zapisywane do plików tekstowych | `python magazyn.py` |
| [Lekcja7_Czytanie_CSV](Lekcja7_Czytanie_CSV) | Odczyt pliku CSV, nałożenie zmian z linii komend i zapis do nowego pliku | `python czytanie.py in.csv out.csv 0,0,gitara` |
| [Zadanie_Ciag_Collatza](Zadanie_Ciag_Collatza) | Długość ciągu Collatza dla liczby od 1 do 100 (if/else, while) | `python Ciąg_Coltza.py` |
| [program_do_zarządzania_plikami](program_do_zarz%C4%85dzania_plikami) | Odczyt CSV, zmiany z linii komend, wypisanie i zapis do nowego pliku | `python reader.py in.csv out.csv 0,0,gitara` |
| [Lekcja14_Pogoda_API](Lekcja14_Pogoda_API) | Sprawdzanie czy bedzie padac (API open-meteo), wyniki zapisywane do pliku | `python pogoda.py` |
| [Lekcja15_Pogoda_klasa](Lekcja15_Pogoda_klasa) | Pogoda w klasie `WeatherForecast` z `__getitem__`, `__setitem__`, `__iter__`, `items()` | `python pogoda_klasa.py` |
| [Lekcja18_Reader_dziedziczenie](Lekcja18_Reader_dziedziczenie) | Reader plikow csv/json/txt/pickle oparty na dziedziczeniu | `python reader.py in.json out.csv 0,0,gitara` |
| [Lekcja20_Accountant_Manager](Lekcja20_Accountant_Manager) | Accountant z klasa `Manager` (dekoratory `assign` i `execute`), bez globali | `python accountant.py` |
| [Web1_Projekt_HTML_CSS](Web1_Projekt_HTML_CSS) | Projekt strony glownej i podstrony Historia w HTML i CSS | otworz `index.html` |
| [Web3_Accountant_Flask](Web3_Accountant_Flask) | Accountant jako strona www we Flasku, dane w plikach | `flask --app app run` |
| [Web5_Accountant_SQLAlchemy](Web5_Accountant_SQLAlchemy) | Accountant we Flasku z baza danych SQLAlchemy i migracjami | `flask --app app db upgrade` i `flask --app app run` |

W każdym folderze jest własne README z opisem komend i tym, co z danej lekcji zostało wykorzystane.

## Co ćwiczone w kolejnych lekcjach

- **Lekcja 5** — listy, krotki, zbiory, słowniki, `enumerate`, walidacja danych wejściowych
- **Lekcja 6** — import własnych plików (`from dane import ...`), czytanie i pisanie plików (`open`, tryby `w` i `a`), `try / except FileNotFoundError`
- **Lekcja 7** — wbudowane pakiety: `sys` (argumenty z terminala), `csv` (reader i writer), `os.path` (ścieżki niezależne od systemu)
- **Ciąg Collatza** — instrukcja warunkowa `if / else`, pętla `while`, reszta z dzielenia `%`, dzielenie całkowite `//`
- **Lekcja 14** — `venv`, `pip`, biblioteka `requests`, zapytania do API, json
- **Lekcja 15** — metody specjalne `__getitem__`, `__setitem__`, `__iter__`, generatory `yield`
- **Lekcja 18** — dziedziczenie, klasa bazowa i klasy pochodne, wyjatki
- **Lekcja 20** — dekoratory, dekorator jako metoda klasy, SOLID
- **Web 1** — HTML, formularze, CSS
- **Web 3** — Flask, `render_template`, formularze POST, `redirect`, `flash`
- **Web 5** — SQLAlchemy, modele tabel, transakcje, migracje Flask-Alembic
- **Czytanie CSV** — wbudowane pakiety `sys`, `csv`, `os.path`, argumenty z terminala, `try / except`

## Jak odpalić u siebie

```bash
git clone https://github.com/Kordzio95/Szkolenia_Python.git
cd Szkolenia_Python/Lekcja7_Czytanie_CSV
python czytanie.py in.csv out.csv 0,0,gitara
```

Pliki z danymi (`konto.txt`, `magazyn.txt`, `historia.txt`, `out.csv`) nie są trzymane w repo — tworzą się same przy uruchomieniu programów.
