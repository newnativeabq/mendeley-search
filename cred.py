# -*- coding: utf-8 -*-
"""
Cred

Credentialing and encryption engine for Mendeley project

Encrypts/Decrypts files with input password as seed for symmetric encryption.
Small, non-critical storage only.  Intended for use in credentials for full git push (because I'm lazy)

Helper class dependent function genKey modified to take environment variables salt and password to generate key across runs.
This way, the api credentials will always be available via the same password.

Created on Sat Jul 20 12:19:48 2019

@author: vince
"""
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class helper():
    def __init__(self, key=None):
        if key == None:
          self.key = genKey()
        self.data = 0

    def lockStore(self, token):
        self.data = self.key.encrypt(bytes(token, 'utf-8'))
    
    def unlock(self):
        return str(self.key.decrypt(self.data), 'utf-8')


def genKey():
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bytes(os.environ.get('salt'), 'utf-8'),
            iterations=100000,
            backend=default_backend()
            )
    key = base64.urlsafe_b64encode(
            kdf.derive(bytes(os.environ.get('password'), 'utf-8'))
            )
    f = Fernet(key)
    return f

def getSalt(path='salt.txt'):
    with open(path, 'r') as f:
        return f.read()


def readFile(file_path):
    '''
    Open file at file path and return full read of file.
    '''
    with open(file_path, 'r') as f:
        return f.read()

def writeFile(data, file_path):
    '''
    Write comma delimited txt file from list of strings.
    Adds commas, so don't include them in str.
    '''
    with open(file_path, 'w+') as f:
        if type(data) == list:
            for item in data:
                if len(item) > 0:
                    f.write(item+',')
        elif type(data) == str:
            f.write(data)
                
def parseComma(string):
    '''
    Return list of str items
    '''
    if type(string) == str:
        return string.split(',')

def setEnv(var_name, value):
    '''
    Take variable and add as environment variable in process
    '''
    os.environ[var_name] = value
    
'''
Getting the credentials with a password
'''

def getCred():
    setEnv('password', input('Enter Password:'))
    setEnv('salt', getSalt())
    
    worker = helper()
    worker.data = bytes(readFile('cred_hash.txt'), 'utf-8')
    return worker.unlock()

def main():
    #   Setup environment   
    setEnv('password', input('Enter Password:'))
    setEnv('salt', getSalt())
    
    #   Initialize data carrier
    worker = helper()
    
    #   Load unencrypted information
    try:
        raw_data = readFile('cred_raw.txt')
    except:
        print('Raw credentials not found.  Check cred_raw.txt location')

    #   Give raw_data to helper for encryption and storage
    worker.lockStore(raw_data)
    
    #   Write encrypted information to file
    try:
        writeFile(str(worker.data, 'utf-8'), 'cred_hash.txt')
    except:
        print('Could not write to cred_hash.txt')


if __name__=='__main__':
    main()
    