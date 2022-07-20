lokacije={}
#splitujenp
def ucitaj_lokacije():
    with open("./database/lokacije.txt", "r") as file:
        linije = file.readlines()
        for linija in linije:
            linija = linija.strip().split("|")
            adresa_parts=linija[3].split(",")
            adresa={
                'ulica' : adresa_parts[0],
                'mesto' : adresa_parts[1],
                'postanski_broj' : adresa_parts[2]
            }
            recnik = {
                'sifra': int(linija[0]),
                'geografska_sirina': float(linija[1]),
                'geografska_visina': float(linija[2]),
                'adresa' : adresa
            }
            lokacije[recnik['sifra']]=recnik

def sacuvaj_lokacije():
    with open("./database/lokacije.txt", "w") as file:
        for lokacija in lokacije.values():
            sifra = str(lokacija['sifra'])
            sirina = str(lokacija['geografska_sirina'])
            visina = str(lokacija['geografska_visina'])
            ulica = lokacija['adresa']['ulica']
            mesto = lokacija['adresa']['mesto']
            postanski_broj = lokacija['adresa']['postanski_broj']
            linija=sifra+"|"+sirina+"|"+visina+"|"+ulica+","+mesto+","+postanski_broj+"\n"
            file.write(linija)


def generisi_sifru():
    if len(lokacije)==0:
        return 1
    sifre=list(lokacije.keys())
    sifre.sort(reverse=True)
    return sifre[0]+1