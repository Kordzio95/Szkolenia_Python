# Zadanie z lekcji 15 - podstawowe interfejsy
# Ten sam program od pogody co w lekcji 14, tylko cala robota siedzi teraz w jednej klasie WeatherForecast
# Klasa umie: weather_forecast[data], weather_forecast[data] = cos, for data in weather_forecast i items()

from datetime import date, datetime, timedelta  # narzedzia do dat, tak samo jak w poprzednim zadaniu

import requests  # biblioteka do zapytan w internecie (pip install requests)

URL = (  # adres API z dziurami na nasze wartosci
    "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"  # wspolrzedne
    "&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon"  # co chcemy dostac, czyli deszcz
    "&start_date={searched_date}&end_date={searched_date}"  # jaki dzien
)  # koniec adresu


class WeatherForecast:  # nasza klasa do pogody
    BEDZIE_PADAC = "Bedzie padac"  # stala w klasie, odpowiedz jak pada
    NIE_BEDZIE_PADAC = "Nie bedzie padac"  # odpowiedz jak nie pada
    NIE_WIEM = "Nie wiem"  # odpowiedz jak nie wiadomo
    SEP = ";"  # separator w pliku

    def __init__(self, latitude, longitude, plik="wyniki_pogody.txt"):  # to sie odpala przy tworzeniu obiektu
        self.latitude = latitude  # zapamietujemy szerokosc w obiekcie
        self.longitude = longitude  # zapamietujemy dlugosc
        self.plik = plik  # zapamietujemy nazwe pliku
        self._dane = {}  # slownik {data: odpowiedz}, podkreslnik znaczy ze to "do srodka" klasy
        self._wczytaj_plik()  # od razu na starcie czytamy co bylo zapisane

    def _wczytaj_plik(self):  # metoda czyta plik z wynikami do slownika
        try:  # pliku moze nie byc
            with open(self.plik, "r", encoding="utf-8") as fd:  # otwieramy do czytania
                for linia in fd:  # linijka po linijce
                    linia = linia.strip()  # ucinamy enter
                    if linia:  # jak linijka nie jest pusta
                        data_tekst, odpowiedz = linia.split(self.SEP, 1)  # rozdzielamy po sredniku
                        self._dane[data_tekst] = odpowiedz  # wrzucamy do slownika
        except FileNotFoundError:  # nie ma pliku
            pass  # to nic, startujemy z pustym

    def zapisz_plik(self):  # metoda zapisuje caly slownik do pliku
        with open(self.plik, "w", encoding="utf-8") as fd:  # "w" nadpisuje plik od nowa
            for data_tekst, odpowiedz in self._dane.items():  # przechodzimy po wszystkich parach
                fd.write("{}{}{}\n".format(data_tekst, self.SEP, odpowiedz))  # kazda para w osobnej linijce

    def _zapytaj_api(self, data_tekst):  # metoda pyta internet o pogode
        url = URL.format(latitude=self.latitude, longitude=self.longitude,  # wstawiamy wspolrzedne z obiektu
                         searched_date=data_tekst)  # i date o ktora pytamy
        try:  # lapiemy bledy z internetu
            odp = requests.get(url, timeout=10)  # wysylamy zapytanie
            odp.raise_for_status()  # jak blad z serwera to wyjatek
            opad = odp.json()["daily"]["rain_sum"][0]  # wyciagamy sume deszczu
        except (requests.RequestException, KeyError, IndexError, ValueError):  # cos poszlo nie tak
            opad = None  # no to nie mamy wyniku
        return self._zinterpretuj(opad)  # od razu oddajemy gotowa odpowiedz tekstowa

    def _zinterpretuj(self, opad):  # zamiana liczby na tekst
        if opad is None or opad < 0:  # brak albo ujemny wynik
            return self.NIE_WIEM  # nie wiemy
        if opad > 0.0:  # cos spadnie
            return self.BEDZIE_PADAC  # bedzie padac
        return self.NIE_BEDZIE_PADAC  # zero, czyli sucho

    def __setitem__(self, data_tekst, odpowiedz):  # to dziala jak piszemy weather_forecast["2026-10-15"] = "cos"
        self._dane[data_tekst] = odpowiedz  # wpisujemy do slownika
        self.zapisz_plik()  # i od razu zapisujemy plik zeby nic nie przepadlo

    def __getitem__(self, data_tekst):  # to dziala jak piszemy weather_forecast["2026-10-15"]
        if data_tekst not in self._dane:  # jak jeszcze nie znamy tej daty
            self[data_tekst] = self._zapytaj_api(data_tekst)  # pytamy API i zapisujemy, tu sie odpala __setitem__
        return self._dane[data_tekst]  # oddajemy odpowiedz, z pliku albo swieza z API

    def __iter__(self):  # to dziala jak robimy for data in weather_forecast
        for data_tekst in self._dane:  # przechodzimy po kluczach slownika czyli datach
            yield data_tekst  # yield oddaje po jednej dacie, to jest generator

    def items(self):  # generator par (data, pogoda) tak jak w slowniku
        for data_tekst, odpowiedz in self._dane.items():  # bierzemy pary ze srodka
            yield data_tekst, odpowiedz  # i oddajemy je po kolei jako krotke


def podaj_date():  # pytanie o date, tak jak w lekcji 14
    while True:  # pytamy do skutku
        tekst = input("Podaj date (YYYY-mm-dd, Enter = jutro): ").strip()  # czytamy co wpisal
        if tekst == "":  # pusty enter
            return (date.today() + timedelta(days=1)).isoformat()  # to jutro
        try:  # sprawdzamy format
            return datetime.strptime(tekst, "%Y-%m-%d").date().isoformat()  # dobra data, oddajemy
        except ValueError:  # zla data
            print("Zly format daty. Przyklad: 2026-10-15")  # podpowiedz i jeszcze raz


if __name__ == "__main__":  # tylko jak odpalamy ten plik bezposrednio
    weather_forecast = WeatherForecast(latitude=52.99, longitude=6.95)  # tworzymy obiekt dla Stadskanaal

    data_tekst = podaj_date()  # pytamy o date
    print("{}: {}".format(data_tekst, weather_forecast[data_tekst]))  # tu dziala __getitem__

    print("\nWszystkie znane daty (iterator):")  # naglowek
    for d in weather_forecast:  # tu dziala __iter__
        print(" -", d)  # wypisujemy kazda date

    print("\nPary (data, pogoda) z items():")  # naglowek
    for d, pogoda in weather_forecast.items():  # tu dziala items()
        print(" - {}: {}".format(d, pogoda))  # wypisujemy date i pogode
