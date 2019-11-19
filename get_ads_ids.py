from requests import request
from json import dumps,loads
import pandas as pd
from time import sleep
import os

def get_clients(account_id, token):
    link = 'https://api.vk.com/method/ads.getClients'
    data = {
    'account_id':str(account_id),
    'access_token':token,
    'v':'5.103'
    }
    r = request('POST', link, data=data)
    if r.ok:
        print ('Got clients')
        r = loads(r.text)
    if 'error' in r.keys():
        a  = [account_id]
    else:
        a = [i['id'] for i in r['response']]
    sleep(.3)
    return a

def get_ads(account_id,token):
    clients = get_clients(account_id,token)
    d = {'account_id':[],
    'client_id':[],
    'ad_id':[]}
    for client in clients:
        link = 'https://api.vk.com/method/ads.getAds'
        data = {
        'account_id':str(account_id),
        'client_id':str(client),
        'access_token':token,
        'v':'5.103'
        }
        r = request('POST', link, data=data)
        if r.ok:
            r = loads(r.text)
            r = [i['id'] for i in r['response']]
            for ad_id in r:
                d['account_id'].append(account_id)
                d['client_id'].append(client)
                d['ad_id'].append(ad_id)
        print(client, 'scanned')
        sleep(.5)
    pd.DataFrame(d).to_csv('ads_ids.csv', index=False)

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    with open('token.txt', 'r') as f:
        token = f.read().rstrip('\n')
    account_id = input('ID аккунта: ')
    get_ads(account_id,token)

if __name__ == "__main__":
    main()