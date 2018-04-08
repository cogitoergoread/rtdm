    
# coding: utf-8

# # Reading and preprocessing data

# In[1]:


import pandas as pd
import os
os.getcwd()


# In[2]:


path = 'f:\\Eszti\\Learning\\Kürt Akadémia Data Scientist\\realtime decisioning\\rtdm-master_v2\\python\\model'


# In[3]:


os.chdir(path)


# In[4]:


path


# In[5]:


df = pd.read_csv("model_simul_orig.csv")


# In[6]:


df.head()


# In[7]:


columnNames = list(df)# header list


# In[8]:


columnNames


# In[9]:
Info_Szoveg = """
Arra jöttem rá, hogy a model adatok között a tranzakciós jellegűeket ki kell
dobnunk. Ugyanis az ügyfeleket szedtük szét.
Én minden ügyfélhez sok vásárlási tranzakciót generáltam.
A normál ügyfeleknél a feature_1 == 0, mindenhol.
De a kiemelt ügyfeleinkre is igaz, hogy a vásárlásaik nagy részében
feature_1 == 0, és csak egyetlenre lesz feature_1 == 1.
A többi változó meg ezekre a rekordokra kb zaj, és ettől kezdve nem lehet 
rendesen tanulni rá.

Szóval, redukáljuk a változóinkat!
A tranzakciókhoz kapcsolódókat dobjuk ki, csak az ügyfélhez tartozókat hagyjuk.
És úgy, hogy a feature_1 maradjon meg.

"""

#Unnamed 0 és transactionId id-k, szerepeltessük majd 0 súllyal a tanuláskor
#Name-et (cust name) és name -et (merchant name) kivettem, Tel-t is
predictorVariables = ['Unnamed: 0', 'TransactionTrend', 'FamilyMembers', 'Gender', 'AvgMonthlySpending', 'CreditScore',
 'merchantType', 'Age', 'amount', 'BalanceAmount', 'PreviousDaySpending', 'accountType', 'CreditLimit', 'transactionId', 
 'IncomeCategory','NrOfDebCards','CrmSegment','ShortTermCredit','NrOfCredCards']

# Joozsi: kivettem minden tranzakcióra vonatkozó mezőt, maradt a customer
predictorVariables = ['TransactionTrend', 'FamilyMembers', 'Gender', 'AvgMonthlySpending', 'CreditScore',
 'Age', 'BalanceAmount', 'PreviousDaySpending', 'CreditLimit', 
 'IncomeCategory','NrOfDebCards','CrmSegment','ShortTermCredit','NrOfCredCards']

targetVariable = ['feature_1']


# In[10]:
# Joozsi: kidobom az ismétlődő sorokat a df-ből:
df = (df[ predictorVariables + targetVariable]
      .sort_values(by='feature_1', ascending=False)
      .drop_duplicates(subset=predictorVariables, keep='first'))
# Azáltal, hogy előre szedtem a feature_1==1-et, és az elsőt tartjuk meg, jó.

# In[10]:
from param_dicts import crdtscore_list
# CreditScore categorical, ordered
df['CreditScore'] = (pd.Categorical(df['CreditScore'],
                                    categories=crdtscore_list,
                                    ordered=True)
                    .codes)

predictorVariables = ['AvgMonthlySpending', 'CreditScore',
 'Age', 'BalanceAmount', 'PreviousDaySpending', 'CreditLimit','NrOfDebCards','NrOfCredCards']


# In[10]:
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier 
import numpy as np

X_train, X_test, y_train, y_test = train_test_split(df[predictorVariables],
                                                    df[targetVariable],
                                                    random_state=0)
clf = DecisionTreeClassifier( ).fit(X_train, y_train)
ras = roc_auc_score(y_test, np.array(clf.predict_proba(X_test)[:,1]))
print(ras)

# In[10]:


df[predictorVariables].head()


# In[11]:


df[targetVariable].head()


# In[12]:


#Lehetséges pre-processing, ha a kategóriváltozók kibontása után szükség lenne rá
#Normalizálás, re-scaling, az értékek 0 és 1 közé
#from sklearn.preprocessing import MinMaxScaler ...scaler = MinMaxScaler(feature_range=(0, 1))
#Standardizálás (Gauss eloszlás szerint) 
#Normalizálás
#Binarizálás (küszöb alatt-felett 0 vagy 1)


# In[13]:


#TODO ezt javítani, mert a minta értékeitől függően más lesz az oszlopszám nominális kategóriaváltozók binárissá alakításánál
#szétszedjük tanuló és teszt halmazra
from sklearn.cross_validation import StratifiedKFold 
#tanuló-teszthalmaz 60%-40%
eval_size = 0.40
kf = StratifiedKFold(df['feature_1'],round(1. / eval_size))
train_indices, valid_indices = next(iter(kf))
X_train, y_train = df[predictorVariables].iloc[train_indices].copy(), df[targetVariable].iloc[train_indices].copy()
X_valid, y_valid = df[predictorVariables].iloc[valid_indices].copy(), df[targetVariable].iloc[valid_indices].copy()


# In[14]:


train_indices


# In[15]:


X_train.head()


# In[16]:


'''After the splitting of the data is done, leave this data out and don’t touch it. Any operations that are applied on
training set must be saved and then applied to the validation set. Validation set, in any case, should not be joined with the 
training set. Doing so will result in very good evaluation scores and make the user happy but instead he/she will be building a
useless model with very high overfitting.
'''


# In[17]:


#Kategória változók kezelése v1 - Upd: ezt lentebb szétszedem nominálisra és ordinálisra
categoricalFeatures = ['TransactionTrend', 'Gender', 'CreditScore', 'merchantType', 'accountType', 'IncomeCategory', 'CrmSegment','ShortTermCredit']
#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#le = LabelEncoder()
#a kategóriaváltozók értékeit kicserélem numerikusra 
#for i in range(0,len(categoricalFeatures)):
#    tmpArray = le.fit_transform(X_train[categoricalFeatures[i]])
#    X_train[categoricalFeatures[i]] = list(tmpArray)

#hiba:ordinálisnál a lexikális rendezés miatt veszik el info; nominálisnál algoritmustól függően akár érdemes tesztelni ennyi konverzió után

#szétdobom az oszlopokat érték db binárisra
#ohe = OneHotEncoder()
#xtrain_cat = ohe.fit_transform(X_train[categoricalFeatures])



# In[18]:


#kategória változók kezelése v2
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
#1. ordinális változók
ordinalFeatures = ['TransactionTrend', 'CreditScore', 'IncomeCategory']

tranTrend_mapping = {'IncInc': 0, 'Inc': 1, 'Stab': 2, 'Dec': 3, 'DecDec': 4, 'Inact': 5}
credScore_mapping = {'NO': 0, 'XS': 1, 'S' : 2, 'M': 3, 'L': 4, 'XL': 5}
incCat_mapping = {'XS': 0, 'S' : 1, 'M': 2, 'L': 3, 'XL': 4, 'XXL': 5}

#X_train['TransactionTrendNew'] = X_train['TransactionTrend'].apply(tranTrend_mapping.get).astype(float)
df_ordinal = X_train[ordinalFeatures].copy()
df_ordinal['enc_TransactionTrend'] = X_train['TransactionTrend'].map(tranTrend_mapping)
df_ordinal['enc_CreditScore'] = X_train['CreditScore'].map(credScore_mapping)
df_ordinal['enc_IncomeCategory'] = X_train['IncomeCategory'].map(incCat_mapping)

#2. nominális változók
nominalFeatures = ['Gender', 'merchantType', 'accountType', 'CrmSegment', 'ShortTermCredit']
#szétdobom az oszlopokat érték db binárisra
df_nominal = pd.get_dummies(X_train, columns = nominalFeatures)
df_nominal.to_csv('testNominal.csv')


# In[19]:


df_nominal.head(20)


# In[20]:


#pd.DataFrame(xtrain_cat.toarray()).to_csv('testSparseMatrix.csv')


# # Applying the same transformations on the validation set

# In[21]:


df_ordinalValid = X_valid[ordinalFeatures].copy()
df_ordinalValid['enc_TransactionTrend'] = X_valid['TransactionTrend'].map(tranTrend_mapping)
df_ordinalValid['enc_CreditScore'] = X_valid['CreditScore'].map(credScore_mapping)
df_ordinalValid['enc_IncomeCategory'] = X_valid['IncomeCategory'].map(incCat_mapping)

df_nominalValid = pd.get_dummies(X_valid, columns = nominalFeatures)


# In[22]:


df_nominalValid.head(5)


# # Concatenating features together

# In[23]:


# X_train - categoricalfeatrues + df_ordinal(enc helyen) + df_nominal (csak új mezők)#
#training set
df_ordinalNew = df_ordinal.drop(ordinalFeatures, axis = 1)
df_allButOrdinal = df_nominal.drop(ordinalFeatures, axis = 1)
X_trainNew = pd.concat([df_allButOrdinal, df_ordinalNew], axis = 1)

#validation set
df_ordinalValidNew = df_ordinalValid.drop(ordinalFeatures, axis = 1)
df_allButOrdinalValid = df_nominalValid.drop(ordinalFeatures, axis = 1)
X_validNew = pd.concat([df_allButOrdinalValid, df_ordinalValidNew], axis = 1)


# In[24]:


X_validNew.head()


# # Applying models

# In[25]:


#try with Logistic Regression, Random Forest, Xgboost, KNeighboursRegressor
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1.0) #default, TODO tesztelni más értékekkel
model.fit(X_trainNew, y_train.values.ravel())


# In[26]:


model.coef_


# In[28]:


testArray = model.predict(X_validNew) 

#hiba: X has 32 features per sample; expecting 38
#--> df_nominalValid = pd.get_dummies(X_valid, columns = nominalFeatures)  itt van hiba: a validációs halmazban nem fordul elő
# minden nominális változó összes értéke, ami a tréningben igen --> StratifiedKFold-ot lecserélni/valahogy megoldani, hogy minden
# érték kerüljön mindenhová


# In[29]:


testArray


# In[33]:


for i in range(0,len(testArray)):
    print(testArray[i])

