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

# check origin occurrence
def check_origin_reference():
    for i in range(1, 7):
        l = [key for key, value in symmops.items() if len(value) == i]
        print(f"there are {len(l)} space groups with {i} different origins:")
        ids = []
        for op in l:
            for j in range(i):
                ids.append([str(key) for key in symmops[op][j].keys()][0])
        element_count = Counter(ids)
        for element, count in element_count.items():
            print(f"\t{element}: {count}")
        print('\n')
        
# i want to find the space groups with origin a and d 
# and print if their sym op are equal
def check_2_origin_point_groups():
    l = [key for key, value in symmops.items() if len(value) == 2]
    first_keys = []
    second_keys = []
    for op in l: 
        key = [str(key) for key in symmops[op][1].keys()][0]
        value_a = [value for key, value in symmops[op][0].items()]
        value_d = [value for key, value in symmops[op][1].items()]
        if key == 'b' and value_d != value_a:
            point_group = SpaceGroup.from_int_number(int(op))
            # print(point_group.full_symbol)
            print(point_group.int_number, point_group.full_symbol, value_a == value_d)
            print()
        first_keys.append(([str(key) for key in symmops[op][0].keys()][0]))
        second_keys.append(([str(key) for key in symmops[op][1].keys()][0]))

check_2_origin_point_groups()