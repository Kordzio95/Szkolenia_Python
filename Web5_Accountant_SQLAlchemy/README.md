# Web 5 - Accountant z baza danych (SQLAlchemy)

## Co to robi, po ludzku
To samo co strona z Flaska, ale dane zamiast w plikach siedza w bazie danych SQLite.
Sa 3 tabele: `konto`, `produkt` (magazyn) i `operacja` (historia).

Kazda akcja zapisuje sie w calosci albo wcale. Np. przy zakupie zmienia sie konto, magazyn i historia
i jak cos po drodze sie wywali, to wszystko sie cofa (rollback). Dzieki temu tabele zawsze sie zgadzaja.

W repo sa migracje (folder `migrations`), a samej bazy nie wrzucam.

## Jak odpalic
```
pip install -r requirements.txt
flask --app app db upgrade
flask --app app run --debug
```
Potem w przegladarce: http://127.0.0.1:5000/

## Sprawdzenie bazy (dodatkowe)
```
python sprawdz_baze.py
```
Skrypt sprawdza czy saldo zgadza sie z historia i czy stan magazynu zgadza sie z zakupami i sprzedazami.
