#VK audience reach counter

Gets vk audience size info, returns its size, saves data to final result

## Installation

1. Run in terminal:

`mkdir get_vk_stats
cd !$
git init
git clone https://github.com/tresbon/get_ads_stats`

2. Prepare a ads.csv file like this or remove with another file with the same name:


`client_id,account_id,ad_id
12345,5433231,65345234`


Order is not important, but column names must be the same!
If you use not an agency account, client_id and account_id must be the same

3. Paste your vk.API token to token.csv
if you don't have one paste link to browser
https://oauth.vk.com/authorize?client_id=6003800&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=ads,offline&response_type=token&v=5.103
take token and save it to the file

4. In terminal run _(Python3 must be installed!)_

`python3 get_bets.py`


