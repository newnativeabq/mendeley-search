# -*- coding: utf-8 -*-
"""
Medical Trends
An implementation of pytrends API to search for terms on Google Trends
Created on Tue Jul 30 21:12:48 2019

@author: vince
"""
# Import search library
import processdict
from pytrends.request import TrendReq
from time import sleep
import pandas as pd
import numpy as np

class trendrequest():
    def __init__(self, term_list, session):
        self.term_list = term_list
        self.session = session
        self.trends = self.executePayloads()
    
    def __len__(self):
        return self.terms.count()[0]
    
    def executePayloads(self):
        return buildPayload(session=self.session, terms=self.term_list).interest_over_time()
    
class searchjob():
    def __init__(self, n_terms = 1, job_wait=60, max_per_thread=5):
        self.num_threads = self.threadCalc(n_terms, max_per_thread)
        self.max_per_thread = max_per_thread
        self.wait = job_wait
        self.searchdict = processdict.request(n=n_terms).terms
        self.search_response = []
        self.session = connectGoogle()
        self.incomplete = []
        self.complete = []
    
    def threadCalc(self, n_terms, max_per_thread):
        num_threads = int(n_terms/max_per_thread)
        if n_terms%max_per_thread:
            num_threads = int(n_terms/max_per_thread) + 1
        return max(1, num_threads)
    
    def splitList(self, search_list=None):
        work_list = []
        for thread in range(self.num_threads):
            start = thread * self.max_per_thread
            stop = (thread+1) * self.max_per_thread
            work_list.append(
                    self.searchdict[start:stop]
                    )
        return work_list
    
    def fetchTrends(self, complete=True):
        if complete == True:
            work_list = self.splitList()
        elif complete == False:
            work_list == self.splitList(search_list=self.incomplete)
        else:
            print('Work List Did Not Arrie to fetchTrends properly')
        
        for i in range(self.num_threads):
            # Goal: get trends and store series information in results dataframe
            frame = work_list[i].copy()
            
            try:
                len(frame.terms.values[0]) # force index error on null series
                trend_data = self.requestWait(term_list=frame.terms.values)                
                self.search_response.append(trend_data)
                self.complete.append(frame)
            except IndexError:
                continue
            except:
                self.incomplete.append(work_list[i:].copy())
                choice = input('Fetch did not complete.  Try again in 60s?')
                if choice: 
                    sleep(60)
            
    def requestWait(self, term_list=None):
        trends_obj = trendrequest(term_list, self.session)
        sleep(1)
        return trends_obj.trends

        
def connectGoogle():
    # Connect to google
    pytrends = TrendReq(hl='en-US', tz=360)
    return pytrends

def buildPayload(session=None, terms=None):
    # Take terms from dataframe and load into session payload
    kw_list = terms
    print('Building payload for:', kw_list)
    session.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    return session

def concatResponse(df_list):
    frame_list = []

    key = df_list[0].index
    for df in df_list:
        frame = df.drop(columns='isPartial').copy()
        frame.reindex(key)
        frame_list.append(frame)

    merged_frame = frame_list[0]
    for frame in frame_list[1:]:
        print('merging, ', type(frame))
        merged_frame = merged_frame.join(frame)

    return merged_frame

def saveDataFrame(df=None, filename=None):
    try:
        df.to_csv(filename)
    except:
        print('File could not be saved')




    