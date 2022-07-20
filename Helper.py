import  datetime
#validacije-za datum splitovana prvenstveno po /, onda provera da li je datum izmedju 1 i 31, a mesec izmedju 1 i 12

def read_int(message):
    while True:
        num=input(message)
        if num.isnumeric():
            return int(num)

def read_float(message):
    while True:
        num=input(message)
        p=num
        if num.replace('.','',1).isdigit():
            return float(p)


def read_str(message):
    while True:
        s=input(message)
        if len(s)!=0:
            return s


def read_date(message):
    while True:
        datum = input(message)
        datum_parts = datum.split("/")
        if len(datum_parts) != 3:
            print("datum mora biti u formtu dd/mm/yyyy")
        else:
            dan = datum_parts[0]
            mesec = datum_parts[1]
            godina = datum_parts[2]
            if dan.isnumeric() and mesec.isnumeric() and godina.isnumeric():
                dan = int(dan)
                mesec = int(mesec)
                godina = int(godina)
                if dan < 1 or dan > 31:
                    print("Greska! Dan moze biti u opsegu samo izmedju 1 i 31!!")
                elif mesec < 1 or mesec > 12:
                    print("Greska! Mesec moze biti broj u opsegu izmedju 1 i 12!")
                else:
                    break
            else:
                print("Dan, mesec i godina moraju biti brojevi!")
    datum=datetime.datetime.strptime(datum,'%d/%m/%Y')
    return datum
