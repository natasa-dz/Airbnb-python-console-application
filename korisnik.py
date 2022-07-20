import re

import tabulate

import meni
from apartman import  apartmani,izdvoj_gradove
import  karakteristika
from Helper import *
from rezervacija import  *
korisnici = {}  # glavna struktura - recnik korisnika
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def ucitaj_korisnike():
    with open("./database/korisnici.txt", "r") as file:
        linije = file.readlines()
        for linija in linije:
            linija = linija.strip().split("|")
            recnik = {
                'ime': linija[0],
                'prezime': linija[1],
                'korisnicko_ime': linija[2],
                'lozinka': linija[3],
                'broj_telefona': linija[4],
                'email': linija[5],
                'uloga': linija[6]
            }
            korisnici[recnik['korisnicko_ime']] = recnik


def sacuvaj_korisnike():
    with open("./database/korisnici.txt", "w") as file:
        for key in korisnici.keys():
            korisnik = korisnici[key]
            linija = korisnik['ime'] + "|" + korisnik['prezime'] + "|" + korisnik['korisnicko_ime'] + "|" + korisnik[
                'lozinka'] + "|" + korisnik['broj_telefona'] + "|" + korisnik['email'] + "|" + korisnik['uloga'] + "\n"
            file.write(linija)


def prijava():
    print("")
    while True:
        korisnicko_ime = input("Unesite korisnicko ime:")
        lozinka = input('Unesite lozinku:')
        if not korisnici.keys().__contains__(korisnicko_ime):
            print("Neispravan unos podataka. Pokušajte ponovo")
        elif korisnici[korisnicko_ime]['uloga'] == 'blokiran':
            print('Administrator je blokirao Vaš nalog, nemate pristup gostinskom meniju!')
            meni.pocetni_meni()
        elif korisnici[korisnicko_ime]['lozinka'] != lozinka:
            print("Neispravan unos podataka. Pokušajte ponovo")
        else:
            return korisnici[korisnicko_ime]

def registracija(uloga):
    print("Registracija novog korisnika:")
    while True:
        ime1 = input("Unesite ime: ")
        if ime1.isalpha() and len(ime1) != 0:
            break
        print("Molimo Vas unesite alfabetski karakter tj. slovo!")
    ime1 = ime1.lower()
    while True:
        prezime1 = input("Unesite prezime: ")
        if prezime1.isalpha() and len(prezime1) != 0:
            break
        print("Molimo Vas unesite alfabetski karakter tj. slovo!")
    prezime1 = prezime1.lower()

    while True:
        k_ime = input("Unesite korisnicko ime: ")
        if k_ime.isalnum() and k_ime not in korisnici.keys():
            break
        print("Korisnicko ime zauzeto. Pokusajte ponovo!")

    while True:
        lozinka = input('Unesite lozinku sa najmanje 4 karaktera: ')
        if len(lozinka) >= 4 and lozinka.isalnum():
            break
        print('Lozinka je prekratka')

    while True:
        telefon = input("Unesite broj telefona:")
        if telefon.isnumeric():
            break
        print("Molimo Vas unesite samo brojeve!")

    while True:
        email = input("Unesite email: ")
        if re.fullmatch(regex, email):
            break
        print("Unesite mejl u ispravnom formatu!")

    korisnik = {
        'ime': ime1,
        'prezime': prezime1,
        'korisnicko_ime': k_ime,
        'lozinka': lozinka,
        'broj_telefona': telefon,
        'email': email,
        'uloga': uloga
    }
    korisnici[k_ime]=korisnik
    sacuvaj_korisnike()
    print("Cestitamo! Uspesno ste se registrovali!")
    return korisnik


def blokiraj_korisnika():
    korisnicko_ime=read_str("Unesite korisnicko ime: ")
    if korisnicko_ime not in korisnici.keys():
        print("Uneto korisnicko ime ne postoji")
    elif korisnici[korisnicko_ime]['uloga']=="admin":
        print("Nije moguce blokirati administratora!")
    else:
        korisnici[korisnicko_ime]['uloga']="blokiran"
        print("Uspesno blokiran korisnik!")


def izvestaj_a():
    trazene_rezervacije={}
    datum=read_date("Unesite datum: ")
    for rezervacija in rezervacije.values():
        if rezervacija['datum'] == datum and rezervacija['status']=="prihvacena":
            trazene_rezervacije[rezervacija['sifra']]=rezervacija

    trazeni_apartmani={}
    for rez in trazene_rezervacije.values():
        trazeni_apartmani[rez['apartman']]=apartmani[rez['apartman']]
    apartman.prikazi_apartmane(trazeni_apartmani)

def izvestaj_b():
    trazene_rezervacije={}
    domacin=read_str("Unesite domacina: ")
    for rezervacija in rezervacije.values():
        a=apartmani[rezervacija['apartman']]
        if a['domacin'] == domacin and rezervacija['status']=="prihvacena":
            trazene_rezervacije[rezervacija['sifra']]=rezervacija

    trazeni_apartmani={}
    for rez in trazene_rezervacije.values():
        trazeni_apartmani[rez['apartman']]=apartmani[rez['apartman']]
    apartman.prikazi_apartmane(trazeni_apartmani)


def izvestaj_c():
    data = []
    domacini = izdvoj_domacine()
    datum = datetime.datetime.now() - datetime.timedelta(days=365)
    for domacin in domacini:
        broj_rezervacija = broj_rezervacija_domacin(domacin, datum)
        ukupna_cena = ukupna_cena_rezervacija(domacin, datum)
        data.append([domacin, broj_rezervacija, ukupna_cena])
    print(tabulate.tabulate(data, headers=['Domacin', 'Broj rezervacija', 'Ukupna cena']))

def izvestaj_d():
    data=[]
    domacini=izdvoj_domacine()
    datum=datetime.datetime.now() - datetime.timedelta(days=31)
    for domacin in domacini:
        broj_rezervacija=broj_rezervacija_domacin(domacin,datum)
        ukupna_cena=ukupna_cena_rezervacija(domacin,datum)
        data.append([domacin,broj_rezervacija,ukupna_cena])
    print(tabulate.tabulate(data,headers=['Domacin','Broj rezervacija','Ukupna cena']))

def izvestaj_e():
    korisnicko_ime=read_str("Unesite korisnicko ime domacina")
    if korisnicko_ime not in korisnici.keys():
        print("Korisnicko ime ne postoji!")
        return
    if korisnici[korisnicko_ime]['uloga']!="domacin":
        print("Greska! Izabrani korisnik nije domacin!")
        return
    datum=read_date("Unesite datum: ")
    br=broj_rezervacija_domacin_za_dan(korisnicko_ime,datum)
    cena=ukupna_cena_rezervacija_za_dan(korisnicko_ime,datum)
    print("Domacin: " +korisnicko_ime+" broj rezervacija: "+ str(br)+" ukupna cena " + str(cena))


def izvestaj_f():
    gradovi=izdvoj_gradove()
    data=[]
    ukupan_br_rezervacija=len(rezervacije.keys())
    for grad in gradovi:
        brojac=0
        for rezervacija in rezervacije.values():
            if lokacija.lokacije[apartmani[rezervacija['apartman']]['lokacija']]['adresa']['mesto']==grad:
                brojac+=1
        procenat=(brojac/ukupan_br_rezervacija) * 100
        procenat_str=str(procenat)+"%"
        odnos=str(brojac)+"/"+str(ukupan_br_rezervacija)
        data.append([grad,odnos,procenat_str])
    print(tabulate.tabulate(data,headers=['Grad','Odnos','Procenat']))

def izvestaji():
    print("")
    print("                                   IZVESTAJI                                       ")
    print("-----------------------------------------------------------------------------------")
    print("1. Lista potvrdjenih rezervisanih apartmana, za izabrani dan realizacije")
    print("2. Lista potvrdjenih izabranih apartmana za izabranog domacina")
    print("3. Godisnji pregled angazovanja domacina")
    print("4. Mesecni pregled angazovanja po domacinu")
    print("5. Ukupan broj i cena potvrdjenih rezervacija za izabrani dan i izabranog domacina")
    print("6. Pregled zastupljenosti pojedinačnih gradova u odnosu na ukupan broj rezervacija")
    print("------------------------------------------------------------------------------------")
    opt=input("Unesite opciju: ")
    if opt=="1":
        izvestaj_a()
    elif opt=="2":
        izvestaj_b()
    elif opt=="3":
        izvestaj_c()
    elif opt == "4":
        izvestaj_d()
    elif opt == "5":
        izvestaj_e()
    elif opt == "6":
        izvestaj_d()


def izdvoj_domacine():
    domacini=[]
    for korisnik in korisnici.values():
        if korisnik['uloga'] == "domacin":
            domacini.append(korisnik['korisnicko_ime'])
    return domacini

def broj_rezervacija_domacin(domacin,datum):
    count=0
    for rezervacija in rezervacije.values():
        if rezervacija['datum'] > datum and apartmani[rezervacija['apartman']]['domacin'] == domacin:
            count+=1
    return count

def broj_rezervacija_domacin_za_dan(domacin,datum):
    count=0
    for rezervacija in rezervacije.values():
        if rezervacija['datum'] == datum and apartmani[rezervacija['apartman']]['domacin'] == domacin:
            count+=1
    return count

def ukupna_cena_rezervacija(domacin,datum):
    count = 0
    for rezervacija in rezervacije.values():
        if rezervacija['datum'] > datum and apartmani[rezervacija['apartman']]['domacin'] == domacin:
            count += rezervacija['cena']
    return count

def ukupna_cena_rezervacija_za_dan(domacin,datum):
    count = 0
    for rezervacija in rezervacije.values():
        if rezervacija['datum'] == datum and apartmani[rezervacija['apartman']]['domacin'] == domacin:
            count += rezervacija['cena']
    return count

