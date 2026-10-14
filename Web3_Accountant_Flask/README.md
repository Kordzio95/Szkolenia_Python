# Web 3 - Accountant na stronie www (Flask)

## Co to robi, po ludzku
Program do firmy przerobiony na strone internetowa.
- Na stronie glownej widac stan konta, magazyn i 3 formularze: **zakup** (nazwa, cena, ilosc), **sprzedaz** (nazwa, ilosc) i **zmiana salda** (kwota).
- `/historia/` pokazuje cala historie, a `/historia/3/12/` tylko operacje od 3 do 12.
- Jak podasz zly zakres, strona powie jaki zakres mozna wybrac.
- Dane dalej trzymane sa w plikach: `konto.json`, `magazyn.json`, `historia.json`.

## Jak odpalic
```
pip install -r requirements.txt
flask --app app run --debug
```
Potem w przegladarce: http://127.0.0.1:5000/

## Pliki
- `app.py` - strony i formularze (Flask)
- `ksiegowosc.py` - sama logika firmy, bez Flaska
- `templates/` - szablony HTML (base, index, historia)
- `static/style.css` - wyglad
