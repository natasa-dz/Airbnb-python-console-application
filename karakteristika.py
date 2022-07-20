karakteristike = {}
import  tabulate
from apartman import apartmani
from Helper import  *


#dodavanje karakteristika u recnik "karakteristike"
# kljuc=sifra karakteristike, izbacuje nam ostatak informacija vezan za karakteristike
def ucitaj_karakteristike():
    with open("./database/karakteristike.txt", "r") as file:
        linije = file.readlines()
        for linija in linije:
            linija = linija.strip().split("|")
            recnik = {
                'sifra': linija[0],
                'naziv': linija[1]
            }
            karakteristike[recnik['sifra']] = recnik



#cuvanje karakteristika-upisivanje vrednosti iz recnika u fajl
def sacuvaj_karakteristike():
    with open("./database/karakteristike.txt", "w") as file:
        for karakteristika in karakteristike.values():
            linija=karakteristika['sifra']+"|"+karakteristika['naziv']+"\n"
            file.write(linija)


#generisanje sifre-pravimo listu vec postojecih sifra, i kako bismo sprecili slucajno ponavljanje sifra, da ne dobijemo neku koju vec postoji
#poredjamo elemente u obrnutom, tj. opadajucem redosledu, kada smo ih poredjali u opadajucem redosledu, uzimamo element na nultoj poziciji, tj. najveci, i na taj nacin
#nikada nece doci do ponavljanja sifri
def generisi_sifru():
    sifre=[]
    if len(karakteristike)==0:
        return "1"
    for key in karakteristike:
        sifre.append(int(key))
    sifre.sort(reverse=True)
    sifra = sifre[0]+1
    return str(sifra)


#pravimo listu koja se sastoji od sifre karakteristike, i njenog naziva, jer funkcija tabulate prima listu listi
#nova lista oznacava novi red, do vrednosti dolazimo tako sto iteriramo kroz kroz vrednosti u recniku
def prikazi_dodatnu_opremu():
    data=[]
    for karakteristika in karakteristike.values():
        data.append([karakteristika['sifra'],karakteristika['naziv']])

    print(tabulate.tabulate(data,headers=['Sifra','Naziv']))

#unosimo naziv dodatne opreme, sifra se sama automatski generise, ne bira je korisnik, upravo da bi sprecili slucaj da se sifre poklapaju
#unosimo dodatnu opremu u vec postojeci recnik karakteristika, kljuc vec generisana sifra, u recniku se nalaze naziv i sifra
#sacuvamo promenu koju smo napravili
def dodaj_dodatnu_opremu():
    print("")
    prikazi_dodatnu_opremu()
    naziv = ""
    while True:
        naziv = input("Unesite naziv dodatne opreme koju dodajete:")
        if len(naziv) != 0:
            break
        print("Morate uneti naziv!")
    sifra = generisi_sifru()
    karakteristika = {
        'sifra' : sifra,
        'naziv' : naziv
    }
    karakteristike[sifra]=karakteristika
    sacuvaj_karakteristike()
    print("Cestitamo, uspesno ste dodali dodatnu opremu apartmana!")

#provervamo da li se sifra nalazi u kljucevima, ukoliko ne postoji, vracamo da je nepostojeca sifra
#potom proveravamo da li je uneta sifra od strane korisnika, vec dodeljena nekom apartmanu, ukoliko jeste-ne mozes obrisati odabranu karakteristiku
#ukoliko nije proslo nista, return-ujemo praznu vrednost, tj. nista, jer se vrednosti ne poklapaju, ukoliko jeste, mi popujemo element cija je odabran sifra iz karakteristika
#pozivamo funkciju sacuvaj karakteristike da bismo apdejtovali promenu
def obrisi_dodatnu_opremu():
    print("")
    prikazi_dodatnu_opremu()
    sifra=read_str("Unesite sifru opreme: ")
    if sifra not in karakteristike.keys():
        print("Nepostojeca sifra")
        return
    for apatman in apartmani.values():
        karakteristike_apartmana=apatman['karakteristike']
        for karakteristika in karakteristike_apartmana:
            if sifra == karakteristika:
                print("Nije moguce obrisati opremu koja je vec dodeljenu apartmanu!")
                return
    karakteristike.pop(sifra)
    sacuvaj_karakteristike()
    print("Cestitamo uspesno ste obrisali dodatnu opremu iz sadrzaja apartmana!")
