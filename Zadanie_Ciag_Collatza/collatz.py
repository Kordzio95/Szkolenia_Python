# Zadanie: Ciag Collatza
# Podajemy liczbe x (od 1 do 100), a program liczy ile wyrazow ma ciag Collatza,
# az dojdziemy do 1.

x = int(input("Podaj liczbe od 1 do 100: "))

if x < 1 or x > 100:
    print("Liczba musi byc z zakresu od 1 do 100")
else:
    licznik = 1          # pierwszym wyrazem ciagu jest sama liczba x
    ciag = str(x)        # tu zbieram caly ciag jako tekst, zeby go pokazac na koncu

    while x != 1:
        if x % 2 == 0:
            x = x // 2       # liczba parzysta -> dzielimy na pol
        else:
            x = 3 * x + 1    # liczba nieparzysta -> 3x + 1

        licznik += 1
        ciag = ciag + " -> " + str(x)

    print(ciag)
    print("Dlugosc ciagu Collatza: {}".format(licznik))
