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
import sys, json;
data_rec = json.load(sys.stdin)

data_rec['feature_1'] = 1

json.dump(data_rec, sys.stdout)