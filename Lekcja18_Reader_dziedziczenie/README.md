# Lekcja 18 - Reader plikow z dziedziczeniem

## Co to robi, po ludzku
Bierze plik, zmienia w nim komorki ktore podasz, pokazuje wynik na ekranie i zapisuje do nowego pliku.
Moze czytac i zapisywac w 4 formatach: **csv, json, txt i pickle**. Mozna np. wczytac json a zapisac csv.

Zmiana wyglada tak: `kolumna,wiersz,nowa_wartosc` (liczone od zera).

## Jak odpalic
```
python reader.py in.json out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
```
Wyjdzie plik `out.csv`:
```
gitara,3,7,0
kanapka,12,5,kubek
pedzel,17,34,5
plakat,czerwony,8,0
```

## Co z lekcji tu jest
- klasa bazowa `FileHandler` i 4 klasy dzieci: `CsvHandler`, `JsonHandler`, `TxtHandler`, `PickleHandler`
- wspolna robota (zmiany, wyswietlanie) jest w rodzicu, dzieci umia tylko czytac i pisac swoj format
- wyjatki: zly format, brak pliku, zmiana poza plikiem
