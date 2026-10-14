# Zadanie SQLAlchemy - ORM i program accountant
# To samo co w zadaniu z Flaskiem, tylko dane zamiast w plikach siedza w bazie SQLite
# Kazda akcja zapisuje sie w jednej transakcji, albo wszystko albo nic
#
# Odpalanie:
#   pip install -r requirements.txt
#   flask --app app db upgrade      <- tworzy baze z migracji w folderze migrations
#   flask --app app run --debug
# Sprawdzenie czy baza sie zgadza:
#   python sprawdz_baze.py

from datetime import datetime  # do zapisania kiedy byla operacja

from flask import Flask, flash, redirect, render_template, request, url_for  # rzeczy z flaska
from flask_alembic import Alembic  # migracje bazy, tak jak na lekcji
from flask_sqlalchemy import SQLAlchemy  # ORM, czyli tabele jako klasy pythona

app = Flask(__name__)  # tworzymy aplikacje
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accountant.db"  # baza to plik accountant.db (tworzy sie w folderze instance)
app.secret_key = "zmien-mnie-na-cos-tajnego"  # klucz do komunikatow flash

db = SQLAlchemy(app)  # podpinamy SQLAlchemy do aplikacji


class Konto(db.Model):  # tabela z kontem, bedzie w niej jeden wiersz
    id = db.Column(db.Integer, primary_key=True)  # numer wiersza, zawsze 1
    saldo = db.Column(db.Float, nullable=False, default=0.0)  # stan konta


class Produkt(db.Model):  # tabela z magazynem
    id = db.Column(db.Integer, primary_key=True)  # numer produktu
    nazwa = db.Column(db.String(120), unique=True, nullable=False)  # nazwa, nie moze sie powtarzac
    cena = db.Column(db.Float, nullable=False)  # cena za sztuke
    ilosc = db.Column(db.Integer, nullable=False, default=0)  # ile sztuk na stanie


class Operacja(db.Model):  # tabela z historia, kazda akcja to jeden wiersz
    id = db.Column(db.Integer, primary_key=True)  # numer operacji
    rodzaj = db.Column(db.String(20), nullable=False)  # saldo, zakup albo sprzedaz
    produkt = db.Column(db.String(120), nullable=True)  # nazwa produktu, przy saldzie pusto
    cena = db.Column(db.Float, nullable=False, default=0.0)  # cena za sztuke
    ilosc = db.Column(db.Integer, nullable=False, default=0)  # ile sztuk
    kwota = db.Column(db.Float, nullable=False)  # o ile zmienilo sie konto, plus albo minus
    data = db.Column(db.DateTime, nullable=False, default=datetime.now)  # kiedy to bylo, wpisuje sie samo


class BladOperacji(Exception):  # nasz wyjatek jak czegos nie da sie zrobic
    pass  # nic wiecej nie potrzebuje


def pobierz_konto():  # bierze wiersz z kontem albo go tworzy
    konto = db.session.get(Konto, 1)  # szukamy konta o id 1
    if konto is None:  # jak go jeszcze nie ma (pierwszy start)
        konto = Konto(id=1, saldo=0.0)  # tworzymy z zerem
        db.session.add(konto)  # dodajemy do sesji, zapisze sie przy commit
    return konto  # oddajemy konto


def wykonaj(akcja):  # odpala akcje w jednej transakcji
    try:  # probujemy
        akcja()  # robimy wszystkie zmiany (konto, magazyn, historia)
        db.session.commit()  # i zapisujemy wszystko na raz
    except BladOperacji:  # nasz blad, np za malo kasy
        db.session.rollback()  # cofamy wszystko co sie zmienilo
        raise  # i puszczamy blad dalej zeby strona go pokazala
    except Exception:  # jakis inny blad z bazy
        db.session.rollback()  # tez cofamy wszystko
        raise BladOperacji("Blad bazy danych - operacja wycofana.")  # i mowimy ze nic sie nie zapisalo


def zmiana_salda(wartosc):  # zmiana salda
    def akcja():  # w srodku zmiany ktore pojda w jednej transakcji
        konto = pobierz_konto()  # bierzemy konto
        if konto.saldo + wartosc < 0:  # nie mozna zejsc pod kreske
            raise BladOperacji("Saldo nie moze byc ujemne.")  # blad
        konto.saldo += wartosc  # zmieniamy saldo
        db.session.add(Operacja(rodzaj="saldo", kwota=wartosc))  # dopisujemy do historii
    wykonaj(akcja)  # odpalamy w transakcji


def zakup(nazwa, cena, ilosc):  # zakup towaru
    nazwa = nazwa.strip().lower()  # porzadkujemy nazwe

    def akcja():  # zmiany do jednej transakcji
        if not nazwa:  # pusta nazwa
            raise BladOperacji("Podaj nazwe produktu.")  # blad
        if cena <= 0 or ilosc <= 0:  # zera albo minusy
            raise BladOperacji("Cena i ilosc musza byc wieksze od zera.")  # blad
        konto = pobierz_konto()  # konto
        koszt = cena * ilosc  # ile placimy
        if koszt > konto.saldo:  # nie stac nas
            raise BladOperacji("Za malo srodkow: potrzeba {:.2f}, jest {:.2f}.".format(koszt, konto.saldo))  # blad
        produkt = Produkt.query.filter_by(nazwa=nazwa).first()  # szukamy produktu w bazie
        if produkt is None:  # nie ma go
            produkt = Produkt(nazwa=nazwa, cena=cena, ilosc=0)  # tworzymy nowy z zerem sztuk
            db.session.add(produkt)  # dodajemy do sesji
        produkt.ilosc += ilosc  # dokladamy sztuki
        produkt.cena = cena  # ustawiamy cene
        konto.saldo -= koszt  # placimy z konta
        db.session.add(Operacja(rodzaj="zakup", produkt=nazwa, cena=cena, ilosc=ilosc, kwota=-koszt))  # historia
    wykonaj(akcja)  # wszystko w jednej transakcji


def sprzedaz(nazwa, ilosc):  # sprzedaz towaru
    nazwa = nazwa.strip().lower()  # porzadkujemy nazwe

    def akcja():  # zmiany do jednej transakcji
        produkt = Produkt.query.filter_by(nazwa=nazwa).first()  # szukamy produktu
        if produkt is None:  # nie ma
            raise BladOperacji("Produktu '{}' nie ma w magazynie.".format(nazwa))  # blad
        if ilosc <= 0:  # zla ilosc
            raise BladOperacji("Ilosc musi byc wieksza od zera.")  # blad
        if ilosc > produkt.ilosc:  # za malo na stanie
            raise BladOperacji("Za malo towaru. W magazynie: {} szt.".format(produkt.ilosc))  # blad
        konto = pobierz_konto()  # konto
        przychod = produkt.cena * ilosc  # ile zarobimy, cena z magazynu
        produkt.ilosc -= ilosc  # zdejmujemy z magazynu
        konto.saldo += przychod  # kasa na konto
        db.session.add(Operacja(rodzaj="sprzedaz", produkt=nazwa, cena=produkt.cena,  # historia
                                ilosc=ilosc, kwota=przychod))  # z kwota na plus
        if produkt.ilosc == 0:  # jak sie skonczyl
            db.session.delete(produkt)  # usuwamy z magazynu
    wykonaj(akcja)  # w jednej transakcji


def liczba(pole, calkowita=False):  # wyciaga liczbe z formularza
    tekst = request.form.get(pole, "").strip().replace(",", ".")  # bierzemy pole, przecinek na kropke
    try:  # zamiana
        return int(tekst) if calkowita else float(tekst)  # calkowita albo nie
    except ValueError:  # nie liczba
        raise BladOperacji("Pole '{}' musi byc liczba.".format(pole))  # nasz blad


@app.route("/", methods=["GET", "POST"])  # strona glowna
def index():  # funkcja strony glownej
    if request.method == "POST":  # wyslano formularz
        akcja = request.form.get("akcja")  # ktory formularz
        try:  # moze sie nie udac
            if akcja == "zakup":  # zakup
                zakup(request.form.get("nazwa", ""), liczba("cena"), liczba("ilosc", True))  # robimy zakup
                flash("Zakup zapisany.", "ok")  # komunikat
            elif akcja == "sprzedaz":  # sprzedaz
                sprzedaz(request.form.get("nazwa", ""), liczba("ilosc", True))  # robimy sprzedaz
                flash("Sprzedaz zapisana.", "ok")  # komunikat
            elif akcja == "saldo":  # saldo
                zmiana_salda(liczba("wartosc"))  # zmieniamy saldo
                flash("Saldo zmienione.", "ok")  # komunikat
            else:  # nie wiadomo co
                flash("Nieznana akcja.", "blad")  # komunikat bledu
        except BladOperacji as blad:  # nie udalo sie
            flash(str(blad), "blad")  # pokazujemy powod
        return redirect(url_for("index"))  # przekierowanie na strone glowna

    konto = db.session.get(Konto, 1)  # bierzemy konto z bazy
    magazyn = {p.nazwa: p for p in Produkt.query.order_by(Produkt.nazwa).all()}  # magazyn jako slownik posortowany po nazwie
    return render_template("index.html", konto=konto.saldo if konto else 0.0, magazyn=magazyn)  # pokazujemy strone


@app.route("/historia/")  # cala historia
@app.route("/historia/<int:start>/<int:koniec>/")  # zakres ze slashem
@app.route("/historia/<int:start>/<int:koniec>")  # zakres bez slasha
def historia(start=None, koniec=None):  # funkcja podstrony historia
    wszystko = Operacja.query.order_by(Operacja.id).all()  # wszystkie operacje z bazy po kolei
    blad = None  # narazie bez bledu

    if start is None:  # bez zakresu
        wpisy = list(enumerate(wszystko, start=1))  # wszystko z numerkami
    elif not wszystko:  # pusta historia
        wpisy, blad = [], "Historia jest pusta."  # nic nie ma
    elif start < 1 or koniec > len(wszystko) or start > koniec:  # zly zakres
        wpisy = []  # nic nie pokazujemy
        blad = "Zly zakres {}-{}. Mozesz wybrac od 1 do {}.".format(start, koniec, len(wszystko))  # podpowiedz zakresu
    else:  # dobry zakres
        wpisy = list(enumerate(wszystko, start=1))[start - 1:koniec]  # wycinamy kawalek

    return render_template("historia.html", wpisy=wpisy, blad=blad, ile=len(wszystko))  # pokazujemy strone


alembic = Alembic()  # tworzymy obiekt do migracji, jak na lekcji na koncu pliku
alembic.init_app(app)  # podpinamy go do aplikacji, od teraz sa komendy flask db ...

if __name__ == "__main__":  # jak odpalamy python app.py
    app.run(debug=True)  # start serwera
