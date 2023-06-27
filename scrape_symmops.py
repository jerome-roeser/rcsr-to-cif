import requests
from bs4 import BeautifulSoup
import json

# url_prefix = 'http://img.chem.ucl.ac.uk/sgp/large/'
url_prefix = 'http://img.chem.ucl.ac.uk/sgp/medium/'

url_sufixes = ['az3.htm', 'bz3.htm', 'cz3.htm', 'dz3.htm', 'ez3.htm', 'fz3.htm']
symmops = {}
symmops_a = {}

for i in range(1,231):
    key = str(i)
    symmops_a[key] = []
    for url_sufix in url_sufixes:
        # key = str(i) + '-' + url_sufix[0]
        if i < 10:
            url = url_prefix + '00' + str(i) + url_sufix
        elif i < 100:
            url = url_prefix + '0' + str(i) + url_sufix
        else:
            url = url_prefix + str(i) + url_sufix
        try: 
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content)
                symmops_a[key].append({url_sufix[0] : soup.pre.text.splitlines()})
                # symmops[key] = {url_sufix:soup.pre.text.splitlines()}
            else:
                continue
        except ConnectionError:
            print('damn...')
    
# symmops['227-b'] = soup.pre.text.splitlines()
with open('symmops.json', 'w') as f:
    f.write(json.dumps(symmops_a))