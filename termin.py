from datetime import datetime

termini={}
import tabulate


#ucitavamo termine, pravimo listu datuma
#na nultoj poziciji nalazi pocetak nekog termina, a na prvoj poziciji se na nalazi kraj nekog termina
#dodajemo sifru termina, sifru apartmana i listu datuma u recnik termina
def ucitaj_termine():
    with open("./database/termini.txt", "r") as file:
        linije = file.readlines()
        for linija in linije:
            linija = linija.strip().split("|")
            datumi_str=linija[2].split(",")
            datumi=[]
            for datum_str in datumi_str:
                temp=datum_str.split("-")
                datum_pocetak=datetime.strptime(temp[0],'%d/%m/%Y')
                datum_kraj = datetime.strptime(temp[1], '%d/%m/%Y')
                datumi.append([datum_pocetak,datum_kraj])
            termin = {
                'sifra' : int(linija[0]),
                'apartman' : int(linija[1]),
                'datumi' : datumi
            }
            termini[termin['sifra']]=termin

#sve izmene unete vezane za termine iz recnika unosimo u fajl
#datum parsiramo kao string, u predjasnje zadatom formatu, izmedju pocetka i kraja termina se nalazi -
#izmedju dva termina se nalazi ",", koristimo funkciju join koja spaja bilo koja dva stringa
def sacuvaj_termine():
    with open("./database/termini.txt", "w") as file:
        for termin in termini.values():
            datumi = []
            sifra=str(termin['sifra'])
            apartman=str(termin['apartman'])
            for datum in termin['datumi']:
                datum_start=datum[0]
                datum_end=datum[1]
                datum_start_str=datum_start.strftime('%d/%m/%Y')
                datum_end_str =datum_end.strftime('%d/%m/%Y')
                datumi.append(datum_start_str+"-"+datum_end_str)
            dates=",".join(datumi)
            linija=sifra+"|"+apartman+"|"+dates+"\n"
            file.write(linija)

#lista datuma, gde prvi predstavlja pocetni datum termina, a drugi datum predstavlja krajnji datum termina
#prikazujemo datume termina u tabeli kao pocetni i krajnji datumi
def prikazi_termine(termin):
    datumi=termin['datumi']
    datumi_str=[]
    for datum in datumi:
        datum_start=datum[0].strftime('%d/%m/%Y')
        datum_end=datum[1].strftime('%d/%m/%Y')
        datumi_str.append([datum_start,datum_end])
    print(tabulate.tabulate(datumi_str, headers=['Pocetak', 'Kraj']))


#proveravamo da li je datum koji je korisnik uneo prilikom iskazane zelje za rezervisanjem apartmana upada u opseg
#dok god imamo termina, pocetni datum termina nam se nalazi na nultoj poziciji, a krajnji datum termina na prvoj
# proveravamo da li nam je uneti datum izmedju krajnjeg i pocetnog datuma termina, ukoliko se nalazi izmedju pocetnog i krajnjeg datuma nekog termina, vrati nam taj termin
#u suprtonom vraca -1 i na taj nacin znamo da ne postoji termin koji zadovoljava nase kriterijume
def nadji_interval_za_datum(intervali,datum):
    for i in range(len(intervali)):
        date_start=intervali[i][0]
        date_end=intervali[i][1]
        if date_start <= datum < date_end:
            return i
    return -1

#isti princip za generisanje sifre termina, pitamo da li je len=0, ako nema termina, prvi ce pocinjati sa sifrom 1
#ako ima sortiramo listu da pocinje od najmaneg ka najvecm, tj. obrnemo redosled i sledeca generisana sifra je uvek veca za jedan od poslednje
def generisi_sifru_termin():
    if len(termini)==0:
        return 1
    sifre=list(termini.keys())
    sifre.sort(reverse=True)
    return  sifre[0]+1