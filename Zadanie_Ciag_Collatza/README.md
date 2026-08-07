# Ciąg Collatza

Program pobiera liczbę x (od 1 do 100) i wypisuje długość ciągu Collatza,
czyli ile wyrazów ma ciąg od podanej liczby aż do 1.

Zasada:
- jeśli liczba jest parzysta -> następna to `x / 2`
- jeśli nieparzysta -> następna to `3x + 1`
- kończymy, gdy wyjdzie 1

## Jak uruchomić

```
python collatz.py
```

Potem wpisujemy liczbę i Enter.

## Przykład

```
Podaj liczbe od 1 do 100: 6
6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
Dlugosc ciagu Collatza: 9
```

## Opis kodu linijka po linijce (na chłopski rozum)

```python
x = int(input("Podaj liczbe od 1 do 100: "))
```
`input(...)` wyświetla pytanie i czeka, aż coś wpiszemy. To, co wpiszemy, jest tekstem,
dlatego `int(...)` zamienia ten tekst na liczbę — inaczej nie dałoby się jej dzielić ani mnożyć.

```python
if x < 1 or x > 100:
    print("Liczba musi byc z zakresu od 1 do 100")
else:
```
Sprawdzenie na wejściu, czy liczba mieści się w zakresie z zadania.
`or` znaczy "albo": jeśli za mała ALBO za duża, to wypisujemy komunikat i program się kończy.
Jeśli liczba jest w porządku, wykonuje się cały blok po `else`.

```python
    licznik = 1
```
Licznik wyrazów ciągu. Startuje od 1, bo sama liczba podana przez użytkownika to już pierwszy wyraz ciągu
(np. dla x = 1 ciąg ma jeden wyraz, więc odpowiedź to 1).

```python
    ciag = str(x)
```
Zmienna na podgląd ciągu. `str(x)` zamienia liczbę na tekst, żeby móc ją dopisywać do tekstu.
Ta linia nie jest wymagana w zadaniu — służy tylko do tego, żeby widzieć, co program po drodze liczy.

```python
    while x != 1:
```
Pętla, która kręci się tak długo, jak długo x nie jest równy 1 (`!=` znaczy "różne od").
W momencie, gdy x zrobi się 1, pętla sama się kończy — dokładnie tak jak w treści zadania.

```python
        if x % 2 == 0:
            x = x // 2
```
`%` to reszta z dzielenia. Jeśli reszta z dzielenia przez 2 wynosi 0, to liczba jest parzysta.
Wtedy dzielimy ją na pół. `//` to dzielenie całkowite — daje 8, a nie 8.0, więc dalej pracujemy na ładnych liczbach całkowitych.

```python
        else:
            x = 3 * x + 1
```
W przeciwnym wypadku (liczba nieparzysta) nowym x jest 3x + 1.

```python
        licznik += 1
```
Doliczamy jeden wyraz ciągu. `licznik += 1` to skrót od `licznik = licznik + 1`.

```python
        ciag = ciag + " -> " + str(x)
```
Dopisujemy nowy wyraz do tekstu z całym ciągiem (znowu tylko dla podglądu).

```python
    print(ciag)
    print("Dlugosc ciagu Collatza: {}".format(licznik))
```
Na końcu, już po wyjściu z pętli, wypisujemy cały ciąg i jego długość.
`{}` w tekście to miejsce, w które `.format(licznik)` wstawia wartość licznika.

## Dobre do zapamiętania

- Wcięcia (4 spacje) decydują o tym, co należy do `if`, `else` i `while` — to nie ozdoba.
- W `while` musi być coś, co zmienia warunek (tutaj zmienia się x), inaczej program kręciłby się bez końca.
- Ciąg Collatza dla 27 ma aż 112 wyrazów i dochodzi do 9232 — mała liczba, a robi niemałą wycieczkę.
