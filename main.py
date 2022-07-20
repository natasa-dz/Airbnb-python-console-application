# This is a sample Python script.
import datetime

import apartman
import meni
from korisnik import *
from karakteristika import *
from apartman import *
from lokacija import *
from termin import *
from meni import *
from rezervacija import  *
from Handlers import  *
import tabulate
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

#ucitamo sve funkcije koje pozivamo
def app_start():
    ucitaj_apartmane()
    ucitaj_lokacije()
    ucitaj_termine()
    ucitaj_karakteristike()
    ucitaj_korisnike()
    ucitaj_rezervacije()
#sacuvamo sve promene koje smo naparavili u aplikaciji i upisemo ih u relevantne destinacije koje za to sluze
def app_closing():
    sacuvaj_apartmane()
    sacuvaj_karakteristike()
    sacuvaj_korisnike()
    sacuvaj_lokacije()
    sacuvaj_termine()
    sacuvaj_rezervacije()
#prosledjujemo opciju koju smo return-ovali iz menija i i spram opcije prosledjujemo i pozivamo dalje funkcije
def app():
    while True:
        opt = pocetni_meni()
        if opt == "2":
            korisnik2 = prijava()
            if korisnik2['uloga']=="gost":
                gost_handle(korisnik2['korisnicko_ime'])
            elif korisnik2['uloga'] == "domacin":
                domacin_handle(korisnik2['korisnicko_ime'])
            else:
                admin_handle(korisnik2['korisnicko_ime'])
        elif opt == "4":
            prikazi_apartmane(apartman.pretraga_apartmana(apartman.apartmani))
        elif opt == "5":
            apartman.visekriterijumska_pretraga()
        elif opt == "6":
            apartman.najpopularniji_gradovi()
        elif opt == "1":
            registracija("gost")
        elif opt.lower() == "x":
            print("Hvala na koriscenju aplikacije!")
            return
        elif opt =="3":
            prikazi_aktivne_apartmane(apartman.apartmani)
        else:
            print("Odabrali ste nepostojecu opciju!")


#pre samog pokretanja aplikacije pripremimo podatke, tj. ucitamo ih, napravimo recnike, koji sadrze informacije
#nakon sto smo ucitali informacije, dolazi do samog pokretanja, a kada zatvaramo app cuvaju se podaci koje smo unosili/izmenili
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app_start()

    app()
    app_closing()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
