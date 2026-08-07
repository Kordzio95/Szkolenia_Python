# Ten plik sam nic nie liczy - jest tylko po to, zeby dzialala komenda z tresci zadania:
#   python reader.py in.csv out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
#
# Caly kod siedzi w pliku "program do zarządzania plikami.py", a tutaj go tylko odpalamy.
# Trzeba tak, bo nazwa glownego pliku ma spacje i polskie znaki, a to bywa niewygodne w terminalu.

import os
import runpy  # pozwala uruchomic inny plik .py tak, jakby byl odpalony bezposrednio

# skladamy sciezke do glownego pliku lezacego obok tego pliku
# os.path.join dba o to, zeby dzialalo i na Windowsie, i na Linuksie
sciezka = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "program do zarządzania plikami.py"
)

# run_path udaje uruchomienie z terminala, wiec glowny program widzi te same argumenty (sys.argv)
runpy.run_path(sciezka, run_name="__main__")
