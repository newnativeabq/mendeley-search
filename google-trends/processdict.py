# -*- coding: utf-8 -*-
"""
ProcessDict
Returns dataframe random sample of size n from medical dictionary sorted by
Lexical difficulty.

Created on Tue Jul 30 21:30:48 2019

@author: vince
"""
import pandas as pd

class request():
    def __init__(self, n=10, dictionary='meddict_clean.csv'):
        self.n = n
        self.dictionary = dictionary
        self.terms = self.getTerms()
        
    def getTerms(self, **kw):
        return loadDict(self.dictionary).sample(self.n)
    

def loadDict(filename):
    '''
    Loads dictionary file and returns dataframe object
    '''
    df = pd.read_csv(filename)
    return df

