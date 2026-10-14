# Skrypt dodatkowy - sprawdza czy w bazie wszystko sie zgadza
# 1. saldo na koncie ma byc rowne sumie kwot z historii
# 2. ilosc kazdego produktu ma byc rowna zakupy minus sprzedaze z historii
# 3. nic nie moze byc na minusie
# Odpalanie: python sprawdz_baze.py

from collections import defaultdict  # slownik ktory sam wstawia zero jak nie ma klucza

from app import Konto, Operacja, Produkt, app, db  # bierzemy tabele i baze z naszej aplikacji


def sprawdz():  # glowna funkcja sprawdzajaca
    bledy = []  # tu zbieramy wszystkie znalezione bledy
    with app.app_context():  # flask potrzebuje kontekstu aplikacji zeby gadac z baza
        konto = db.session.get(Konto, 1)  # bierzemy konto
        saldo = konto.saldo if konto else 0.0  # jak nie ma konta to zero
        operacje = Operacja.query.all()  # cala historia

        suma = sum(op.kwota for op in operacje)  # sumujemy wszystkie zmiany konta z historii
        if abs(suma - saldo) > 0.001:  # porownujemy z malym marginesem bo float lubi sie mylic
            bledy.append("Saldo {:.2f} != suma historii {:.2f}".format(saldo, suma))  # zapisujemy blad
        if saldo < 0:  # saldo na minusie
            bledy.append("Saldo jest ujemne: {:.2f}".format(saldo))  # blad

        z_historii = defaultdict(int)  # ile powinno byc sztuk wedlug historii
        for op in operacje:  # kazda operacja
            if op.rodzaj == "zakup":  # zakup
                z_historii[op.produkt] += op.ilosc  # dodajemy sztuki
            elif op.rodzaj == "sprzedaz":  # sprzedaz
                z_historii[op.produkt] -= op.ilosc  # odejmujemy sztuki

        w_bazie = {p.nazwa: p.ilosc for p in Produkt.query.all()}  # ile faktycznie jest w magazynie
        for nazwa in set(z_historii) | set(w_bazie):  # wszystkie nazwy z obu miejsc razem
            if z_historii.get(nazwa, 0) != w_bazie.get(nazwa, 0):  # jak sie nie zgadza
                bledy.append("Produkt '{}': w magazynie {}, wg historii {}".format(  # zapisujemy blad
                    nazwa, w_bazie.get(nazwa, 0), z_historii.get(nazwa, 0)))  # z obiema liczbami
            if w_bazie.get(nazwa, 0) < 0:  # ujemna ilosc
                bledy.append("Produkt '{}' ma ujemna ilosc".format(nazwa))  # blad

    if bledy:  # jak cos znalezlismy
        print("ZNALEZIONO BLEDY:")  # naglowek
        for b in bledy:  # kazdy blad
            print(" -", b)  # wypisujemy
    else:  # wszystko gra
        print("OK - baza jest spojna (operacji: {}, saldo: {:.2f}).".format(len(operacje), saldo))  # info ze ok
    return not bledy  # True jak bez bledow


if __name__ == "__main__":  # tylko jak odpalamy ten plik
    sprawdz()  # sprawdzamy
