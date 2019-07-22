# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:57:39 2019

todo pull this directly from google API

@author: vince
"""
slist = []

# Clean the text
with open('search_list.txt') as f:
    slist = f.readlines()

for i, row in enumerate(slist):
    slist[i] = ' '.join(row.split(' ')[3:])

for i, row in enumerate(slist):
    if row.find(' ') == 1:
        slist[i] = row[2:]
        
slist[7] = "HIV/AIDS"

for i, row in enumerate(slist):
    slist[i] = row.rstrip()

# Create a set of unique values
search_set = set(slist)

# Write set back to file for later use
with open('search_clean.txt', 'w+') as f:
    for item in search_set:
        f.write(item+',')
        
