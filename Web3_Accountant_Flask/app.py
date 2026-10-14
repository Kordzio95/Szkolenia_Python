# Zadanie Flask - system accountant dostepny przez strone www
# Strona glowna: stan konta, magazyn i trzy formularze (zakup, sprzedaz, zmiana salda)
# Podstrona /historia/ i /historia/<start>/<koniec>/ pokazuje historie operacji
#
# Odpalanie:
#   pip install -r requirements.txt
#   flask --app app run --debug
# i w przegladarce http://127.0.0.1:5000/

from flask import Flask, flash, redirect, render_template, request, url_for  # wszystko co potrzebne z flaska

from ksiegowosc import BladOperacji, Ksiegowosc  # nasza logika firmy z drugiego pliku

app = Flask(__name__)  # tworzymy aplikacje flask
app.secret_key = "zmien-mnie-na-cos-tajnego"  # klucz jest potrzebny zeby dzialaly komunikaty flash


def liczba(pole, calkowita=False):  # wyciaga liczbe z formularza
    tekst = request.form.get(pole, "").strip().replace(",", ".")  # bierzemy pole z formularza, przecinek na kropke
    try:  # proba zamiany
        return int(tekst) if calkowita else float(tekst)  # calkowita albo z przecinkiem
    except ValueError:  # jak nie liczba
        raise BladOperacji("Pole '{}' musi byc liczba.".format(pole))  # rzucamy nasz blad


@app.route("/", methods=["GET", "POST"])  # strona glowna, GET to wejscie a POST to wyslanie formularza
def index():  # funkcja strony glownej
    ks = Ksiegowosc()  # wczytujemy stan firmy z plikow

    if request.method == "POST":  # jak ktos wyslal formularz
        akcja = request.form.get("akcja")  # sprawdzamy ktory formularz, kazdy ma ukryte pole akcja
        try:  # operacja moze sie nie udac
            if akcja == "zakup":  # formularz zakupu
                ks.zakup(request.form.get("nazwa", ""), liczba("cena"), liczba("ilosc", True))  # robimy zakup
                flash("Zakup zapisany.", "ok")  # komunikat na zielono
            elif akcja == "sprzedaz":  # formularz sprzedazy
                ks.sprzedaz(request.form.get("nazwa", ""), liczba("ilosc", True))  # robimy sprzedaz
                flash("Sprzedaz zapisana.", "ok")  # komunikat
            elif akcja == "saldo":  # formularz salda
                ks.zmiana_salda(liczba("wartosc"))  # zmieniamy saldo
                flash("Saldo zmienione.", "ok")  # komunikat
            else:  # jakas dziwna akcja
                flash("Nieznana akcja.", "blad")  # komunikat na czerwono
        except BladOperacji as blad:  # cos sie nie udalo
            flash(str(blad), "blad")  # pokazujemy powod na czerwono
        return redirect(url_for("index"))  # przekierowanie zeby odswiezenie strony nie wyslalo formularza drugi raz

    return render_template("index.html", konto=ks.konto, magazyn=ks.magazyn)  # pokazujemy strone z danymi


@app.route("/historia/")  # cala historia
@app.route("/historia/<int:start>/<int:koniec>/")  # historia od do, ze slashem na koncu
@app.route("/historia/<int:start>/<int:koniec>")  # i bez slasha, zeby oba dzialaly
def historia(start=None, koniec=None):  # funkcja podstrony historia
    ks = Ksiegowosc()  # wczytujemy dane
    wszystko = ks.historia  # cala lista operacji
    blad = None  # narazie nie ma bledu

    if start is None:  # nie podano zakresu
        wpisy = list(enumerate(wszystko, start=1))  # bierzemy wszystko z numerkami od 1
    elif not wszystko:  # historia pusta
        wpisy, blad = [], "Historia jest pusta."  # nic do pokazania
    elif start < 1 or koniec > len(wszystko) or start > koniec:  # zly zakres
        wpisy = []  # nic nie pokazujemy
        blad = "Zly zakres {}-{}. Mozesz wybrac od 1 do {}.".format(start, koniec, len(wszystko))  # i mowimy jaki zakres jest mozliwy
    else:  # zakres dobry
        wpisy = list(enumerate(wszystko, start=1))[start - 1:koniec]  # wycinamy kawalek z numerkami

    return render_template("historia.html", wpisy=wpisy, blad=blad, ile=len(wszystko))  # pokazujemy strone


if __name__ == "__main__":  # jak odpalamy python app.py
    app.run(debug=True)  # startujemy serwer w trybie debug
