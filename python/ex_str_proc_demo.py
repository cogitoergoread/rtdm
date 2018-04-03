#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 19:38:40 2018

@author: muszi

NiFi ExecuteStreamProcessor test
https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-standard-nar/1.5.0/org.apache.nifi.processors.standard.ExecuteStreamCommand/index.html

Read STDIN, JSON
Write STDOUT, JSON
"""


import sys
import json
from sklearn.externals import joblib

# Process the JSON from STDIN
data_rec = json.load(sys.stdin)


# Load persisted kNN Classifier
clf = joblib.load('model_estimator_test.pkl')

# Predict a feature based on the JSON fields
predicted = clf.predict(data_rec["BalanceAmount"])

# Add a new JSON field as a predicted value
data_rec['feature_1'] = int(predicted[0])

# Write the JSON to STDOUT
json.dump(data_rec, sys.stdout)
