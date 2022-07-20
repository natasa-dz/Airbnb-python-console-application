import apartman

rezervacije={}
from apartman import *
import datetime
from termin import termini,prikazi_termine,nadji_interval_za_datum

#svaki put kada dodamo novu rezervaciju, azuriramo fajl tako sto upisujemo sve vrednosti iz recnika u fajl
# time izbegavamo gresku sa ListIndexError-om, ili ipak da nam nesto ne ode u new line character, sto mi se desavalo
def sacuvaj_rezervacije():
    with open("./database/rezervacije.txt", "w") as file:
        for rezervacija in rezervacije.values():
            sifra = str(rezervacija['sifra'])
            apartman = str(rezervacija['apartman'])
            datum = rezervacija['datum'].strftime('%d/%m/%Y')
            broj_nocenja = str(rezervacija['broj_nocenja'])
            cena = str(rezervacija['cena'])
            gost = rezervacija['gost']
            status = rezervacija['status']
            linija = sifra +"|"+ apartman +"|"+ datum +"|"+ broj_nocenja +"|"+ cena +"|"+ gost +"|"+ status + "\n"
            file.write(linija)


#Ucitavamo rezervacije iz fajla, na drugoj poziciji se nalazi datum-string isparsiramo kao datum
#dodajemo u recnik rezervacija, po sifri, kroz koji onda iteriramo u zavisnosti od radnje-trazimo odredjene vrednosti
def ucitaj_rezervacije():
    with open("./database/rezervacije.txt", "r") as file:
        linije = file.readlines()
        for linija in linije:
            linija = linija.strip().split("|")
            datum=datetime.datetime.strptime(linija[2], '%d/%m/%Y')
            sifra=int(linija[0])
            apartman=int(linija[1])
            broj_nocenja=int(linija[3])
            cena=float(linija[4])
            gost=linija[5]
            status=linija[6]
            rezervacija={
                'sifra' : sifra,
                'apartman' : apartman,
                'datum' : datum,
                'broj_nocenja' : broj_nocenja,
                'cena' : cena,
                'gost' : gost,
                'status' : status
            }
            rezervacije[sifra]=rezervacija

#rezervacija,
def rezervacija(gost):
    print("Da biste rezervisali apartman, odaberite jednu od ponudjenih opcija:")
    print("")
    ponovi = True
    popust = False
    while ponovi:
        opt=""
        while True:
            print("1. Odabir apartmana direktno preko sifre")
            print("2. Odabir apartmana, prvenstveno putem pretrage apartmana")
            opt = input("Unesite opciju:")
            if opt == "1" or opt == "2":
                break
        if opt == "2":
           apartman.prikazi_aktivne_apartmane(apartman.apartmani)
        while True:
            sifra = input("Unesite sifru apartmana: ")
            if sifra.isnumeric():
                break
        ponovi=rezervisi_apartman(int(sifra),gost,popust)
        popust=True
    sacuvaj_rezervacije()

def rezervacije_header():
    print(f'{"Sifra rezervacije":^9s}|{"Sifra apartmana":^17s}|{"Pocetni datum":^15s}|{"Nocenja":^11s}|{"Cena":^25s}|{"Gost":^12s}|{"Status"}:^12s')
    print("-"*90)
def print_rezervacija(rezervacija):
    print("{:^9s}|{:^17s}|{:^15s}|{:^11s}|{:^25s}|{:^12s}{:^12s}".format
          (rezervacija['sifra'],rezervacija['apartman'],rezervacija["datum"],rezervacija["broj_nocenja"],rezervacija["cena"],rezervacija["gost"],rezervacija["status"]))





#prvo proveravamo da li je unesena sifra koju je korisnik uneo u kljucevima apartmana, ako nije-obavestimo ga o tome
#potom proveravamo da li je status apartmana-aktivan, ukoliko smo prosli obe provere
#potom uzimamo termine vezane za odredjeni apartman stavljamo u recnik termina i onda prikazujemo korisniku
#nakon toga korisnik unosi datum kada zeli da rezervise termin-validacija datuma
#nakon toga proveravamo da li izabrani datum upada u opseg naseg termina
#ako uneseni datum upada u interaval nekog termina, pitamo korisnika da unese broj dana preko time delta funkcije
# racunamo potencijalni kraj termina, ako kraj izlazi van opsega, prekidamo rezervisanje, ne moze prekoraciti moguci broj ostanka u smestaju
#kreiramo novi termin koji je tehnicki novi pocetak je jednak kraju odabranog broja dana ostanka i novi kraj je jednak vec postojecem kraju termina
#preko pop-a izbaci postojece vrednosti starog termina, formiraj novi termin, prekrojen u recnik
#nakon toga korisnik unosi podatke da li rezervise samo za sebe ili dovodi i goste, ako dovodi i goste proverava se da li broj gostiju prevazilazi kapacitet apartmana

def rezervisi_apartman(sifra,gost,popust):
    if sifra not in apartmani.keys():
        print("Uneli ste nepostojecu sifru apartmana!")
        return False

    if apartmani[sifra]['status']!="aktivan":
        print("Apartman koji ste izabrali nije aktivan!")
        return False

    apartman=apartmani[sifra]
    termini_apartmana = termini[apartman['termini']]
    print("Slobodni termini")
    prikazi_termine(termini_apartmana)
    while True:
        datum=input("Unesite datum: ")
        datum_parts=datum.split("/")
        if len(datum_parts)!=3:
            print("Uneseni datum mora biti u formatu dd/mm/yyyy!")
        else:
            dan=datum_parts[0]
            mesec=datum_parts[1]
            godina=datum_parts[2]
            if dan.isnumeric() and mesec.isnumeric() and godina.isnumeric():
                dan=int(dan)
                mesec=int(mesec)
                godina=int(godina)
                if dan<1 or dan>31:
                    print("Dan moze biti samo broj izmedju 1 i 31! Molimo Vas pokusajte ponovo!")
                elif mesec < 1 or mesec > 12:
                    print("nevalidan opseg za mesec")
                else:
                    break
            else:
                print("Dan, mesec i godina moraju biti brojevi! Molimo Vas pokusajte ponovo!")
    datum=datetime.datetime.strptime(datum,'%d/%m/%Y')
    index=nadji_interval_za_datum(termini_apartmana['datumi'],datum)
    if index==-1:
        print("Uneti datum ne pripada ni jednom slobodnom terminu!")
        return False
    broj_nocenja=""
    while True:
        broj_nocenja=input("Unesite broj nocenja: ")
        if broj_nocenja.isnumeric():
            broj_nocenja=int(broj_nocenja)
            break
    datum_end=datum + datetime.timedelta(days=broj_nocenja)
    if datum_end > termini_apartmana['datumi'][index][1]:
        print("Ne mozete prekoraciti kraj termina ")
        return False
    novi_interval1=[ termini_apartmana['datumi'][index][0],datum]
    novi_interval2=[datum_end, termini_apartmana['datumi'][index][1]]
    termini[apartman['termini']]['datumi'].pop(index)
    termini[apartman['termini']]['datumi'].insert(index,novi_interval1)
    termini[apartman['termini']]['datumi'].insert(index+1,novi_interval2)
    opt=""
    while True:
        print("Odaberite jednu od ponudjenih opcija:")
        print("----------------------------------------")
        print("1. Rezervisete apartman za sebe")
        print("2. Dolazite sa prijateljima")
        opt=input("Unesite opciju: ")
        if opt!="1" and opt!="2":
            print("Nepostojeca opcija")
        else:
            break
    if opt=="2":
        max_broj_gostiju=apartman['broj_gostiju']
        i=0
        while True:
            print("Odaberite jednu od dole ponudjenih opcija")
            print("------------------------------------------")
            print("1. Unos gostiju koje dovodite sa sobom ")
            print("2. Zavrsite sa unosom gostiju")
            opt = input("Unesite opciju: ")
            if opt != "1" and opt != "2":
                print("Nepostojeca opcija")
            else:
                if opt=="2":
                    break
                else:
                    i=i+1
                    if i==max_broj_gostiju:
                        print("Dostigli ste maksimalan broj gostiju, koje mozete povesti sa sobom u apartman!")
                        break
                    else:
                        while True:
                            ime=input("Unesite ime gosta:")
                            if ime.isalpha():
                                break
                            print("Ime moze sadrzati samo slova!")
                        while True:
                            prezime=input("Unesite prezime gosta:")
                            if prezime.isalpha():
                                break
                            print("Prezime moze sadrzati samo slova!")

    while True:
        print("1. Potvrdite rezervaciju: ")
        print("2. Odustanite od rezervacije")
        opt = input("Unesite opciju: ")
        if opt == "2":
            return False
        elif opt=="1":
            sifra_rezervacije=generisi_sifru()
            cena=apartman['cena']*broj_nocenja
            if popust:
                cena=cena*0.95
            rezervacija={
                'sifra' : sifra_rezervacije,
                'apartman' : sifra,
                'datum' : datum,
                'broj_nocenja' : broj_nocenja,
                'cena' : cena,
                'gost' : gost,
                'status' : "kreirana"
            }
            rezervacije[sifra]=rezervacija
            while True:
                print("Da li zelite da nastavite sa rezervacijom jos apartmana?")
                print("1. Rezervisite jos jedan apartman")
                print("2. Zavrsite za rezervacijom")
                print("---------------------------------------")
                opt=input("Unesite opciju:")
                if opt=="1":
                    return True
                elif opt=="2":
                    return False
        else:
            print("Nepostojeca opcija")
        sacuvaj_rezervacije()

def generisi_sifru():
    if len(rezervacije) == 0:
        return 1
    sifre=list(rezervacije.keys())
    sifre.sort(reverse = True)
    sifra=sifre[0]+1
    return sifra

#pretrazujemo vrednosti u rezervacijama i nalazimo rezervaciju gosta, vracamo rezervaciju po sifri rezervacije
def nadji_rezervacije_gosta(gost):
    trazene_rezervacije={}
    for rezervacija in rezervacije.values():
        if rezervacija['gost']==gost:
            trazene_rezervacije[rezervacija['sifra']]=rezervacija

    return trazene_rezervacije

#pravimo listu podataka koja se sastoji od svih relevantnih podataka rezervacije, pravimo tabulate funkciju
def prikazi_rezervacije(rez):
    data=[]
    for rezervacija in rez.values():
        sifra = rezervacija['sifra']
        gost = rezervacija['gost']
        datum=rezervacija['datum'].strftime('%d/%m/%Y')
        broj_nocenja=rezervacija['broj_nocenja']
        cena=rezervacija['cena']
        status=rezervacija['status']
        data.append([sifra,gost,datum,broj_nocenja,cena,status])

    print(tabulate.tabulate(data,headers=['Sifra','Gost','Datum','Broj nocenja','Cena','Status']))

#pregled rezervacije gosta, prima parametar gosta, pozivamo funkciju za pronalazenje rezervacije, i onda prikazujemo tu istu
def pregled_rezervacija(gost):
    rez=nadji_rezervacije_gosta(gost)
    prikazi_rezervacije(rez)

#isti princip kao i kod gosta, samo sto prvo u apartmanima moramo naci domacina
# kada nadjemo domacina dodajemo sifru rezervaciju u recnik trazene rezervacije, a ostatak sadrzi upravo informacije o toj istoj rezervaciji
def nadji_rezervacije_domacina(domacin):
    trazene_rezervacije = {}
    for rezervacija in rezervacije.values():
        if apartman.apartmani[rezervacija['apartman']]['domacin'] == domacin:
            trazene_rezervacije[rezervacija['sifra']] = rezervacija
    return trazene_rezervacije
#printamo vrednosti nadjene u predjasnjoj funkciji
def pregled_rezervacija_domacin(domacin):
    rez = nadji_rezervacije_domacina(domacin)
    prikazi_rezervacije(rez)

#ako ponistavamo rezervacijiu, prvo proveravamo da li rezervacija uopste i postoji, ako ne postoji vracamo korisniku da rezervacija ne postoji
#ako ostoji proveravamo da li je sifra validna poredjeci sa kljucevima, ako postoji, mi pop-ujemo ceo taj kljuc i ostatak informacija koji on sa sobom nosi
#printaj korisniku da je rezervacija ponistena
def ponisti_rezervaciju(gost):
    rez=nadji_rezervacije_gosta(gost)
    if len(rez) == 0:
        print("Nemate nijednu rezervaciju")
        return
    pregled_rezervacija(gost)
    sifra=read_int("Unesite sifru rezervacije koju zelite da ponistite")
    if sifra not in rezervacije.keys():
        print("Uneli ste sifru koja ne postoji: ")
        return
    rezervacije.pop(sifra)
    print("Rezervacija ponistena")

#status rezervacije u recniku se menja spram odabira admina
def ponisti_prihvati_rezervaciju(domacin):
    pregled_rezervacija_domacin(domacin)
    sifra=read_int("Unesite sifru rezervacije: ")
    if sifra not in rezervacije.keys():
        print("Uneli ste sifru koja ne postoji")
        return
    while True:
        print("Za prihvatanje ili odbijanje rezervacije korisnika, odaberite jednu od ponudjenih opcija")
        print("----------------------------------------------------------------------------------------")
        print("                               1. Prihvati rezervaciju ")
        print("                               2. Odbij rezervaciju  ")
        print("-----------------------------------------------------------------------------------------")
        opt=input("Unesite opciju: ")
        if opt=="1":
            rezervacije[sifra]['status']="prihvacena"
            break
        elif opt=="2":
            rezervacije[sifra]['status'] = "odbijena"
            break

def pretraga_rezervacija():
    print("Dobrodosli u pretrazivanje rezervacija!")
    print("1.Potvrdjene rezervacije")
    print("2. Odbijene rezervacije")
    print("3. Pretraga rezervacija po mestu u kom se apartman nalazi")
    print("4. Pretraga rezervacija po korisnickom imenu korisnika")
    opt=input("--->")
    if opt=="4":
        while True:
            gost=input("Unesite korisnicko ime gosta:")
            if gost.isalnum():
                break
            print("Unesite korisnicko ime korisnika u ipsravnom formatu!")
        pregled_rezervacija(gost)
    elif opt=="1":
        for rezervacija1 in rezervacije.values():
            if rezervacija1['status']=='prihvacena':
                prikazi_rezervacije(rezervacija1)
    elif opt=="2":
        for rezervacija2 in rezervacije.values():
            if rezervacija2['status']=='odbijena':
                prikazi_rezervacije(rezervacija2)
    elif opt=="3":
        print("Unesite mesto u kom se apartman, ciju rezervaciju trazimo nalazi")
        while True:
            unos = input("--->")
            if len(unos)>4:
                break
            print("Molimo Vas unesite ispravan unos! ")
            rezervacije_header()
        for apartman1 in apartman.apartmani.values():
            for rezervacija in rezervacije.values():
                mesto = lokacija.lokacije[apartman1['lokacija']]['adresa']['mesto']
                if mesto == unos:
                    sifra_apartmana=str(apartman1['sifra'])
                    if sifra_apartmana==str(rezervacija['apartman']):
                        print(rezervacija)
    else:
        print("Ne postoji rezervacija koja odgovara Vasim kriterijumima koje ste naveli!")
        meni.admin_meni()
