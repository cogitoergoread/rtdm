#!/usr/bin/env python
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
import logging

# Set logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)

# Process the JSON from STDIN
data_rec = json.load(sys.stdin)
logging.debug('Incoming')
logging.debug(data_rec)

# Load persisted kNN Classifier
clf = joblib.load('model_estimator_test.pkl')

# Predict a feature based on the JSON fields
try:
    predicted = int(clf.predict(data_rec["BalanceAmount"])[0])
    logging.debug('predict OK. :{}'.format(predicted))
except:
    predicted = 0
    logging.debug('predict Exception')

# Simple print
print(predicted)
exit(0)

# Add a new JSON field as a predicted value
data_rec[u'feature_1'] = u'{}'.format(predicted)

logging.debug('Outgoing')
logging.debug(data_rec)



# Write the JSON to STDOUT
json.dump(data_rec, sys.stdout)

exit(0)
