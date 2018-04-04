# Real Time Decisioning Model

# HDF
Be kell húzni Virtualbox alá a HDF imaget.
Nem árt elnevezni a gépet sandbox-hdf.hortonworks.com névre (localhost),
hogy jól érezze magát a sok installált SW.

## Kikapcsolás / bekapcsolás
Nem szabad leállítani rendesen a gépet.
Nekem többször volt, hogy nem indult el.

Helyette: 

A better way to go with the Sandbox VMs is to use the 
"save the machine state" rather than power off from the VirtualBox 
shutdown options. This acts more like a suspend/resume and will 
preserve the Docker container.

## Elérés ssh-val

A virtuális gépen fut egy host, azon egy docker guest.

Host elérése:
``` sh
ssh root@sandbox-hdf.hortonworks.com -p 2122
```

Tényleges HDF gép elérése:
``` sh
ssh root@sandbox-hdf.hortonworks.com -p 2222
```

(pass: hadoop)

Érdemes publikus kulcsot felmásolni:
``` sh
ssh-copy-id  root@sandbox-hdf.hortonworks.com -p 2122
```
## Idő beállítás

Ébresztés után elmászik a host órája. Állítani kell:
``` sh
ntpdate time.kfki.hu
```
# Teszt adat generálás

## Git repo

Kihoztam a git repot a HDF gépen a /var/local/rtdm alá.

Időről időre lehet mondani szinkronizálást:

``` sh
cd /var/local/rtdm
git pull
```
## Teszt adat paraméterek
/var/local/rtdm/python/param_dicts.py fájlban vannak.

Nagyrészt hasraütésre vettem fel a kategóriákat.

ToDo : nézzük át, reálisak-e.

## Teszt adat generálás

Ezek után lehet futtatni:
``` sh
cd /var/local/rtdm/python
python -i python\test_dta_gen.py

```
## Teszt adat eredmények
Jó eséllyel legyárt egy halom CSV fájlt:

  * customer_model.csv - Ügyfeleink, modellezéshez
  * customer_simul.csv - Ügyfelek majd a NiFI szimulációhoz
  * cards.csv - Bank kártyák az ügyfelekhez
  * transaction_model.csv / transaction_model.csv - Bank kártyához tartozó tranzakciók
  * merchant.csv - Kereskedő adatok

Valamint MySQL alatt lesznek adatok `mysql -p -u rtdm`:

``` {sql}
use rtdm
select * from customer limit 10;
select * from bank_card limit 10;
select * from merchant limit 10;
```

# NiFi modell

## NiFi
Ha jól van elnevezve a gép, akkor:

http://sandbox-hdf.hortonworks.com:9090/nifi/

Én Benn hagytam a modellt.

### Előkészületek

Kell két alkönyvtár, ahova a nifi dolgozik. 
 * /var/local/rtdm/nifi/data - innen veszi a fájlt, amit feldolgoz
 * /var/local/rtdm/nifi/output - ide rakja amit kiirkál

Indítás előtt érdemes kidobni az output tartalmát:
``` sh
rm -f /var/local/rtdm/nifi/output/*
```

És kell adni minta fájlt neki:
``` sh
cp /var/local/rtdm/nifi/work/transaction_simul.csv /var/local/rtdm/nifi/data/transactions.csv
```

### NiFi alatt, model betöltés
Most épp be van töltve, de így hagytam a leírást.

Fel kell tölteni a templatet. "Operate" részben első sor, utolsó ikon "Upload Template". Töltsd fel a nifi/CSV_Ert_Mux.xml fájlt.

Ettől a Teplates alatt megjelenik: Jobb felső sarok, három csik, jobb gomb, Templates, SCV_Ert_Mux.

Modell behúzása. Húzz rá egy 'Template' elemt a lapra, Felső ikonsor, utolsó előti "Template" ikon. Válaszd ki a SCV_Ert_Mux templatet.

Lett elvileg egy szép CsvRead ProcessGroup. Öröm.


### Nifi model editálás

Ezeket is végigcsináltam, már nem kell.

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

## NiFi Python ML model kiértékelés

A ProcessGroup-ba kell belépni.
Lényeg a ExecuteStreamCommand processor.

### Előkészületek

A betanított, elmentett modelt és a hozzá tartozó Python wrappert át kell másolni a nifi/model alkönyvtárba:
```{Python}
cp python/ex_str_proc_demo.py nifi/model/
cp python/model_estimator_test.pkl nifi/model/
```
### 

# Model építés

A /var/local/rtdm/python/model_simul.csv fájl adataira kell modellt építeni.

``` sh
head -n 2 /var/local/rtdm/python/model_simul.csv 
,TransactionTrend,Account,FamilyMembers,Gender,long,Name,AvgMonthlySpending,merchantId,CreditScore,merchantType,Age,lat,amount,BalanceAmount,PreviousDaySpending,accountType,CreditLimit,accountNumber,transactionId,IncomeCategory,name,NrOfDebCards,Tel,CrmSegment,ShortTermCredit,NrOfCredCards,feature_1
1315,Inact,230010996,1,F,19.0488859,Bálint Márton,394455,1082,S,utazás,70,47.49721,69069,731653,254158,MASTERCARD,1120000,2871 7229 4142 6115,5382377001,M,Neckermann Vörö,3,3680472249,Pension,Y,1,0.0
```

A feature_1 a cél változó. 0, ha nincs limit emelés, 1, ha van.

A normál ügyfelek tulajdonságai:
```{python}
	cred_score = rand_list(crdtscore_list[:3])
        nr_of_cred_card = random.randint(0, 1)
        bal_amount = random.randint(int((avg_mon_spen / 3) *
                                    (1.1 + random.random())),
                                    768576)
```

Azaz a credit score rosszabb, kevesebb a hitelkártyája, de nagyobb az egyenlege, mint a havi /3.

A limit emeléses ügyfelek tulajdonságai:
```{python}
        # Set values for Model Customer, model1
        # - Hitelkártya fõkártya db >= 1
        # - Hitel előminősített <> 0
        # - egyenleg összeg (decimal), < Átlagos havi költés /3
        cred_score = rand_list(crdtscore_list[3:])
        nr_of_cred_card = random.randint(1, 3)
        bal_amount = random.randint(314, int(avg_mon_spen / 3))
        cc = 1
```

Azaz a Crdit score nagyobb, kártyaszám nagyobb, egyenlege kisebb.

## Teszt model - model elmentése
A 'python/clf_test.py' fájlban egy preimitív kNN model található.
Helyben generált teszt adatokon tanul, és prediktál.

Az a szép benne, hogy a modelt tanulás után fájlba mentjük.

A 'python/ex_str_proc_demo.py' fájlban van az elmentett modelt felhasználó NiFi ExecuteStreamCommand processor által hívható kiértékelő.

A modelt majd le kell futtatni a Hortonworks Sandboxban is, ott 2.7 Python van, és a Python 3 által elmentett modelt nem akarja olvasni.

Megoldás lehet a `, protocol=2)` használata. Nem ellenőriztem.
[StacOverflow](https://stackoverflow.com/questions/25843698/valueerror-unsupported-pickle-protocol-3-python2-pickle-can-not-load-the-file)
