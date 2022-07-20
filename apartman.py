import meni
import termin

apartmani={}
from Helper import  *
import lokacija
import  tabulate
import karakteristika
import rezervacija

#pravimo recnik aktivnih apartmana, prvo uzimamo kljuceve apartmana, proveravamo za svaki kljuc, tj. apartman po sifri koji sam izvukla da li je njegov status aktivan
#ukoliko jeste-dodajem ga u  recnik

#sacuvavam apartmane tako sto upisujem sve vrednosti koje sam dodala u recnik, na kraju prilikom zatvaranja aplikacije
def sacuvaj_apartmane():
    with open("./database/apartmani.txt", "w") as file:
        for apartman in apartmani.values():
            sifra=str(apartman['sifra'])
            tip=apartman['tip']
            broj_soba=str(apartman['broj_soba'])
            broj_gostiju = str(apartman['broj_gostiju'])
            lokacija=str(apartman['lokacija'])
            termini=str(apartman['termini'])
            domacin=apartman['domacin']
            cena=str(apartman['cena'])
            status=apartman['status']
            karakteristike=",".join(apartman['karakteristike'])
            linija=sifra+"|"+tip+"|"+broj_soba+"|"+broj_gostiju+"|"+lokacija+"|"+termini+"|"+domacin+"|"+cena+"|"+status+"|"+karakteristike+"\n"
            file.write(linija)

#ucitavanje apartmana, dodajemo sve u jedan veliki recnik apartmana
def ucitaj_apartmane():
    with open("./database/apartmani.txt", "r") as file:
        linije = file.readlines()
        for linija in linije:
            linija = linija.strip().split("|")
            karakteristike=linija[9].split(",")
            apartman = {
                'sifra': int(linija[0]),
                'tip': linija[1],
                'broj_soba': int(linija[2]),
                'broj_gostiju': int(linija[3]),
                'lokacija': int(linija[4]),
                'termini' : int(linija[5]),
                'domacin': linija[6],
                'cena': float(linija[7]),
                'status' : linija[8],
                'karakteristike' : karakteristike
            }
            apartmani[apartman['sifra']]=apartman
def pripremi_aktivne_za_prikaz(apartmani):
    za_prikaz=[]
    for apartman in apartmani.values():
        tip=apartman['tip']
        grad=lokacija.lokacije[apartman['lokacija']]['adresa']['mesto']
        cena=apartman['cena']
        sifra_apartmana=apartman['sifra']
        broj_soba=apartman['broj_soba']
        broj_osoba=apartman['broj_gostiju']
        sadrzaji=[]
        karakteristike_sifre=apartman['karakteristike']
        for sifra in karakteristike_sifre:
            sadrzaji.append(karakteristika.karakteristike[sifra]['naziv'])
        sadrzaji=",".join(sadrzaji)
        if apartman['status']=='aktivan':
            za_prikaz.append([sifra_apartmana,tip,grad,cena,broj_soba,broj_osoba,sadrzaji])
    return tabulate.tabulate(za_prikaz, headers=['Sifra','Tip','Grad','Cena','Broj soba','Broj gostiju','Sadrzaji'])

#priprema za prikaz-zasto?pa zato sto funkcija tabulate prima listu vrednosti, pa onda vrednosti iz
def pripremi_za_prikaz(apartmani):
    za_prikaz=[]
    for apartman in apartmani.values():
        tip=apartman['tip']
        grad=lokacija.lokacije[apartman['lokacija']]['adresa']['mesto']
        cena=apartman['cena']
        sifra_apartmana=apartman['sifra']
        broj_soba=apartman['broj_soba']
        broj_osoba=apartman['broj_gostiju']
        sadrzaji=[]
        karakteristike_sifre=apartman['karakteristike']
        for sifra in karakteristike_sifre:
            sadrzaji.append(karakteristika.karakteristike[sifra]['naziv'])
        sadrzaji=",".join(sadrzaji)
        za_prikaz.append([sifra_apartmana,tip,grad,cena,broj_soba,broj_osoba,sadrzaji])
    return tabulate.tabulate(za_prikaz, headers=['Sifra','Tip','Grad','Cena','Broj soba','Broj gostiju','Sadrzaji'])


def prikazi_apartmane(apartmani):
    print(pripremi_za_prikaz(apartmani))


def prikazi_aktivne_apartmane(apartmani):
    print(pripremi_aktivne_za_prikaz(apartmani))

#prilikom visekriterijumske pretrage, pravim recnik u koji dodajem trenutni rezultat pretrage, pa se dodaje sledeci rezultati pretrage
# presek rezultata koji zadovoljavaju nase kriterijume
def visekriterijumska_pretraga():
    print("              Dobrodosli u visekriterijumsku pretragu apartmana!")
    print("-------------------------------------------------------------------------------")
    print("Da biste pretrazili apartmane, molimo Vas odaberite jednu od ponudjenih opcija")
    trenutni_apartmani=apartmani.copy()
    opt=""
    while True:
        print("1. Dodaj kriterijum ")
        print("2. Zavrsi pretragu ")
        opt=input("----> ")
        if opt == "1":
            trenutni_apartmani=pretraga_apartmana(trenutni_apartmani)
        elif opt == "2":
            break
    prikazi_apartmane(trenutni_apartmani)


#pretraga apartmana, tip=saljemo kao parametar funkciji, u zavisnosti da li je 0 ili 1, pitacemo da li je == sa values ili ipak samo in values-grad
#kod tip 0-prikaz smestaja sa manjim brojem , tip 1-sa vecim brojem, tip 2-pretraga izmedju gornje i donje granice tj. min i max
#kljuc pretrage, pa kljuc cije vrednosti zelimo iz recnika
#vrednost pretrage=opcija koju je korisnik uneo po kojoj zeli da pretrazuje
def pretraga_apartmana(apartmani):
    print("")
    opt=""
    tip=0
    trazeni_apartmani={}
    print("         Dobrodosli u pretragu apartmana!")
    print("------------------------------------------------")
    print("Molimo Vas odaberite jednu od ponudjenih opcija:")
    while True:
        print("1. Pretraga po mestu")
        print("2. Pretraga po broju soba")
        print("3. Pretraga po broju osoba")
        print("4. Pretraga po ceni")
        print("5. Povratak na glavni meni")
        opt=input("----> ")
        if opt=='5':
            meni.pocetni_meni()
        if opt=="1":
            print("Odaberite opciju na koji nacin ce se vrsiti pretraga:")
            while True:
                print("1. Pretraga apartmana po prefisku(npr.Beo, Ni, Sub, itd.) ")
                print("2. Pretraga apartmana po punom nazivu ")
                print("------------------------------------------")
                o=input("----> ")
                if o=="1":
                    tip=0
                    break
                elif o=="2":
                    tip=1
                    break
                print("Uneli ste nepostojecu opciju!Molimo Vas pokusajte ponovo")
            while True:
                vrednost_pretrage=input("Unesite Vas odabir po kojem pretrazujete zeljeni apartman: ")
                if vrednost_pretrage.isalpha():
                    break
                print("Pogresan unos! Pokusajte ponovo!")
            kljuc_pretrage="mesto"
            trazeni_apartmani=nadji_apartmane(kljuc_pretrage,vrednost_pretrage,tip,apartmani)
            break
        elif opt=="2":
            param=None
            while True:
                print("Odaberite opciju na koji nacin ce se vrsiti pretraga:")
                print("1. Prikaz smestaja sa manjim brojem soba ")
                print("2. Prikaz smestaja sa vecim brojem soba ")
                print("3. Prikaz smestaja sa brojem soba koji se nalaze u intervalu izmedju gornje i donje granice ")
                print("---------------------------------------------------------------------------------------------")
                o=input("---> ")
                if o=="1":
                    param=read_int("Unesite broj soba:")
                    tip=0
                    break
                elif o=="2":
                    param=read_int("Unesite broj soba:")
                    tip=1
                    break
                elif o=="3":
                    donja_granica=read_int("Unesite najmanji zeljeni broj soba u smestaju:")
                    gornja_granica=read_int("Unesite najveci zeljeni broj soba u smestaju:")
                    param=[donja_granica,gornja_granica]
                    tip = 2
                    break
            vrednost_pretrage=param
            kljuc_pretrage="broj_soba"
            trazeni_apartmani=nadji_apartmane(kljuc_pretrage,vrednost_pretrage,tip,apartmani)
            break
        elif opt == "3":
            param = None
            while True:
                print("Odaberite opciju na koji nacin ce se vrsiti pretraga:")
                print("1. Prikaz smestaja koji imaju manji kapacitet od kriterijuma")
                print("2. Prikaz smestaja koji imaju veci kapacitet od kriterijuma")
                print("3. Prikaz smestaja ciji je kapacitet smestanja gostiju u intervalu izmedju gornje i donje granice")
                print("--------------------------------------------------------------------------------------------------")
                o = input("---> ")
                if o == "1":
                    param = read_int("Unesite broj gostiju:")
                    tip = 0
                    break
                elif o == "2":
                    param = read_int("Unesite broj gostiju:")
                    tip = 1
                    break
                elif o == "3":
                    donja_granica = read_int("Unesite minimalan broj gostiju koji smestaj mora da smesti:")
                    gornja_granica = read_int("Unesite maksimalan broj gostiju koji apartman mora da smesti:")
                    param = [donja_granica, gornja_granica]
                    tip = 2
                    break
            vrednost_pretrage = param
            kljuc_pretrage = "broj_gostiju"
            trazeni_apartmani = nadji_apartmane(kljuc_pretrage, vrednost_pretrage, tip,apartmani)
            break
        elif opt == "4":
            param = None
            while True:
                print("Odaberite opciju na koji nacin ce se vrsiti pretraga:")
                print("1. Prikaz smestaja koji su jeftiniji od kriterijuma")
                print("2. Prikaz smestaja koji su skuplji od kriterijuma")
                print("3. Prikaz smestaja cija cena ulazi u opseg izmedju dve granice (min i max cena smestaja)")
                print("--------------------------------------------------------------------------------------------------")
                o = input("---> ")
                if o == "1":
                    param = read_int("Unesite cenu spram koje pretrazujete smestaj:")
                    tip = 0
                    break
                elif o == "2":
                    param = read_int("Unesite cenu spram koje pretrazujete smestaj:")
                    tip = 1
                    break
                elif o == "3":
                    gornja_granica = read_int("Unesite maksimalnu cenu smestaja koja dolazi u obzir:")
                    donja_granica = read_int("Unesite minimalnu cenu smestaja koja dolazi u obzir:")
                    param = [donja_granica, gornja_granica]
                    tip = 2
                    break
            vrednost_pretrage = param
            kljuc_pretrage = "cena"
            trazeni_apartmani = nadji_apartmane(kljuc_pretrage, vrednost_pretrage, tip,apartmani)
            break



    return  trazeni_apartmani

#prikaz apartmana domacina, kada nadjemo da se trenutno logovani domacin poklapa sa domacinom u apartmanima
# vracamo njegove apartmane u jedan recnik trazeni
def nadji_apartmane_domacina(domacin):
    trazeni={}

    for apartman in apartmani.values():
        if apartman['domacin'] == domacin:
            trazeni[apartman['sifra']]=apartman
    return trazeni

#prvo se osiguramo da domacin moze da brise samo svoje apartmane
#nakon toga domacin unosi sifru apartmana, koja se potom izbacuje iz recnika
def brisanje_apartmana(domacin):
    trazeni=nadji_apartmane_domacina(domacin)
    prikazi_apartmane(trazeni)
    sifra=read_int("Unesite sifru apartmana za brisanje: ")
    obrisi_apartman(sifra)



def nadji_apartmane(kljuc_pretrage,vrednost_pretrage,tip,apartmani):
    trazeni_apartmani={}
    for kljuc in apartmani.keys():
        apartman=apartmani[kljuc]
        if kljuc_pretrage=='mesto':
            mesto=lokacija.lokacije[apartman['lokacija']]['adresa']['mesto']
            if tip==0:
                if vrednost_pretrage.lower() in mesto.lower():
                    trazeni_apartmani[kljuc]=apartman
            else:
                if vrednost_pretrage.lower()==mesto.lower():
                    trazeni_apartmani[kljuc] = apartman
        elif kljuc_pretrage=='broj_soba':
            broj_soba=apartman['broj_soba']
            if tip==0:
                if broj_soba<vrednost_pretrage:
                    trazeni_apartmani[kljuc] = apartman
            elif tip==1:
                if broj_soba>vrednost_pretrage:
                    trazeni_apartmani[kljuc] = apartman
            else:
                donja_granica=vrednost_pretrage[0]
                gornja_granica=vrednost_pretrage[1]
                if donja_granica <= broj_soba <= gornja_granica:
                    trazeni_apartmani[kljuc] = apartman
        elif kljuc_pretrage=='broj_gostiju':
            broj_gostiju=apartman['broj_gostiju']
            if tip==0:
                if broj_gostiju<vrednost_pretrage:
                    trazeni_apartmani[kljuc] = apartman
            elif tip==1:
                if broj_gostiju>vrednost_pretrage:
                    trazeni_apartmani[kljuc] = apartman
            else:
                donja_granica=vrednost_pretrage[0]
                gornja_granica=vrednost_pretrage[1]
                if donja_granica < broj_gostiju < gornja_granica:
                    trazeni_apartmani[kljuc] = apartman
        elif kljuc_pretrage=='cena':
            cena=apartman['cena']
            if tip==0:
                if cena<vrednost_pretrage:
                    trazeni_apartmani[kljuc] = apartman
            elif tip==1:
                if cena>vrednost_pretrage:
                    trazeni_apartmani[kljuc] = apartman
            else:
                donja_granica=vrednost_pretrage[0]
                gornja_granica=vrednost_pretrage[1]
                if donja_granica < cena < gornja_granica:
                    trazeni_apartmani[kljuc] = apartman
    return trazeni_apartmani

#pravimo listu gradova
def izdvoj_gradove():
    gradovi=[]
    for key in apartmani.keys():
        apartman=apartmani[key]
        mesto=lokacija.lokacije[apartman['lokacija']]['adresa']['mesto']
        if mesto not in gradovi:
            gradovi.append(mesto)
    return gradovi


#izdvajamo sve gradove koji se nalaze u listi, na pocetku inicajalizujemo pojavljivanje svakog na nula
#kako pronalazimo ime pojedinog grada u recniku, povecavamo counter za jedan
#sve te vrednosti se potom dodaju u recnik, gde sortiramo po redosledu od grada sa najvecim brojem pojavljivanja
# ka najmanjem broju pojavljivanja
def najpopularniji_gradovi():
    print("")
    print("Prikaz trenutno najpopularnijih gradova")
    print("----------------------------------------")
    gradovi=izdvoj_gradove()
    popularnost={}
    for grad in gradovi:
        popularnost[grad]=0
    for apartman in rezervacija.rezervacije.values():
        for apartman1 in apartmani.values():
            if apartman1['sifra']==apartman['sifra']:
                mesto = lokacija.lokacije[apartman1['lokacija']]['adresa']['mesto']
                #mesto=apartman1['lokacija']
                popularnost[mesto] += 1

    popularnost_sorted= {k: v for k, v in sorted(popularnost.items(), key=lambda item: item[1], reverse=True)}
    count = 0
    i=0
    for key in popularnost_sorted:
        i=i+1
        count+=1
        if count==10:
            return
        print(str(i) + "."+" "+key)


#popujemo element iz recnika, i zato sto u for petlji ne mozemo vrsiti brisanje, izbacuje error
# dodajemo sifru rezervacije, koju nalazimo preko sifre apartmana, u listu
# potom popujemo element iz liste, kako bisom obrisali i rezervaciju

def obrisi_apartman(sifra):
    if sifra not in apartmani.keys():
        print("Ne postoji apartman sa unetom sifrom!")
        return
    apartmani.pop(sifra)
    za_brisanje=[]
    for key in rezervacija.rezervacije.keys():
        if rezervacija.rezervacije[key]['apartman']==sifra:
            za_brisanje.append(key)

    for key in za_brisanje:
        rezervacija.rezervacije.pop(key)

#osiguramo se da domacin moze vrsiti samo izmene svog apartmana
#na mestima gde ne zelimo da vrsi slobodan unos, da ne bi pobrljavio vrednosti-zadajemo predefinisani
#sifru generisemo po vec objasnjenom principu
#dodajemo apartman u recnik
#prilikom dodavanje dodatne opreme proveravamo da li vec postoji
def izmeni_apartman(domacin):
    print("")
    print("                     IZMENA APARTMANA                      ")
    print("-----------------------------------------------------------")
    trazeni=nadji_apartmane_domacina(domacin)
    prikazi_apartmane(trazeni)
    sifra=read_int("Unesite sifru apartmana kod kojeg se vrsi izmena:")
    if sifra not in apartmani.keys():
        print("Uneli ste nepostojecu sifru!")
        return
    while True:
        opt=""
        print("1. Izmena tipa smestaja")
        print("2. Izmena broja soba apartmana")
        print("3. Izmena broja gostiju koja moze stati u apartman")
        print("4. Izmena cene apartmana")
        print("5. Izmena statusa apartmana")
        print("6. Izmena liste sadrzaja apartmana")
        print("7. Zavrsi izmenu")
        print("-----------------------------------------------------")
        opt=input("Odaberite i unesite Vasu opciju: ")
        if opt=="1":
            tip=""
            while True:
                print("Odaberite tip smestaja:")
                print("1. Ceo apartman")
                print("2. Soba")
                print("------------------------")
                o=input("--->: ")
                if o=="1":
                    tip="ceo apartman"
                    break
                elif o == "2":
                    tip = "soba"
                    break
            apartmani[sifra]['tip']=tip
        elif opt == "2":
            broj_soba=read_int("Unesite broj soba: ")
            apartmani[sifra]['broj_soba']=broj_soba
        elif opt == "3":
            broj_gostiju=read_int("Unesite broj gostiju: ")
            apartmani[sifra]['broj_gostiju']=broj_gostiju
        elif opt == "4":
            cena=read_float("Unesite cenu: ")
            apartmani[sifra]['cena']=cena
        elif opt == "5":
            status=""
            while True:
                print("Odaberite jednu od ponudjenih opcija:")
                print("1. Aktivan")
                print("2. Neaktivan")
                print("--------------------------------------")
                o=input("--->")
                if o == "1":
                    status="aktivan"
                    break
                elif o == "2":
                    status = "neaktivan"
                    break
            apartmani[sifra]['status']=status
        elif opt == "6":
            kk = []
            while True:
                print("Da li zelite da nastavite da nastavite sa dodavanjem dodatne opreme?")
                print("1. Nastavi sa doodavanjem dodatne opremu ")
                print("2. Zavrsi sa dodavanjem dodatne opreme ")
                print("-------------------------------------------")
                oo = input("---> ")
                if oo == "2":
                    break
                elif oo == "1":
                    karakteristika.prikazi_dodatnu_opremu()
                    ss = read_str("Unesite sifru opreme: ")
                    if ss not in kk:
                        if ss in karakteristika.karakteristike.keys():
                            kk.append(ss)
            apartmani[sifra]['karakteristike'] = kk
        elif opt == "7":
            break


def generisi_sifru_apartman():
    if len(apartmani)==0:
        return 1
    sifre=list(apartmani.keys())
    sifre.sort(reverse=True)
    return sifre[0]+1

#dodavanje apartmana, domacin i sifra-automatski
def dodaj_apartman(domacin):
    print("")
    print("                    DODAVANJE APARTMANA                           ")
    print("-------------------------------------------------------------------")
    print("    ZA IZLAZAK IZ DODAVANJA APARTMANA U PRVOM UNOSU UNESITE 'X'    ")
    tip=""
    opt=""
    sifra_apartmana=generisi_sifru_apartman()
    while True:
        print("Za odabir tipa apartmana unesite jednu od ponudjenih opcija")
        print("1. Tip smestaja-soba")
        print("2. Tip smestaja- ceo apartman")
        opt=input("--->")
        if opt=="1":
            tip="soba"
            break
        elif opt=="2":
            tip="ceo apartman"
            break
    broj_soba=read_int("Unesite broj soba: ")
    broj_gostiju=read_int("Unesite broj gostiju: ")
    cena=read_float("Unesite cenu nocenja: ")
    sirina=read_float("Unesite geografsku sirinu: ")
    visina=read_float("Unesite geografsku visinu: ")
    ulica=read_str("Unesite ulicu: ")
    mesto=read_str("Unesite mesto: ")
    postanski_broj=read_str("Unesite postanski broj:")
    sifra_lokacije=lokacija.generisi_sifru()
    adresa={
        'ulica' : ulica,
        'mesto' : mesto,
        'postanski_broj' : postanski_broj
    }

    lok={
        'sifra' : sifra_lokacije,
        'geografska_sirina' : sirina,
        'geografska_visina' : visina,
        'adresa' : adresa
    }

    termini=[]
    while True:
        opt=""
        print("1. Dodajte termin")
        print("2. Zavrsite dodavanje termina")
        opt=input("Unesite opciju: ")
        if opt == "2":
            break
        elif opt=="1":
            termini.append(ucitaj_termin())

    k=[]
    while True:
        print("1. Dodaj dodatnu opremu ")
        print("2. Zavrsi dodavanje opreme ")
        opt=input("Unesite opciju: ")
        if opt=="2":
            break
        elif opt == "1":
            karakteristika.prikazi_dodatnu_opremu()
            sifra=read_str("Unesite sifru opreme: ")
            if sifra not in k:
                if sifra in karakteristika.karakteristike.keys():
                    k.append(sifra)
    status="neaktivan"

    lokacija.lokacije[sifra_lokacije]=lok
    sifra_termina=termin.generisi_sifru_termin()

    term={
        'sifra' : sifra_termina,
        'apartman' : sifra_apartmana,
        'datumi' : termini

    }
    termin.termini[sifra_termina]=term
    apartman={
        'sifra' : sifra_apartmana,
        'tip' : tip,
        'broj_soba' : broj_soba,
        'broj_gostiju' : broj_gostiju,
        'lokacija' : sifra_lokacije,
        'termini' : sifra_termina,
        'domacin' : domacin,
        'cena' : cena,
        'karakteristike' : k,
        'status' : status
    }

    apartmani[sifra_apartmana]=apartman
    print("Cestitamo uspesno ste dodali apartman!")



def ucitaj_termin():
    print("")
    while True:
        datum_start=read_date("Unesite pocetak zeljenog termina:")
        datum_end=read_date("Unesite kraj zeljenog termina:")
        if datum_start>=datum_end:
            print("Greska! Kraj termina, mora biti nakon pocetka termina!")
        else:
            return [datum_start,datum_end]