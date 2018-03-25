# Real Time Decisioning Model

# Install
## Install NiFi
A <https://nifi.apache.org/> lapon a Download alól le lehet tölteni.
Tipikusan <https://www.apache.org/dyn/closer.lua?path=/nifi/1.5.0/nifi-1.5.0-bin.zip> fájl kell. Ki kell csomagolni.

Én átkonfiguráltam, hogy a NiFi a 9090 porton fusson, mert ez egyezik a HortonWorks setuppal, és már megszoktam `vim /var/local/nifi/nifi-1.5.0/conf/nifi.properties`:
```
nifi.web.http.port=9090
```

Indítás:
``` sh
cd /var/local/nifi/nifi-1.5.0/bin
./nifi.sh start

```
Windows esetén <https://nifi.apache.org/docs/nifi-docs/html/getting-started.html#for-windows-users>:

Kis idő elteltével a böngészőben rá lehet lépni: <http://localhost:9090/nifi>.


``` sh
cd c:\NiFi\bin
run-nifi.bat
```

## Install MySQL
A <https://dev.mysql.com/downloads/mysql/> lapról ki kell választani, Windows, ha jól látom, felrakja magát.

### MySQL teszt adatbázis
Én ennek alapján csináltam: <https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql>.

Be kell lépni a shellbe: `mysql -p -u root ` , kéri a jelszót, amit install alatt beállítottál.

Adatbázis létrehozása:
``` sh
CREATE USER 'rtdm'@'localhost' IDENTIFIED BY 'rtdm123Kecske';
CREATE DATABASE rtdm CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON rtdm.* TO rtdm@localhost;
FLUSH PRIVILEGES;
```

Nyilván megadhatsz más jelszót, usert, ízlés szerint.

## Install Python
A <https://www.python.org/downloads/windows/> lapról érdemes.

## Alternatíva: Conda
Az Anaconda egy Data Science keretrendszer. Érdemes lehet felrakni.
Bele van csomagolva egy csomó okosság, pl Python, Spyder.
Innen érdemes: <https://conda.io/docs/user-guide/install/windows.html>


# Teszt adat generálás
Python kell hozzá.

A python/test_dta_gen.py fájlt kell Python alatt futtatni.
Kell hozzá pár import, azokat fel kell rakni:
``` sh
pip install pandas numpy mysql-python
# vagy Anacondánál
conda install fentebbiek
```
A def `write_static_db(cust, card):` függvényben be kell állítani a JDBC URL-t, arra a teszt adatbázisra, amelyet létrehoztunk:

``` python
db_connection = 'mysql+mysqlconnector://rtdm:rtdm123Kecske@localhost:3306/rtdm'
```

Ezek után lehet futtatni:
``` sh
python -i python\test_dta_gen.py

```
## Teszt adat eredmények
Jó eséllyel legyárt 3 CSV fájlt:

  * customer.csv - Ügyfeleink
  * cards.csv - Bank kártyák az ügyfelekhez
  * transactions.csv - Bank kártyához tartozó tranzakciók
  * merchant.csv - Kereskedő adatok

Valamint MySQL alatt lesznek adatok `mysql -p -u rtdm`:
(Gondolom, Windows alatt is van valami konzol. Ha nagyon nincs, akor MySQLWorkbench programot installáld.)

``` {sql}
use rtdm
select * from customer limit 10;
select * from bank_card limit 10;
select * from merchant limit 10;
```

# NiFi modell

## NiFi, CSV_Ert_Mux.xml 

Ez felolvasgatja a fájlt, és rekordokra vágja, első működő csodám!

### Előkészületek

Kell két alkönyvtár, ahova a nifi dolgozik. 
 * /opt/u01/gwork/rtdm/nifi/data - innen veszi a fájlt, amit feldolgoz
 * /opt/u01/gwork/rtdm/nifi/output - ide rakja amit kiirkál

Indítás előtt érdemes kidobni az output tartalmát:
``` sh
rm -f /opt/u01/gwork/rtdm/nifi/output/*
```

És kell adni pár rekordot neki, mondjuk az első 10 tranzakciót:
``` sh
cat /opt/u01/gwork/rtdm/python/transactions.csv | head > /opt/u01/gwork/rtdm/nifi/data/transactions.csv
```

### NiFi alatt, model betöltés

Fel kell tölteni a templatet. "Operate" részben első sor, utolsó ikon "Upload Template". Töltsd fel a nifi/CSV_Ert_Mux.xml fájlt.

Ettől a Teplates alatt megjelenik: Jobb felső sarok, három csik, jobb gomb, Templates, SCV_Ert_Mux.

Modell behúzása. Húzz rá egy 'Template' elemt a lapra, Felső ikonsor, utolsó előti "Template" ikon. Válaszd ki a SCV_Ert_Mux templatet.

Lett elvileg egy szép CsvRead ProcessGroup. Öröm.


### Nifi model editálás

CsvRead ProcessGroupon duplakatt, ezáltal belépsz a groupba, bal alsó sarok mutatja: NiFi Flow >> CsvRead

Editálandó Processek, duplakatt processen:
  * GetFile, Property, Input directory, amit felvettél az előzőekben.
  * PutFile, Property, Directory, mint előbb, csak az output

Nekem kellett még egy Controller Services indítás is:

  * CSV Read alatt vagyunk
  * Operate ablak, első ikonm (fogaskerék), CONROLLER SERVICES fül
  * Kis villámocska ikonnal futtani kell mindhárom servicet
  * (Először AvroSchema, másik kettő tőle függ.)
### NiFi futtatása

Előtte kell egy adag teszt fájl, lásd "Előkészületek".

  * Üres helyen katt. 
  * Operate Stop gomb (biztos, ami biztos)
  * Operate Start gomb

## NiFi, SimulateBankCard.xml

Arra szolgál, hogy kártyás tranzakciókat szimuláljunk, és hozzá rakjuk a banki adatokat.
Most, hogy gndolkodom rajta, a fájl feldolgozást és flow controlt ki  kellene venni külön modulba, ha egyszer is akarunk HTTP bementetet.
No majd egyszer.

### NiFi

SimulateBankCard.xml fájl felvenni template ként.
Lásd előző részben.
Ugyanazokat a dobozokat kell editálni, GetFile, PutFile.
Kell hozzá a MySQL teszt adat is, lásd teszt adatok rész.

Magában kiirkálja a flow fájlokat. Output portját kötni kell valami értelmeshez.

### ExecuteSQL MySQL beállítás
  * NiFi FLow >> SimualteBankCardTransactions
  * ExecuteSQL process
  * Properties, 'Database Connection Pooling Service', kis nyilacska a végén
  * Ez átdob a COntroller Services' lapra, ott DBCPConnectionPool, fogaskerék
  * Ki kell tölteni az alábbi Propertyket
    * Database Connection URL: jdbc:mysql://localhost:3306/rtdm (Win alatt is lyesmi)
	* Database Driver Class Name: com.mysql.jdbc.Driver
	* Database Driver Location: file:///usr/share/java/mysql.jar (ahol van a MySQL Jar fájl, MySQL install során elvileg lett ilyen fájl)
	* Database User: MySQL részből
	* Password: mint előző
