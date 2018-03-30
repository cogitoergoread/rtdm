#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 20:29:09 2018

@author: muszi

Parameters of test data: dictionary definitions
- Merchant category
- Merchant
- Account typa: bankkártya kibocsátók
"""
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

# CRM szegmens (Aktív folyószámlahiteles, Tranzaktáló hosszúhiteles)        
crm_segment = ['CreditAct', 'TransCredit', 'NoTrans', 'Young', 'Pension']

# Gender List, nemek N: Nő, F: Férfi 
gend_list = ['N', 'F']

# YesNo List
yn_list = ['Y', 'N']

# Tranzakciók változása (Csökkenés, Jelentõs csökkenés, Stabil, Inaktív, Jelentõs növekedés)
trchg_list = ['Dec', 'DecDec', 'Stab', 'Inc', 'IncInc', 'Inact']

# Income Category List  - Bevétel kategória (0-20M, 21-50M, 51-300M,..)
incmcat_list = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

# Hitel előminősített (0, 200-ig, 500-ig, 1m, 5m)
crdtscore_list = ['NO', 'XS', 'S', 'M', 'L', 'XL']
