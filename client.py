# -*- coding: utf-8 -*-
"""
Client Op
Created on Sat Jul 20 14:26:14 2019

gets credectials from cred.py and password
takes search terms and sends requests to mendeley
exports returned objects to storage.

@author: vince
"""

from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

import cred

def parseCred(creds):
    cred_list = creds.split(',')
    
    cred_dict = {}
    for line in cred_list:
        cred_dict[line.split(':')[0]] = line.split(':')[1]
    
    return cred_dict

print(parseCred(cred.getCred()))