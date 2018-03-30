#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 10:41:30 2018

@author: muszi

Create test Data for Real Time Decisioning Model
"""

import random
import pandas as pd
import numpy as np
import datetime as dt
from param_dicts import merchant_category, account_types, merchants, crm_segment, gend_list, yn_list, trchg_list, incmcat_list, crdtscore_list

random.seed(8128)


def rand_list(ilist):
    """
    Returns a random element from the list ilist
    """
    return ilist[random.randint(0, len(ilist)-1)]


def generate_merchants_df():
    """
    Returns a DataFrame containing the merchants dict
    """
    mlist = list()
    for key, values in merchants.items():
        for merch in values:
            merch['category'] = key
            mlist.append(merch)
    merch = pd.DataFrame(mlist)
    merch.set_index('id', inplace=True)
    merch.to_csv("merchant.csv")
    return merch


def generate_random_name(gender):
    first_name_wmn = ['Hanna', 'Anna', 'Jázmin', 'Nóra', 'Boglárka', 'Zsófia', 'Lili', 'Réka', 'Dóra', 'Luca', 'Viktória', 'Emma', 'Vivien', 'Laura', 'Eszter', 'Fanni', 'Petra', 'Lilla', 'Csenge', 'Noémi', 'Sára', 'Dorina', 'Gréta', 'Zoé', 'Dorka', 'Rebeka', 'Bianka', 'Flóra', 'Léna', 'Panna', 'Lara', 'Maja', 'Kamilla', 'Szonja', 'Fruzsina', 'Virág', 'Blanka', 'Kinga', 'Ramóna', 'Kitti', 'Tímea', 'Janka', 'Kata', 'Júlia', 'Dorottya', 'Emese', 'Vanessza', 'Izabella', 'Mira', 'Nikolett', 'Liza', 'Veronika', 'Tamara', 'Alíz', 'Emília', 'Lilien', 'Kira', 'Adrienn', 'Amanda', 'Borbála', 'Leila', 'Kincső', 'Adél', 'Zselyke', 'Diána', 'Natália', 'Melissza', 'Abigél']
    first_name_men = ['Bence', 'Máté', 'Levente', 'Ádám', 'Dávid', 'Balázs', 'Dominik', 'Péter', 'Gergő', 'Milán', 'Tamás', 'Zsombor', 'Dániel', 'Bálint', 'Botond', 'Kristóf', 'Zalán', 'Áron', 'László', 'Márk', 'Attila', 'Zoltán', 'Noel', 'Marcell', 'András', 'Benedek', 'Ákos', 'Gábor', 'István', 'Olivér', 'Márton', 'Patrik', 'Roland', 'Zsolt', 'Kevin', 'János', 'Martin', 'Csaba', 'Hunor', 'Richárd', 'Benett', 'Gergely', 'József', 'Norbert', 'Nimród', 'Róbert', 'Sándor', 'Alex', 'Zétény', 'Ferenc', 'Erik', 'Viktor', 'Mátyás', 'Ábel', 'Kornél', 'Vince', 'Mihály', 'Nándor', 'Csongor', 'Tibor', 'Rikárdó', 'Ármin', 'Csanád', 'Adrián', 'Miklós', 'Imre', 'György', 'Gyula', 'Vilmos', 'Soma', 'Kende']
    last_name = ['Nagy', 'Kovács', 'Tóth', 'Szabó', 'Horváth', 'Varga', 'Kiss', 'Molnár', 'Németh', 'Farkas', 'Balogh', 'Papp', 'Takács', 'Juhász', 'Lakatos', 'Mészáros', 'Oláh', 'Simon', 'Rácz', 'Fekete', 'Szilágyi', 'Török', 'Fehér', 'Balázs', 'Gál', 'Kis', 'Szűcs', 'Kocsis', 'Orsós', 'Pintér', 'Fodor', 'Szalai', 'Sipos', 'Magyar', 'Lukács', 'Gulyás', 'Biró', 'Király', 'László', 'Katona', 'Jakab', 'Bogdán', 'Balog', 'Sándor', 'Boros', 'Fazekas', 'Kelemen', 'Váradi', 'Antal', 'Somogyi', 'Orosz', 'Fülöp', 'Veres', 'Vincze', 'Hegedűs', 'Budai', 'Deák', 'Pap', 'Bálint', 'Pál', 'Illés', 'Vass', 'Szőke', 'Vörös', 'Bognár', 'Fábián', 'Lengyel', 'Bodnár', 'Szücs', 'Hajdu', 'Halász', 'Jónás', 'Máté', 'Székely', 'Kozma', 'Gáspár', 'Pásztor', 'Bakos', 'Dudás', 'Major', 'Orbán', 'Hegedüs', 'Virág', 'Barna', 'Novák', 'Soós', 'Tamás', 'Nemes', 'Pataki', 'Balla', 'Faragó', 'Kerekes', 'Borbély', 'Barta', 'Péter', 'Szekeres', 'Csonka', 'Mezei', 'Márton', 'Sárközi']
    return (rand_list(last_name) +
            " " +
            (rand_list(first_name_wmn)
             if gender == 'N' else
             rand_list(first_name_men)))


def generate_random_cardnr():
    return "{:04d} {:04d} {:04d} {:04d}".format(random.randint(0, 9999),
                                                random.randint(0, 9999),
                                                random.randint(0, 9999),
                                                random.randint(0, 9999))


class AccNr:
    def __init__(self, startNr):
        self.nr = startNr


    def getNr(self):
        self.nr += 1
        return self.nr


accNr = AccNr(230010000)
transNr = AccNr(5382367345)
cust_columns = ['Gender', 'Name', 'Age', 'Tel', 'BalanceAmount',
                'CrmSegment', 'ShortTermCredit', 'FamilyMembers',
                'TransactionTrend', 'IncomeCategory', 'NrOfDebCards',
                'NrOfCredCards', 'CreditScore', 'AvgMonthlySpending',
                'CreditLimit', 'PreviousDaySpending']


def create_one_cust(cust_type):
    """
    Creates test Customer
    cust_type: normal / model1
    gen_phase: True = model phase, target variables added /False: transaction
    Fields of Cust record:
    Account: account number
    Gender: N / F
    Name: Full name
    Age: in years
    Tel: 3680123456
    BalanceAmount: egyenleg összeg (decimal)
    CrmSegment: crm_segment List - aCRM szegmens
       (Aktív folyószámlahiteles, Tranzaktáló hosszúhiteles)
    ShortTermCredit : Y/N - 2 hónapon belül lejáró hitel (Y/N)
    FamilyMembers: - Háztartás mérete (short int)
    TransactionTrend: Dec,DecDec,Stab,Inc,IncInc,Inact,) - Tranzakciók
      változása (Csökkenés, Jelentõs csökkenés, Stabil, Inaktív
         , Jelentõs növekedés)
    IncomeCategory: XS,S,M,L,XL,XXL - Bevétel kategória (0-20M, 21-50M,
       51-300M,..)
    NrOfDebCards: - Betéti kártya db (decimal)
    NrOfCredCards: - Hitelkártya fõkártya db (decimal)
    CreditScore: - NO,S,M,L,XL, Hitel előminősített (0, 200-ig, 500-ig, 1m, 5m)
    AvgMonthlySpending: - Átlagos havi költés
    CreditLimit: - Bankkártya limit, decimal
    PreviousDaySpending: - Előző napi kártyás vásárlás
    CandidateTargetCreditIncrease: Model cél változó, majd tranzakciós
    adatokba generálunk hitel kártya emelést
    """
    # Choose random gender
    gender = rand_list(gend_list)
    # Based on cust_type generate different random data
    bal_amount, nr_of_cred_card, cred_score, avg_mon_spen = 0, 0, 'NO', 0
    cc = 0
    avg_mon_spen = random.randint(15418, 1024512)
    if cust_type == 'normal':
        # Set values for normal customer
        cred_score = rand_list(crdtscore_list[:3])
        nr_of_cred_card = random.randint(0, 1)
        bal_amount = random.randint(int((avg_mon_spen / 3) *
                                    (1.1 + random.random())),
                                    768576)
    else:
        # Set values for Model Customer, model1
        # - Hitelkártya fõkártya db >= 1
        # - Hitel előminősített <> 0
        # - egyenleg összeg (decimal), < Átlagos havi költés /3
        cred_score = rand_list(crdtscore_list[3:])
        nr_of_cred_card = random.randint(1, 3)
        bal_amount = random.randint(314, int(avg_mon_spen / 3))
        cc = 1
    # Create Cust dict
    cust_dic = {'Account': "{}".format(accNr.getNr()),
                'Gender': gender,
                'Name': generate_random_name(gender),
                'Age': random.randint(18, 77),
                'Tel': "3680{}".format(random.randint(100000, 887887)),
                'BalanceAmount': bal_amount,
                'CrmSegment': rand_list(crm_segment),
                'ShortTermCredit': rand_list(yn_list),
                'FamilyMembers': random.randint(1, 5),
                'TransactionTrend': rand_list(trchg_list),
                'IncomeCategory': rand_list(incmcat_list),
                'NrOfDebCards': random.randint(1, 3),
                'NrOfCredCards': nr_of_cred_card,
                'CreditScore': cred_score,
                'AvgMonthlySpending': avg_mon_spen,
                'CreditLimit': random.randint(10, 120) * 10000,
                'PreviousDaySpending': random.randint(13000, 320000),
                'CandidateTargetCreditIncrease': cc}
    return cust_dic


#print(create_one_cust('normal', True))


def create_test_customers(nr_of_cust, cust_type):
    """
    Random ügyfeleket vesz fel.

    cust_type: normal / model1
    gen_phase: True = model phase, target variables added / False: transaction

    Ebből DataFrame-t generál, és kiírja customer.csv néven.
    """
    cust_list = list()
    for i in range(nr_of_cust):
        cust_list.append(create_one_cust(cust_type))
    cust = pd.DataFrame(cust_list)
    cust.set_index('Account', inplace=True)
    return cust


def create_test_card(cust, nr_cards_over_one):
    """
    Minden ügyfélnek generál egy random kártyát,
    ezen felül még nr_cards_over_one darabot véletlenszerűen
    """
    cardlist = list()
    # Minden ügyfélnek egy kártya
    for acc in cust.index:
        cardlist.append({'Account': acc,
                         'Card': generate_random_cardnr(),
                         'Type': rand_list(account_types)})
    # És még nr_...
    for i in range(nr_cards_over_one):
        cardlist.append({
                'Account': cust.index[random.randint(0,len(cust.index)-1)],
                'Card': generate_random_cardnr(),
                'Type': rand_list(account_types)})
    # DataFrame
    cards = pd.DataFrame(cardlist)
    cards.set_index('Card', inplace=True)
    cards.to_csv('cards.csv')
    return cards


def write_static_db(cust, card, merch):
    """
    Writes the Customer and Card DataFrames to MySQL Db
    """
    import mysql.connector
    from sqlalchemy import create_engine
    from sqlalchemy.types import Float, String, BigInteger, Integer
    db_con = 'mysql+mysqlconnector://rtdm:rtdm123Kecske@localhost:3306/rtdm'
    engine = create_engine(db_con, echo=False, encoding='utf-8')
    (cust[cust_columns]
     .reset_index()
     .to_sql(name='customer',
             con=engine,
             dtype={'Account': BigInteger, 'Age': Integer,
                    'Gender': String(1), 'Name': String(50),
                    'Tel': String(20),
                    'BalanceAmount': Integer,
                    'CrmSegment': String(15),
                    'ShortTermCredit': String(1),
                    'FamilyMembers': Integer,
                    'TransactionTrend': String(10),
                    'IncomeCategory': String(5),
                    'NrOfDebCards': Integer,
                    'NrOfCredCards': Integer,
                    'CreditScore': String(5),
                    'AvgMonthlySpending': Integer,
                    'CreditLimit': Integer,
                    'PreviousDaySpending': Integer},
             if_exists='replace',
             index=False))
    card.reset_index().to_sql(name='bank_card',
                              con=engine,
                              dtype={'Card': String(20),
                                     'Account': BigInteger,
                                     'Type': String(21)},
                              if_exists='replace',
                              index=False)
    merch.reset_index().to_sql(name='merchant',
                               con=engine,
                               dtype={'id': Integer, 'name': String(30),
                                      'type': String(20), 'long': Float,
                                      'lat': Float, 'category': String(20)},
                               if_exists='replace',
                               index=False)
    # Create Primary keys
    with engine.connect() as con:
        con.execute('ALTER TABLE bank_card ADD PRIMARY KEY (Card);')
        con.execute('ALTER TABLE customer ADD PRIMARY KEY (Account);')
        con.execute('ALTER TABLE merchant ADD PRIMARY KEY (id);')


def get_random_trans(cardNumber, cardType, trans_date, feature_flag=None):
    """
    Returns a transaction dict.
    feature_flag = None: No feeture at all, 1: Feature set, 0: Feature no
    """
    randmerchcatid = rand_list(list(merchant_category.keys()))
    randmerchcat = merchant_category[randmerchcatid]
    merchant = rand_list(merchants[randmerchcatid])
    trans = {'accountNumber': cardNumber,
             'accountType': cardType,
             'merchantId': merchant['id'],
             'merchantType': randmerchcatid,
             'transactionId': transNr.getNr(),
             'amount': random.randrange(randmerchcat['min_value'],
                                        randmerchcat['max_value']),
             'currency': 'HUF',
             'isCardPresent': "True",
             'transactionTimeStamp': trans_date}
    # Add feature
    if feature_flag is None:
        # Ha nem modellezünk, nem írja fel a feature flaget
        pass
    else:
        # Modellezéskor meg felírja
        trans['feature_1'] = feature_flag
    return trans


def create_test_transactions(nr_trips, nr_unknown, cust, card, is_model,
                             filename):
    """
    Véletlen tranzakciós adatokat generál.
    Trip, néhány vásárlást érintő útvonal, random hosszú.
    UnKnown: véletlen kártyaszám.
    DataFrame, kiírja CSV fájlba.

    is_model: True esetén efature flaget átadja
    """
    import csv
    trans_list = list()
    # Tranzakciók az ügyfelekre
    for i in range(nr_trips):
        # Index of the card item
        randind = random.randrange(0, len(card))
        isCandidate = (cust
                       .loc[card.iloc[randind]['Account']]
                       ['CandidateTargetCreditIncrease'])
        if isCandidate == 0:
            # Nem speciális ügyfél
            # Vásárlások hossza szép normális legyen, de torzítva min 1-re
            trip_len = int(max(1, np.random.normal(loc=4, scale=4)))
        else:
            # Speciális ügyfél
            # Vásárlások hossza szép normális legyen, de torzítva min 3-re
            trip_len = int(max(3, np.random.normal(loc=6, scale=4)))
        # Bevásárló utakat generálunk
        trip_start = random.randrange(0, 86400)
        for trip in range(trip_len):
            trans_stamp = (simualtion_stamp +
                           trip_start +
                           trip * trip_delta * 60)
            feature_flag = None
            if is_model:
                feature_flag = 1 if ((trip == int(trip_len / 2)) &
                                     (isCandidate == 1)) else 0
            trans = get_random_trans(cardNumber=card.index[randind],
                                     cardType=card.iloc[randind]['Type'],
                                     trans_date=trans_stamp,
                                     feature_flag=feature_flag)
            trans_list.append(trans)

    # Ismeretlen kártyás tranzakciók
    if is_model:
        feature_flag = 0
    else:
        feature_flag = None
    for j in range(nr_unknown):
        trans_stamp = simualtion_stamp + random.randrange(0, 86400)
        trans = get_random_trans(cardNumber=generate_random_cardnr(),
                                 cardType=rand_list(account_types),
                                 trans_date=trans_stamp,
                                 feature_flag=feature_flag)
        trans_list.append(trans)
    # DataFrame, rendezés
    if is_model:
        trans_df = (pd.DataFrame(trans_list)
                    [['accountNumber', 'accountType', 'merchantId',
                      'merchantType', 'transactionId', 'amount', 'currency',
                      'isCardPresent', 'transactionTimeStamp', 'feature_1']]
                    .sort_values('transactionTimeStamp'))
        trans_df.to_csv(filename,
                        sep=';',
                        header=True,
                        index_label='idx',
                        encoding='UTF-8',
                        quoting=csv.QUOTE_ALL)
    else:
        trans_df = (pd.DataFrame(trans_list)
                    [['accountNumber', 'accountType', 'merchantId',
                      'merchantType', 'transactionId', 'amount', 'currency',
                      'isCardPresent', 'transactionTimeStamp']]
                    .sort_values('transactionTimeStamp'))
        trans_df.to_csv(filename,
                        sep=';',
                        header=False,
                        index_label='idx',
                        encoding='UTF-8',
                        quoting=csv.QUOTE_ALL)
    return trans_df



# Params
simulation_start = "2018.04.01 08:00:00"
epoch=dt.datetime.fromtimestamp(0)
simualtion_stamp = (
    dt.datetime.strptime(simulation_start.strip(),
                         '%Y.%m.%d %H:%M:%S') - epoch).total_seconds()
trip_delta = 5      # 5 percenként vásárol

# Create Customers for Modeling
cust_model_normal = create_test_customers(nr_of_cust=325,
                                          cust_type='normal')
cust_model_model1 = create_test_customers(nr_of_cust=75,
                                          cust_type='model1')
cust_model = cust_model_normal.copy().append(cust_model_model1)
# Create Customers for simulation
cust_simul_normal = create_test_customers(nr_of_cust=250,
                                          cust_type='normal')
cust_simul_model1 = create_test_customers(nr_of_cust=50,
                                          cust_type='model1')
cust_simul = cust_simul_normal.copy().append(cust_simul_model1)
# All customer
cust_all = cust_model.copy().append(cust_simul)


# Generates test cards
card_model = create_test_card(cust_model, nr_cards_over_one=200)
card_simul = create_test_card(cust_simul, nr_cards_over_one=200)
# Create mercahnt df
merch = generate_merchants_df()
# Saves to MySQL
write_static_db(cust_all, card_model.append(card_simul), merch)


# Write CSV for csak azért, hogy legyen
cust_model.to_csv('customer_model.csv')
cust_simul.to_csv('customer_simul.csv')

# Create transactions for the customers
# Simulation data, no feature flag
trans_simul = create_test_transactions(nr_trips=500,
                                       nr_unknown=50,
                                       cust=cust_simul,
                                       card=card_simul,
                                       is_model=False,
                                       filename="transaction_simul.csv")
# MOdel data, with feature flag
trans_model = create_test_transactions(nr_trips=500,
                                       nr_unknown=50,
                                       cust=cust_model,
                                       card=card_model,
                                       is_model=True,
                                       filename="transaction_model.csv")

# Modellezéshez a teljes adatsetet előállítja
# Tranzakció + Kártya, Account miatt
df_model = trans_model.copy().merge(card_model,
                           how='inner',
                           left_on='accountNumber',
                           right_index=True)
# Eddigiek + Customer
df_model = df_model.merge(cust_model,
                          how='inner',
                          left_on='Account',
                          right_index=True)
# + Merchant
df_model = df_model.merge(merch,
                          how='inner',
                          left_on='merchantId',
                          right_index=True)
# Csak azok az oszlopok kellenek, amelyek megvannak a NiFiben is + feature_1
df_model = df_model[["TransactionTrend", "Account", "FamilyMembers", "Gender",
                     "long", "Name", "AvgMonthlySpending", "merchantId",
                     "CreditScore", "merchantType", "Age", "lat", "amount",
                     "BalanceAmount", "PreviousDaySpending", "accountType",
                     "CreditLimit", "accountNumber", "transactionId",
                     "IncomeCategory", "name", "NrOfDebCards", "Tel",
                     "CrmSegment", "ShortTermCredit", "NrOfCredCards",
                     "feature_1"]]

df_model.to_csv('model_simul.csv')
