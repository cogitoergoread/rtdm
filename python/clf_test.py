#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:55:37 2018

@author: muszi

Test Dummy KNN Classifier for RTDM decision model
Persit fitted model and loads it.
"""

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier

# Test Data
# http://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html#sklearn.datasets.make_classification
test_dta, test_feature = make_classification(n_features=1,
                                             n_informative=1,
                                             n_redundant=0,
                                             n_repeated=0,
                                             n_classes=2,
                                             n_clusters_per_class=1,
                                             n_samples=100)

# Legyen DF
df = pd.DataFrame(data=test_dta,
                  columns=['BalanceAmount'])
df['feature_1']= test_feature

# Transzformáljuk a Balance eloszlására. [314, 768576]
df['BalanceAmount'] = (314 + (768576 - 314) *
                       (df['BalanceAmount'] - df.BalanceAmount.min()) /
                       (df.BalanceAmount.max() - df.BalanceAmount.min()))

# Tanítunk
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(df['BalanceAmount'].values.reshape(-1, 1), df['feature_1'])

# Ellenőrzés
print("Predict 320:{}, 768000:{}".format(knn.predict(320), 
      knn.predict(7680000)))

# Perzisztálás
# http://scikit-learn.org/stable/modules/model_persistence.html

from sklearn.externals import joblib
joblib.dump(knn, 'model_estimator_test.pkl')


# Perzisztált model visszatöltése
clf = joblib.load('model_estimator_test.pkl')
print("Predict 320:{}, 768000:{}".format(clf.predict(320), 
      clf.predict(7680000)))
