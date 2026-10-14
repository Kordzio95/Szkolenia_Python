# Zadanie z lekcji 14 - obsluga biblioteki zewnetrznej (venv i pip)
# Program sprawdza czy danego dnia bedzie padac, pyta o to strone open-meteo
# i zapisuje wynik do pliku zeby drugi raz nie pytac o to samo

from datetime import date, datetime, timedelta  # bierzemy narzedzia do dat, dzisiaj, zamiana tekstu na date i dodawanie dni

import requests  # biblioteka z pip do gadania z internetem, trzeba ja doinstalowac w venv

LATITUDE = 52.99  # szerokosc geograficzna, tu jest Stadskanaal, mozna wpisac inne miasto
LONGITUDE = 6.95  # dlugosc geograficzna tego samego miejsca

PLIK_WYNIKOW = "wyniki_pogody.txt"  # nazwa pliku gdzie odkladamy wyniki
SEP = ";"  # znak ktorym rozdzielamy date od odpowiedzi w jednej linijce

URL = (  # adres API, w klamerkach wstawimy pozniej swoje wartosci
    "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"  # pierwsza czesc adresu z wspolrzednymi
    "&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon"  # chcemy deszcz godzinowy i sume na caly dzien
    "&start_date={searched_date}&end_date={searched_date}"  # od jakiego do jakiego dnia, u nas ten sam dzien
)  # koniec adresu, python sam skleja te kawalki w jeden tekst

BEDZIE_PADAC = "Bedzie padac"  # odpowiedz jak opad jest wiekszy od zera
NIE_BEDZIE_PADAC = "Nie bedzie padac"  # odpowiedz jak opad rowno zero
NIE_WIEM = "Nie wiem"  # odpowiedz jak nie ma wyniku albo jest jakis dziwny


def wczytaj_wyniki():  # funkcja czyta z pliku to co juz kiedys sprawdzilismy
    wyniki = {}  # pusty slownik, kluczem bedzie data a wartoscia odpowiedz
    try:  # probujemy otworzyc plik, moze go jeszcze nie byc
        with open(PLIK_WYNIKOW, "r", encoding="utf-8") as fd:  # otwieramy plik do czytania, with sam go potem zamknie
            for linia in fd:  # lecimy linijka po linijce
                linia = linia.strip()  # ucinamy entery i spacje z koncow
                if not linia:  # jak linijka pusta
                    continue  # to ja pomijamy i idziemy dalej
                data_tekst, odpowiedz = linia.split(SEP, 1)  # dzielimy linijke na date i odpowiedz po sredniku
                wyniki[data_tekst] = odpowiedz  # wkladamy do slownika
    except FileNotFoundError:  # jak pliku nie ma, to znaczy ze odpalamy pierwszy raz
        pass  # i nic sie nie dzieje, poprostu idziemy dalej z pustym slownikiem
    return wyniki  # oddajemy slownik z wynikami


def dopisz_wynik(data_tekst, odpowiedz):  # funkcja dopisuje jeden nowy wynik na koniec pliku
    with open(PLIK_WYNIKOW, "a", encoding="utf-8") as fd:  # tryb "a" czyli dopisywanie, nie kasuje tego co bylo
        fd.write("{}{}{}\n".format(data_tekst, SEP, odpowiedz))  # zapisujemy data;odpowiedz i enter na koncu


def podaj_date():  # funkcja pyta uzytkownika o date tak dlugo az poda dobra
    while True:  # petla bez konca, wychodzimy z niej przez return
        tekst = input("Podaj date (YYYY-mm-dd, Enter = jutro): ").strip()  # pytamy i ucinamy spacje
        if tekst == "":  # jak ktos nic nie wpisal tylko dal enter
            return (date.today() + timedelta(days=1)).isoformat()  # bierzemy jutrzejsza date i robimy z niej tekst 2026-10-15
        try:  # probujemy zamienic tekst na date
            return datetime.strptime(tekst, "%Y-%m-%d").date().isoformat()  # jak format pasuje to oddajemy date jako tekst
        except ValueError:  # jak ktos wpisal bzdury albo zly dzien
            print("Zly format daty. Przyklad: 2026-10-15")  # mowimy jak ma wygladac i pytamy znowu


def zapytaj_api(data_tekst):  # funkcja pyta API o opady dla danego dnia
    url = URL.format(latitude=LATITUDE, longitude=LONGITUDE, searched_date=data_tekst)  # wstawiamy nasze wartosci do adresu
    try:  # w internecie wszystko moze sie wywalic wiec lapiemy bledy
        odpowiedz = requests.get(url, timeout=10)  # wysylamy zapytanie, czekamy max 10 sekund
        odpowiedz.raise_for_status()  # jak strona oddala blad (np 400) to tu wyskoczy wyjatek
        dane = odpowiedz.json()  # zamieniamy odpowiedz z tekstu json na slownik pythona
        return dane["daily"]["rain_sum"][0]  # wyciagamy sume deszczu z pierwszego (i jedynego) dnia
    except (requests.RequestException, KeyError, IndexError, ValueError):  # brak netu, zla data, dziwna odpowiedz
        return None  # w takim razie nie wiemy, oddajemy None


def zinterpretuj(opad):  # funkcja zamienia liczbe z API na jedna z trzech odpowiedzi
    if opad is None or opad < 0:  # jak nie ma wyniku albo jest ujemny
        return NIE_WIEM  # to nie wiemy
    if opad > 0.0:  # jak wiecej niz zero milimetrow
        return BEDZIE_PADAC  # to bedzie padac
    return NIE_BEDZIE_PADAC  # zostalo tylko zero czyli nie bedzie padac


def main():  # glowna funkcja, tu sie wszystko zaczyna
    wyniki = wczytaj_wyniki()  # najpierw czytamy co juz mamy w pliku
    data_tekst = podaj_date()  # pytamy o date

    if data_tekst in wyniki:  # jak ta data juz jest w pliku
        print("{}: {} (z pliku)".format(data_tekst, wyniki[data_tekst]))  # to wypisujemy wynik z pliku
        return  # i konczymy, nie meczymy API niepotrzebnie

    odpowiedz = zinterpretuj(zapytaj_api(data_tekst))  # pytamy API i od razu zamieniamy liczbe na odpowiedz
    dopisz_wynik(data_tekst, odpowiedz)  # zapisujemy do pliku na przyszlosc
    print("{}: {}".format(data_tekst, odpowiedz))  # i wypisujemy na ekran


if __name__ == "__main__":  # ten warunek jest prawdziwy tylko jak odpalamy ten plik bezposrednio
    main()  # odpalamy glowna funkcje
