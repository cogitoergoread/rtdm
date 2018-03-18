#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 10:41:30 2018

@author: muszi
"""

import random
import pandas as pd
import numpy as np
import datetime as dt

# Dict of Dict, Külső kategóriák, belső: tranzakció értékek
merchant_category = {
        'élelmiszer' : {'min_value' : 500, 'max_value' : 38000},
        'étterem' :  {'min_value' : 2000, 'max_value' : 10000},
        'ruházat' :  {'min_value' : 5000, 'max_value' : 27000},
        'egészség' :  {'min_value' : 1000, 'max_value' : 40000},
        'elektronikai' :  {'min_value' : 10000, 'max_value' : 250000},
        'üzemanyag' :  {'min_value' : 5000, 'max_value' : 20000},
        'szórakozás' :  {'min_value' : 1000, 'max_value' : 8000},
        'könyv' :  {'min_value' : 2000, 'max_value' : 7000},
        'utazás' :  {'min_value' : 50000, 'max_value' : 350000}}

# Kártya fajták
account_types = ['VISA', 'MASTERCARD', 'JCB', 'MAESTRO', 'AMEX', 'DINERS']

# Keresedők, kategóriák alapján Dict of Dict
merchants = {
        'élelmiszer' : [{'id' : 1001, 'name' : "CBA Déli", 'lat' : 47.4993318, 'long' : 19.0237523},
                        {'id' : 1002, 'name' : "Spar Király", 'lat' : 47.50098 , 'long' : 19.0593837},
                        {'id' : 1003, 'name' : "Aldi Kossuth", 'lat' : 47.4937711, 'long' : 19.0564734}],
        'étterem' :  [{'id' : 1010, 'name' : "Tüköry", 'lat' : 47.5050979, 'long' : 19.0504007},
                      {'id' : 1011, 'name' : "Kaltenberg", 'lat' :47.4861163, 'long' : 19.0647328},
                      {'id' : 1012, 'name' : "Wang mester", 'lat' :47.5098377 , 'long' : 19.0981019}],
        'ruházat' :  [{'id' : 1020, 'name' : "Berhska WE", 'lat' : 7.5132144, 'long' : 19.0568654},
                      {'id' : 1021, 'name' : "TomTailor ÁR", 'lat' : 47.5024646, 'long' : 19.1347594},
                      {'id' : 1022, 'name' : "Trapper Fő", 'lat' : 47.511583, 'long' : 19.035859}],
        'egészség' :  [{'id' : 1030, 'name' : "Egressy Patika", 'lat' : 47.5065185, 'long' : 19.1019453},
                      {'id' : 1031, 'name' : "Best Dental", 'lat' : 47.4999491, 'long' : 19.0571779},
                      {'id' : 1032, 'name' : "Életerő mozgás", 'lat' : 47.510766, 'long' : 19.0513418}],
        'elektronikai' :  [{'id' : 1040, 'name' : "MediaMarkt ARE", 'lat' : 47.4983895, 'long' : 19.0913913},
                      {'id' : 1041, 'name' : "Mérkabolt Józ", 'lat' : 47.4955751, 'long' : 19.0689243},
                      {'id' : 1042, 'name' : "HiFi Station", 'lat' : 47.517732, 'long' : 19.141521}],
        'üzemanyag' :  [{'id' : 1050, 'name' : "MOL Róna", 'lat' : 47.5135858, 'long' : 19.1208947},
                      {'id' : 1051, 'name' : "OMV Hun", 'lat' : 47.50853, 'long' : 19.0997001},
                      {'id' : 1052, 'name' : "Shell Váci", 'lat' : 47.558184, 'long' : 19.07439}],
        'szórakozás' :  [{'id' : 1060, 'name' : "ZAK", 'lat' : 47.5031823, 'long' : 19.0621811},
                      {'id' : 1061, 'name' : "Katona", 'lat' : 47.4936625, 'long' : 19.0526852},
                      {'id' : 1062, 'name' : "A38", 'lat' : 47.4771073, 'long' : 19.0602603}],
        'könyv' : [{'id' : 1070, 'name' : "Írók boltja", 'lat' : 47.5042391, 'long' : 19.0599304},
                      {'id' : 1071, 'name' : "TypoTex", 'lat' : 47.5085084, 'long' : 19.0194369},
                      {'id' : 1072, 'name' : "Libri Blaha", 'lat' : 47.496119, 'long' : 19.066945}],
        'utazás' : [{'id' : 1080, 'name' : "Vista Andr", 'lat' : 47.499512, 'long' : 19.053063},
                      {'id' : 1081, 'name' : "IBUSZ Feren", 'lat' :47.492694 , 'long' : 19.053128},
                      {'id' : 1082, 'name' : "Neckermann Vörö", 'lat' : 47.49721, 'long' : 19.0488859}]}


def generate_random_name(gender):
    first_name_wmn = ['Hanna', 'Anna', 'Jázmin', 'Nóra', 'Boglárka', 'Zsófia', 'Lili', 'Réka', 'Dóra', 'Luca', 'Viktória', 'Emma', 'Vivien', 'Laura', 'Eszter', 'Fanni', 'Petra', 'Lilla', 'Csenge', 'Noémi', 'Sára', 'Dorina', 'Gréta', 'Zoé', 'Dorka', 'Rebeka', 'Bianka', 'Flóra', 'Léna', 'Panna', 'Lara', 'Maja', 'Kamilla', 'Szonja', 'Fruzsina', 'Virág', 'Blanka', 'Kinga', 'Ramóna', 'Kitti', 'Tímea', 'Janka', 'Kata', 'Júlia', 'Dorottya', 'Emese', 'Vanessza', 'Izabella', 'Mira', 'Nikolett', 'Liza', 'Veronika', 'Tamara', 'Alíz', 'Emília', 'Lilien', 'Kira', 'Adrienn', 'Amanda', 'Borbála', 'Leila', 'Kincső', 'Adél', 'Zselyke', 'Diána', 'Natália', 'Melissza', 'Abigél']
    first_name_men = ['Bence', 'Máté', 'Levente', 'Ádám', 'Dávid', 'Balázs', 'Dominik', 'Péter', 'Gergő', 'Milán', 'Tamás', 'Zsombor', 'Dániel', 'Bálint', 'Botond', 'Kristóf', 'Zalán', 'Áron', 'László', 'Márk', 'Attila', 'Zoltán', 'Noel', 'Marcell', 'András', 'Benedek', 'Ákos', 'Gábor', 'István', 'Olivér', 'Márton', 'Patrik', 'Roland', 'Zsolt', 'Kevin', 'János', 'Martin', 'Csaba', 'Hunor', 'Richárd', 'Benett', 'Gergely', 'József', 'Norbert', 'Nimród', 'Róbert', 'Sándor', 'Alex', 'Zétény', 'Ferenc', 'Erik', 'Viktor', 'Mátyás', 'Ábel', 'Kornél', 'Vince', 'Mihály', 'Nándor', 'Csongor', 'Tibor', 'Rikárdó', 'Ármin', 'Csanád', 'Adrián', 'Miklós', 'Imre', 'György', 'Gyula', 'Vilmos', 'Soma', 'Kende']
    last_name = ['Nagy', 'Kovács', 'Tóth', 'Szabó', 'Horváth', 'Varga', 'Kiss', 'Molnár', 'Németh', 'Farkas', 'Balogh', 'Papp', 'Takács', 'Juhász', 'Lakatos', 'Mészáros', 'Oláh', 'Simon', 'Rácz', 'Fekete', 'Szilágyi', 'Török', 'Fehér', 'Balázs', 'Gál', 'Kis', 'Szűcs', 'Kocsis', 'Orsós', 'Pintér', 'Fodor', 'Szalai', 'Sipos', 'Magyar', 'Lukács', 'Gulyás', 'Biró', 'Király', 'László', 'Katona', 'Jakab', 'Bogdán', 'Balog', 'Sándor', 'Boros', 'Fazekas', 'Kelemen', 'Váradi', 'Antal', 'Somogyi', 'Orosz', 'Fülöp', 'Veres', 'Vincze', 'Hegedűs', 'Budai', 'Deák', 'Pap', 'Bálint', 'Pál', 'Illés', 'Vass', 'Szőke', 'Vörös', 'Bognár', 'Fábián', 'Lengyel', 'Bodnár', 'Szücs', 'Hajdu', 'Halász', 'Jónás', 'Máté', 'Székely', 'Kozma', 'Gáspár', 'Pásztor', 'Bakos', 'Dudás', 'Major', 'Orbán', 'Hegedüs', 'Virág', 'Barna', 'Novák', 'Soós', 'Tamás', 'Nemes', 'Pataki', 'Balla', 'Faragó', 'Kerekes', 'Borbély', 'Barta', 'Péter', 'Szekeres', 'Csonka', 'Mezei', 'Márton', 'Sárközi']
    return (last_name[random.randint(0, len(last_name)-1)] +
                      " " +
                      ( first_name_wmn[random.randint(0, len(first_name_wmn)-1)]
                      if gender == 'N' else
                      first_name_men[random.randint(0, len(first_name_men)-1)] ))

def generate_random_cardnr():
    return "{:04d} {:04d} {:04d} {:04d}".format(random.randint(0, 9999),
            random.randint(0, 9999),
            random.randint(0, 9999),
            random.randint(0, 9999))

def create_test_customers(nr_of_cust):
    """
    Random ügyfeleket vesz fel.
    Ebből DataFrame-t generál, és kiírja customer.csv néven.
    """
    cust_list =list()
    for i in range(nr_of_cust):
        gender = "N" if random.randint(0, 2) == 0 else "F"
        cust_list.append({
                'Account' : "23001{:04d}".format(i),
                'Gender' : gender,
                'Name' : generate_random_name(gender),
                'Age' : random.randint(18,77),
                'Tel' : "3680{}".format(random.randint(100000, 887887))})
    cust = pd.DataFrame(cust_list)
    cust.set_index('Account', inplace=True)
    cust.to_csv("customer.csv")
    return cust

def create_test_card(cust, nr_cards_over_one):
    """
    Minden ügyfélnek generál egy random kártyát, 
    ezen felül még nr_cards_over_one darabot véletlenszerűen
    """
    cardlist = list()
    # Minden ügyfélnek egy kártya
    for acc in cust.index:
        cardlist.append({
                'Account' : acc,
                'Card' : generate_random_cardnr(),
                'Type' : account_types[random.randint(0, len(account_types)-1)]})
    # És még nr_...
    for i in range(nr_cards_over_one):
        cardlist.append({
                'Account' : cust.index[random.randint(0,len(cust.index)-1)],
                'Card' : generate_random_cardnr(),
                'Type' : account_types[random.randint(0, len(account_types)-1)]})
    # DataFrame
    cards = pd.DataFrame(cardlist)
    cards.set_index('Card', inplace=True)
    cards.to_csv('cards.csv')
    return cards

# Params
simulation_start = "2018.04.01 08:00:00"
epoch=dt.datetime.fromtimestamp(0)
simualtion_stamp = ( dt.datetime.strptime(simulation_start.strip(),
                                          '%Y.%m.%d %H:%M:%S') - epoch).total_seconds()
trip_delta = 5      # 5 percenként vásárol
cust = create_test_customers(nr_of_cust=300)
card = create_test_card(cust, nr_cards_over_one=200)
trans_id_start = 5382367345

def get_random_trans(cardNumber, cardType, trans_date):
    global trans_id_start
    randmerchcatid = (list(merchant_category.keys())
        [random.randrange(0, len(merchant_category))])
    randmerchcat = merchant_category[randmerchcatid]
    merchant = merchants[randmerchcatid][random.randrange(0,
                        len(merchants[randmerchcatid]))]
    trans_id_start +=1
    return {'accountNumber' : cardNumber,
            'accountType' : cardType,
            'merchantId' : merchant['id'],
            'merchantType' : randmerchcatid,
            'transactionId' : trans_id_start,
            'amount' : random.randrange(randmerchcat['min_value'],randmerchcat['max_value']),
            'currency' : 'HUF',
            'isCardPresent' : "True",
            'latitude' : merchant['lat'],
            'longitude' : merchant['long'],
            'ipAddress' : "",
            'transactionTimeStamp' : trans_date}


def create_test_transactions(nr_trips, nr_unknown):
    """
    Véletlen tranzakcis adatokat generál.
    Trip, néhány vásárlást érintő útvonal, random hosszú.
    UnKnown: véletlen kártyaszám.
    DataFrame, kiírja CSV fájlba.
    """
    import csv
    trans_list = list()
    # Tranzakciók az ügyfelekre
    for i in range(nr_trips):
        # Vásárlások hossza szép normális legyen, de torzítva min 1-re
        trip_len = int(max(1, np.random.normal(loc=4, scale=4)))
        # Index of the card item
        randind = random.randrange(0, len(card))
        for trip in range(trip_len):
            trans_stamp = (simualtion_stamp +
                           random.randrange(0, 86400) +
                           trip * trip_delta * 60 )
            trans_list.append(get_random_trans(cardNumber=card.index[randind],
                                               cardType=card.iloc[randind]['Type'],
                                               trans_date=trans_stamp))
    # DataFrame, rendezés
    for i in range(nr_unknown):
        trans_stamp = (simualtion_stamp +
                       random.randrange(0, 86400))
        trans_list.append(get_random_trans(cardNumber=generate_random_cardnr(),
                                           cardType=account_types[random.randint(0, len(account_types)-1)],
                                           trans_date=trans_stamp))
    trans_df = (pd.DataFrame(trans_list)
        [['accountNumber', 'accountType', 'merchantId', 'merchantType', 
          'transactionId', 'amount', 'currency', 'isCardPresent',
          'latitude', 'longitude', 'ipAddress', 'transactionTimeStamp']]
        .sort_values('transactionTimeStamp'))
    # trans_df.to_csv('transactions.csv')
    trans_df.to_csv('transactions.csv',
                    sep=';',
                    header=False,
                    index_label='idx',
                    encoding='UTF-8',
                    quoting=csv.QUOTE_ALL)
    return trans_df

create_test_transactions(200,20)
