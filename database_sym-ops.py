# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 11:07:48 2023

@author: Jerome Roeser
"""

import requests
from bs4 import BeautifulSoup

url_prefix = 'http://img.chem.ucl.ac.uk/sgp/large/'
url_suffix = 'az3.htm'
ops = []


for i in range(226,227):
    url = url_prefix + f'{i}{url_suffix}'
    r = requests.get(url).content
    soup = BeautifulSoup(r, features='lxml')
    pre = soup.select('pre')
    ops.append(pre[0].text.strip())