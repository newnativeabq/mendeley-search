# -*- coding: utf-8 -*-
"""
Client Op
Created on Sat Jul 20 14:26:14 2019

gets credectials from cred.py and password
takes search terms and sends requests to mendeley
exports returned objects to storage.

@author: vince
"""
#   Import libraries
import cred
from mendeley import Mendeley

def startSession():
    '''
    Initializes credential flow and returns session object for search
    '''
    credentials = cred.getCred()
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    
    mendeley = Mendeley(client_id, client_secret=client_secret)
    auth = mendeley.start_client_credentials_flow()
    session = auth.authenticate()
    print('Session open command sent')
    return session

    
def closeSession(session):
    session.close()
    print('Close session command sent')
    

if __name__ ==  "__main__":
    mendeley_session = startSession()
    print(type(mendeley_session))

