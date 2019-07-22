# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:05:59 2019

Search mendeley catalog for queries in search list.

@author: vince
"""
# Import libraries
import pandas as pd
import client

def searchMendeley(query, session=None, close ='yes'):
    '''
    Searches mendeley catalog with given query term on existing session.
    Session must be authenticated with startSession() prior.
    Returns an iterable catalog search object
    '''
    if session == None:
        session = client.startSession()
    
    search = session.catalog.search(query=query).iter()
    
    if close == 'yes':
        client.closeSession()
    
    return search

def listSearchFiles(search_obj, num_records=5):
    '''
    Takes iterable search_obj and iterates through num_records count of 
    Mendeley document objects and capture file information.
    
    Returns list of XXXX
    '''
    for count, item in enumerate(search_obj):
        if count > 5:
            break
        else:
            for x in item.files.iter():
                try:
                    print(x.file_name)
                except MendeleyApiException:
                    print('No files found or error')
                except:
                    print('unknown error has occured')
                    
        