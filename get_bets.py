from requests import request
from json import dumps,loads
import pandas as pd
from time import sleep
from datetime import datetime
import os
import collections 
    
def make_request (ids, token, link = 'https://api.vk.com/method/ads.getTargetingStats'):
    '''Request recommended CPM & CPC'''

    d = {
        'ad_id':[],
        'ad_platform':[],
        'audience_count':[],
        'recommended_cpc':[],
        'recommended_cpm':[]
    }

    for acc in ids['account_id'].unique():
        for client in ids[ids['account_id']==acc]['client_id'].unique():
            for ad in ids[(ids['account_id'] == acc) & (ids['client_id'] == client)]['ad_id'].unique():

                if 9 in ids[(ids['account_id'] == acc) & (ids['client_id'] == client) & (ids['ad_id'] == ad)]['ad_format']:
                    ad_platforms = ('all','desktop','mobile')
                elif 11 in ids[(ids['account_id'] == acc) & (ids['client_id'] == client) & (ids['ad_id'] == ad)]['ad_format']:
                    ad_platforms = ('all','desktop','mobile')
                elif 1  in ids[(ids['account_id'] == acc) & (ids['client_id'] == client) & (ids['ad_id'] == ad)]['ad_format']:
                    ad_platforms = (0,1)
                else: ad_platforms = [None]
                
                for ad_platform in ad_platforms:

                    data = {
                        'account_id':str(acc),
                        'client_id':str(client),
                        'ad_id':str(ad),
                        'link_url':'https://ya.ru',
                        'link_domain':'ya.ru',
                        'access_token':token,
                        'ad_platform':ad_platform,
                        'v':'5.103'
                    }
                    if data['ad_platform'] is None:
                        del(data['ad_platform'])

                    r = request('POST', link, data=data)
                    sleep(2)
                    print (ad, r.ok, r.text)
                    if r.ok:
                        r = loads(r.text)
                        if 'error' in r.keys():
                            continue
                    else:
                        continue
                    d['ad_id'].append(ad)
                    d['ad_platform'].append(ad_platform)
                    for key in r['response'].keys():
                        d[key].append(r['response'][key])
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
