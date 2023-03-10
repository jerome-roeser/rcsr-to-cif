# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:11:13 2023

@author: Jerome Roeser
"""

import json
import pandas as pd
import re
import time
from datetime import datetime
from pymatgen.core import Lattice, Structure
from pymatgen.symmetry.groups import SpaceGroup 
from selenium.webdriver import Chrome
from textwrap import dedent
# from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
# from pymatgen.io.cif import CifWriter



# webdriver = r"C:\Users\roeser\Downloads\install_files\chromedriver_win32"
# webdriver = r"C:/Users/Jerome Roeser/Documents/chromedriver.exe"
webdriver = r"W:/Documents/finxter/projects/chromedriver.exe" #change me!
#^Download from: https://chromedriver.chromium.org/

driver = Chrome(executable_path=webdriver)
nets = ['boe', 'etq', 'kgk', 'oge', 'dgn', 'kgt', 'bpu', 'bpw']

with open('symmops.json', 'rb') as f: 
    symmops = json.load(f)

for i, net in enumerate(nets):
    url = 'http://rcsr.anu.edu.au/nets/'+ net
    filename = f'output/{net}.cif' 
    
    driver.get(url)
    if i == 0: 
        time.sleep(10)
    else:
        time.sleep(1)
    dfs = pd.read_html(driver.page_source)
    space_group_name = re.sub('\(|\)','', dfs[0].iloc[0,1])
    space_group = SpaceGroup(space_group_name)
    a, b, c = dfs[1].iloc[0,[0,1,2]]
    alpha, beta, gamma = dfs[1].iloc[0,[3,4,5]]
    
    
    all_vert_info = [dfs[2].loc[j,'vertex':'z'].to_list() for j in range(0, len(dfs[2]))]
    lattice = Lattice.from_parameters(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
    species = [dfs[2].loc[j,'vertex'] for j in range(0, len(dfs[2]))]
    coords = [dfs[2].loc[j,'x':'z'].to_list() for j in range(0, len(dfs[2]))]
    
    structure = Structure.from_spacegroup(space_group_name, lattice, species, coords)
    # structure.to(filename=filename)
    # w = CifWriter(structure)
    # w.write_file('mystructure.cif')
    
    with open(filename, 'w') as f: 
        header =f"""
                data_{net}
                _audit_creation_date              {datetime.today().date()}
                _audit_creation_method            'script-jr'
                _symmetry_space_group_name_H-M    '{space_group_name}'
                _symmetry_Int_Tables_number       {space_group.int_number}
                _symmetry_cell_setting            {space_group.crystal_system}
                loop_
                _symmetry_equiv_pos_as_xyz
                """
        f.write(dedent(header).strip())
        for op in symmops[str(space_group.int_number)][1:]:
        # for op in symmops['227-b'][1:]:
            s = re.sub(r'\s', '', op) 
            f.write(f"\n\t{s}")
        f.write('\n')
        middle =f"""
                
                _cell_length_a                    {lattice.a}
                _cell_length_b                    {lattice.b}
                _cell_length_c                    {lattice.c}
                _cell_angle_alpha                 {lattice.alpha}
                _cell_angle_beta                  {lattice.beta}
                _cell_angle_gamma                 {lattice.gamma}
                loop_
                _atom_site_label
                _atom_site_type_symbol
                _atom_site_fract_x
                _atom_site_fract_y
                _atom_site_fract_z
                # _atom_site_U_iso_or_equiv
                # _atom_site_adp_type
                # _atom_site_occupancy
                """
        f.write(dedent(middle).strip())
        for v in all_vert_info:
            CN = ['__', 'H', 'O', 'N', 'Si', '', 'Ti']
            f.write(f"\n{v[0]}  {CN[v[1]]}  {v[2]:.4f}  {v[3]:.4f}  {v[4]:.4f}")

driver.close()
print('Done!')