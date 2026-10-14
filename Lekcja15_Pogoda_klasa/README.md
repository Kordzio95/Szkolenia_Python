# Lekcja 15 - Pogoda w klasie (podstawowe interfejsy)

## Co to robi, po ludzku
To samo co pogoda z lekcji 14, tylko cala robota (plik i internet) jest zamknieta w jednej klasie `WeatherForecast`.
Z obiektem gada sie jak ze slownikiem:
- `weather_forecast["2026-10-15"]` - daje pogode na ten dzien (z pliku albo z internetu)
- `for data in weather_forecast` - leci po wszystkich dniach, ktore juz znamy
- `weather_forecast.items()` - daje pary (data, pogoda)

## Jak odpalic
```
pip install -r requirements.txt
python pogoda_klasa.py
```

## Co z lekcji tu jest
- metody specjalne `__getitem__`, `__setitem__`, `__iter__`
- generatory i `yield` w `__iter__` i `items()`
