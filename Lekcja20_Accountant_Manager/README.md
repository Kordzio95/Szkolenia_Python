# Lekcja 20 - Accountant z klasa Manager (dekoratory, SOLID)

## Co to robi, po ludzku
To jest ten sam program do firmy co wczesniej: saldo, zakup, sprzedaz, konto, lista, magazyn, przeglad i koniec.
Wszystko dalej zapisuje sie do pliku (`stan_firmy.json`), wiec po zamknieciu nic nie ginie.

Nowe jest to, ze kazda komenda jest podpieta do klasy `Manager` dekoratorem:
```python
@manager.assign("saldo")
def saldo(m):
    ...
```
a odpalana przez `manager.execute("saldo")`.
Nie ma zadnych zmiennych globalnych, cale dane siedza w obiekcie managera.

## Jak odpalic
```
python accountant.py
```

## Co z lekcji tu jest
- dekorator z parametrem (`assign`) jako metoda klasy
- `execute` odpala funkcje po nazwie ze slownika `actions`
- brak globali, zasada jednej odpowiedzialnosci (osobno dane, osobno komendy)
