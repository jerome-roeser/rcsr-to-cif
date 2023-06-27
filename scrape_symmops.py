import requests
from bs4 import BeautifulSoup
import json

#TODO: for tetragonal and upwards replace with origin-2 (test status of a.htm sufix )
# url_prefix = 'http://img.chem.ucl.ac.uk/sgp/large/'
url_prefix = 'http://img.chem.ucl.ac.uk/sgp/medium/'

url_sufixes = ['az3.htm', 'bz3.htm', 'cz3.htm', 'dz3.htm', 'ez3.htm', 'fz3.htm']

# symmops_origin_1 = {}
# symmops_origin_2 = {}
symmops_all = {}

def scrape_all_suffixes():
    for i in range(1,231):
        key = str(i)
        symmops_all[key] = []
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
                    symmops_all[key].append({url_sufix[0] : soup.pre.text.splitlines()})
                    # symmops[key] = {url_sufix:soup.pre.text.splitlines()}
                else:
                    continue
            except ConnectionError:
                print('damn...')
        
    # symmops['227-b'] = soup.pre.text.splitlines()
    with open('symmops.json', 'w') as f:
        f.write(json.dumps(symmops_all))
        
def scrape_origin_1():
    symmops_origin_1 = {}
    for i in range(1,231):
        key = str(i)
        symmops_origin_1[key] = []
        url_sufix = 'az3.htm'
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
                symmops_origin_1[key].append({'origin-1' : soup.pre.text.splitlines()})
                # symmops[key] = {url_sufix:soup.pre.text.splitlines()}
            else:
                continue
        except ConnectionError:
            print('damn...')
        
    return symmops_origin_1
  
def scrape_origin_2(space_group__origin_2_list):
    symmops_origin_2 = {}
    for group in space_group__origin_2_list:
        key = str(group)
        symmops_origin_2[key] = []
        url_sufix = 'bz3.htm'
        # key = str(i) + '-' + url_sufix[0]
        if group < 10:
            url = url_prefix + '00' + str(group) + url_sufix
        elif group < 100:
            url = url_prefix + '0' + str(group) + url_sufix
        else:
            url = url_prefix + str(group) + url_sufix
        try: 
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content)
                symmops_origin_2[key].append({'origin-2' : soup.pre.text.splitlines()})
                # symmops[key] = {url_sufix:soup.pre.text.splitlines()}
            else:
                continue
        except ConnectionError:
            print('damn...')
    return symmops_origin_2
        
def find_origin_2_point_groups():
    space_group_list = []
    for i in range(1,231):
        url_sufix = 'a.htm'
        
        if i < 10:
            url = url_prefix + '00' + str(i) + url_sufix
        elif i < 100:
            url = url_prefix + '0' + str(i) + url_sufix
        else:
            url = url_prefix + str(i) + url_sufix
        try: 
            r = requests.get(url)
            if r.status_code == 200:
                space_group_list.append(i)
            else:
                continue
        except ConnectionError:
            print('damn...')
        
    return space_group_list

def make_hybrid_symmops():
    symmops = symmops_origin_1
    for key in symmops_origin_2.keys(): 
        symmops[key] = symmops_origin_2[key]
    with open('symmops_final.json', 'w') as f:
        f.write(json.dumps(symmops))
    return symmops
    
    
origin_2_list = find_origin_2_point_groups()
symmops_origin_1 = scrape_origin_1()
symmops_origin_2 = scrape_origin_2(origin_2_list)
symmops = make_hybrid_symmops()
