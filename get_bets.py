from requests import request
from json import dumps,loads
import pandas as pd
from time import sleep
from datetime import datetime
import os

def make_request (ids, token, link = 'https://api.vk.com/method/ads.getTargetingStats'):
    '''Request recc CPM & CPC'''

    d = {
        'ad_id':[],
        'audience_count':[],
        'recommended_cpc':[],
        'recommended_cpm':[]
    }

    for acc in ids['account_id'].unique():
        for client in ids[ids['account_id']==acc]['client_id'].unique():
            for ad in ids[(ids['account_id'] == acc) & (ids['client_id'] == client)]['ad_id'].unique():

                data = {
                    'account_id':str(acc),
                    'client_id':str(client),
                    'ad_id':str(ad),
                    'link_url':'https://ya.ru',
                    'link_domain':'ya.ru',
                    'access_token':token,
                    'v':'5.103'
                }

                r = request('POST', link, data=data)
                print (ad, r.ok, r.text)
                if r.ok:
                    r = loads(r.text)
                else:
                    continue
                d['ad_id'].append(ad)
                for key in r['response'].keys():
                    d[key].append(r['response'][key])
                sleep (.5)
    return pd.DataFrame(d)

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    ids = pd.read_csv('ads_ids.csv')
    # https://oauth.vk.com/authorize?client_id=6003800&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=ads,offline&response_type=token&v=5.103
    with open('token.txt', 'r') as f:
        token = f.read().rstrip('\n')
    make_request(ids=ids, token=token).to_csv(f'stats_{datetime.now().strftime("%y-%d-%m_%H-%M")}.csv', index = False)


if __name__ == "__main__":
    main()




