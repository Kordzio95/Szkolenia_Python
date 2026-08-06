# Ten plik nic sam nie robi - jest tylko po to, zeby dzialala komenda z tresci zadania:
#   python reader.py in.csv out.csv 0,0,gitara 3,1,kubek
# Caly kod siedzi w czytanie.py, a tutaj go tylko odpalamy.

import os
import runpy  # pozwala uruchomic inny plik .py tak, jakby byl odpalony bezposrednio

# skladamy pelna sciezke do czytanie.py obok tego pliku
# (dzieki temu dziala tez wtedy, gdy odpalamy program z innego katalogu)
sciezka = os.path.join(os.path.dirname(os.path.abspath(__file__)), "czytanie.py")

# run_path udaje uruchomienie z terminala, wiec czytanie.py widzi te same argumenty (sys.argv)
runpy.run_path(sciezka, run_name="__main__")
