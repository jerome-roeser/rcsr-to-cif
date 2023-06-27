import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import time
from datetime import datetime
from pymatgen.core import Lattice
from pymatgen.symmetry.groups import SpaceGroup 
from selenium.webdriver import Chrome
from textwrap import dedent
from collections import Counter

# import symmetry operations of spcace groups
with open('symmops.json', 'rb') as f: 
    symmops = json.load(f)

for i in range(0, 7):
    l = [key for key, value in symmops.items() if len(value) == i]
    print(len(l), l)
    ids = []
    for op in l:
        for j in range(i):
            ids.append([str(key) for key in symmops[op][j].keys()][0])
    element_count = Counter(ids)
    for element, count in element_count.items():
        print(f"{element}: {count}")
    