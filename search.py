# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:05:59 2019

Search mendeley catalog for queries in search list.

@author: vince
"""
# Import libraries
import pandas as pd
import os

import client

# Debug functions

def searchMendeley(query, session=None, close ='yes'):
    '''
    Searches mendeley catalog with given query term on existing session.
    Session must be authenticated with startSession() prior.
    Returns an iterable catalog search object and the session object search, session 
    '''
    if session == None:
        session = client.startSession()
        
    search = session.catalog.search(query=query, view='all').iter()
    
    if (close == 'yes') and (session != None):
        client.closeSession(session)
    
    return search, session

def getFiles(doc_obj):
    '''
    Takes a single mendeley.catalog.doc object obtained in catalog.search.
    Returns an iterable files object that can be searched for files
    
    Returns list of file_names
    '''
    
    # Create a files iterator
    files = doc_obj.files
    
    def checkFiles(file_iter):
        '''
        Iterate through mendeley.resources.files.Files object and report information.
        ** Having activity scoped here allows try statement to pick up on API errors.
        '''
        for count, file in enumerate(file_iter):
            print(count)
            return count
    
    try:
        checkFiles(files)
    except:
        print('File Search Failed')
    
    return files


def buildSearchDict(search_obj, num_docs=10):
    '''
    Takes a mendeley.catalog.search object and returns a dictionary of
    documents and file objects.
    '''
    search_dict = {}
    for count, doc in enumerate(search_obj):
        print('checking document', count, ':', doc.file_attached)
        if count >= num_docs:
            break
        if not doc.file_attached:
            search_dict[type(doc)] = doc.file_attached
    return search_dict
        
        
        
        
        
        
        
        