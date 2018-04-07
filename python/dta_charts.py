#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 07:44:39 2018

@author: muszi

Create nice graphs to be included in final PPT
"""
# In[ ]:

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from param_dicts import crdtscore_list

# In[ ]:
# Import and filter Customer data
df = pd.read_csv("customer_model.csv",
                 index_col="Account",
                 usecols=["AvgMonthlySpending", "BalanceAmount",
                          "CreditScore", "Account"],
                 )
# CreditScore categorical, ordered
df['CreditScore'] = (pd.Categorical(df['CreditScore'],
                                    categories=crdtscore_list,
                                    ordered=True)
                    .codes)
# BalDiff = AvgMonthlySpending - BalanceAmount
df['BalDiff'] = df['AvgMonthlySpending'] - df['aBalanceAmount']
# Feature_1 visszaállítása
df['feature_1'] = 0
df.loc[df['CreditScore']>2, "feature_1"] = 1
 
# In[ ]:
# Jó / még jobb ügyfelek
df_jo = df[df['feature_1'] ==0].dropna()
df_megjobb = df[df['feature_1'] ==1].dropna()



# In[ ]:
# Szép scatter plot
colors_jo = ['green']*(len(df_jo))
colors_megjobb = ['red']*(len(df_megjobb))

# New figure
plt.figure()

# plot the point with size 100 and chosen colors
plt.scatter(df_jo['BalDiff'], df_jo['CreditScore'],
            s=100, c=colors_jo, label='Jó ügyfelek')
plt.scatter(df_megjobb['BalDiff'], df_megjobb['CreditScore'],
            s=100, c=colors_megjobb, label='Még jobb ügyfelek')
# add a label to the x axis
plt.xlabel('Különbség az átlagos költés és az egyenleg között')
# add a label to the y axis
plt.ylabel('Hitelképességi kategória')
# add a title
plt.title('Random bank ügyfelek kategória és egyenleg függése')
# add a legend (uses the labels from plt.scatter)
plt.legend()
# Show the figure
plt.show()

# In[ ]:
# Másik szép ábra, vásárlások számának eloszlása

# Nem speciális ügyfél
# Vásárlások hossza szép normális legyen, de torzítva min 1-re

# Vektirizált maximum függvény
vfunc = np.vectorize(max)
# Eloszlás a jókra
trip_len_jo = np.trunc(vfunc(np.ones(325),np.random.normal(loc=4, scale=4, size=325)))
# Eloszlás a még jobbakra
trip_len_megjobb = np.trunc(vfunc(np.ones(75)*3,np.random.normal(loc=6, scale=4, size=75)))

# In[ ]:

# New figure
plt.figure()

# Histograms
plt.hist(trip_len_jo, bins=30, color='green', alpha=0.5, label='Jó ügyfelek')
plt.hist(trip_len_megjobb, bins=30, color='red', alpha=0.3, label='Még jobb ügyfelek')
# add a label to the x axis
plt.xlabel('Vásárlások száma')
# add a label to the y axis
plt.ylabel('Ügyfelek darabszáma')
# add a title
plt.title('Random bank ügyfelek vásárlási szokásai')
# add a legend (uses the labels from plt.hist)
plt.legend()
# Show the figure
plt.show()

# In[ ]:
