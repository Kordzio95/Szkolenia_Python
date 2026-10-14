# Lekcja 14 - Pogoda z API (venv i pip)

## Co to robi, po ludzku
Pytasz program o jakis dzien, a on sprawdza w internecie (strona open-meteo) czy bedzie padac.
Odpowiada jednym z trzech: **Bedzie padac**, **Nie bedzie padac** albo **Nie wiem**.
Wynik zapisuje do pliku `wyniki_pogody.txt`, wiec jak drugi raz zapytasz o ten sam dzien, to nie leci do internetu tylko bierze z pliku.
Jak nic nie wpiszesz i dasz Enter, to sprawdza jutro.

## Jak odpalic
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python pogoda.py
```

## Co z lekcji tu jest
- `venv` i `pip` - biblioteka `requests` instalowana z zewnatrz
- zapytanie do API i czytanie odpowiedzi w formacie json
- zapis i odczyt z pliku, `try / except`
- daty: `datetime`, `timedelta`
