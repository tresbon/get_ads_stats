from requests import request
from json import dumps

with open('','r') as f:
    ids = f.read()

with open('token.txt', 'r') as f:
    token = f.read()

def create_request (link, token, ids):

    link = ''

    data = {
        'key':'value',
        'key2':'value2'
    }

    rqst = request('POST', link, data)

    print (rqst.ok)

    return 

