import korisnik
from meni import gost_meni, domacin_meni,admin_meni
from apartman import *
from korisnik import  registracija,blokiraj_korisnika
from rezervacija import *
from  karakteristika import  *
#handlers-kao sto i naziv kaze pomocnik, kada korisnik se tehnicki uloguje dobije meni namenjen njemu
# prethodna funkcija vrati opciju njegovog odabira, i spram toga se poziva zadovoljavajuca funkcija
def gost_handle(gost):
    opt = ""
    while True:
        opt = gost_meni()
        if opt == "1":
            prikazi_apartmane(pretraga_apartmana(apartmani))
        elif opt == "2":
            visekriterijumska_pretraga()
        elif opt == "3":
            najpopularniji_gradovi()
        elif opt == "4":
            rezervacija(gost)
        elif opt == "5":
            pregled_rezervacija(gost)
        elif opt == "6":
            ponisti_rezervaciju(gost)
        elif opt == "7":
            prikazi_apartmane(apartmani)
        elif opt.lower() == "x":
            return


def domacin_handle(domacin):
    opt = ""
    while True:
        opt = domacin_meni()
        if opt == "1":
            prikazi_apartmane(pretraga_apartmana())
        elif opt == "2":
            visekriterijumska_pretraga()
        elif opt == "3":
            najpopularniji_gradovi()
        elif opt == "4":
            prikazi_apartmane(apartmani)
        elif opt == "5":
            dodaj_apartman(domacin)
        elif opt == "6":
            izmeni_apartman(domacin)
        elif opt == "7":
            brisanje_apartmana(domacin)
        elif opt == "8":
            pregled_rezervacija_domacin(domacin)
        elif opt == "9":
            ponisti_prihvati_rezervaciju(domacin)
        elif opt.lower() == "x":
            return


def admin_handle(admin):
    opt = ""
    while True:
        opt = admin_meni()
        if opt == "1":
            prikazi_apartmane(pretraga_apartmana(apartmani))
        elif opt == "2":
            visekriterijumska_pretraga()
        elif opt == "3":
            najpopularniji_gradovi()
        elif opt == "4":
            pretraga_rezervacija()
        elif opt == "5":
            registracija("domacin")
        elif opt == "6":
           dodaj_dodatnu_opremu()
        elif opt == "7":
           obrisi_dodatnu_opremu()
        elif opt == "8":
           blokiraj_korisnika()
        elif opt == "9":
            korisnik.izvestaji()
        elif opt.lower() == "x":
            return

def blokirani_handle(blokiran):
    print("Vas korisnicki nalog je blokiran! Ne mozete se ulogovati na aplikaciju!")
    meni.pocetni_meni()