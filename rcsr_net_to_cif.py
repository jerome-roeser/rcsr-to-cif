# -*- coding: utf-8 -*-
"""
@author: Jerome Roeser
#TODO fix problem with symmops origin (default here is origin-1 whereas it is origin-2 in RCSR)
"""

import json
import pandas as pd
import re
import time
from datetime import datetime
from pymatgen.core import Lattice
from pymatgen.symmetry.groups import SpaceGroup 
from selenium.webdriver import Chrome
from textwrap import dedent


# Define the structures that need to be scraped here
nets = ['dia', 'srs', 'bor', 'ctn']
layers = []
ribbons = []
polyhedra = []


# import symmetry operations of spcace groups
with open('symmops_final.json', 'rb') as f: 
    symmops = json.load(f)


# webdriver = r"C:\Users\roeser\Downloads\install_files\chromedriver_win32"
# webdriver = r"C:/Users/Jerome Roeser/Documents/chromedriver.exe"
# webdriver = r"C:/temp/git_repos/chromedriver.exe"
# webdriver = r"W:/Documents/finxter/projects/chromedriver.exe" #change me!
#^Download from: https://chromedriver.chromium.org/

# driver = Chrome(executable_path=webdriver)
driver = Chrome()

def write_cif(filename, net, space_group_name, space_group, lattice, all_vert_info):
    """
    """
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
            # for op in symmops[str(space_group.int_number)][1:]:
            for value in symmops[str(space_group.int_number)][0].values():
                for op in value[1:]:
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
                CN = ['__', 'H', 'O', 'N', 'Si', 'P', 'Ti']
                f.write(f"\n{v[0]}  {CN[v[1]]}  {v[2]:.4f}  {v[3]:.4f}  {v[4]:.4f}")

def scrape_nets(nets):
    """ 
    """
    for i, net in enumerate(nets):
        url = 'http://rcsr.anu.edu.au/nets/'+ net
        filename = f'output/{net}.cif' 
        
        driver.get(url)
        if i == 0: 
            time.sleep(5)
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
        
        write_cif(filename, net, space_group_name, space_group, lattice, all_vert_info)

def scrape_layers(layers):
    
    """ 
    """
    for i, layer in enumerate(layers):
        url = 'https://rcsr.anu.edu.au/layers/'+ layer
        filename = f'output/{layer}.cif' 
        
        driver.get(url)
        if i == 0: 
            time.sleep(5)
        else:
            time.sleep(1)
        dfs = pd.read_html(driver.page_source)
        space_group_name = re.sub('\(|\)','', dfs[0].iloc[0,1])
        space_group = SpaceGroup(space_group_name)
        a, b, c = dfs[2].iloc[0,[0,1,2]]
        alpha, beta, gamma = dfs[2].iloc[0,[3,4,5]]
        
        
        all_vert_info = [dfs[3].loc[j,'vertex':'z'].to_list() for j in range(0, len(dfs[3]))]
        lattice = Lattice.from_parameters(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
        species = [dfs[3].loc[j,'vertex'] for j in range(0, len(dfs[3]))]
        coords = [dfs[3].loc[j,'x':'z'].to_list() for j in range(0, len(dfs[3]))]
        
        write_cif(filename, layer, space_group_name, space_group, lattice, all_vert_info)

def scrape_ribbons(ribbons):
    
    """ 
    """
    for i, ribbon in enumerate(ribbons):
        url = 'https://rcsr.anu.edu.au/ribbons/'+ ribbon
        filename = f'output/{ribbon}.cif' 
        
        driver.get(url)
        if i == 0: 
            time.sleep(5)
        else:
            time.sleep(1)
        dfs = pd.read_html(driver.page_source)
        space_group_name = re.sub('\(|\)','', dfs[0].iloc[0,1])
        space_group = SpaceGroup(space_group_name)
        a, b, c = dfs[2].iloc[0,[0,1,2]]
        alpha, beta, gamma = dfs[2].iloc[0,[3,4,5]]
        
        
        all_vert_info = [dfs[3].loc[j,'vertex':'z'].to_list() for j in range(0, len(dfs[3]))]
        lattice = Lattice.from_parameters(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
        species = [dfs[3].loc[j,'vertex'] for j in range(0, len(dfs[3]))]
        coords = [dfs[3].loc[j,'x':'z'].to_list() for j in range(0, len(dfs[3]))]
        
        write_cif(filename, ribbon, space_group_name, space_group, lattice, all_vert_info)
        
def scrape_polyhedra(polyhedra):
    
    """ 
    """
    for i, polyhedron in enumerate(polyhedra):
        url = 'https://rcsr.anu.edu.au/polyhedra/'+ polyhedron
        filename = f'output/{polyhedron}.cif' 
        
        driver.get(url)
        if i == 0: 
            time.sleep(5)
        else:
            time.sleep(1)
        dfs = pd.read_html(driver.page_source)
        space_group_name = re.sub('\(|\)','', dfs[0].iloc[0,3])
        space_group = SpaceGroup(space_group_name)
        a, b, c = 20, 20, 20
        alpha, beta, gamma = 90, 90, 90
        
        
        all_vert_info = [dfs[3].loc[j,'vertex':'z'].to_list() for j in range(0, len(dfs[3]))]
        lattice = Lattice.from_parameters(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
        species = [dfs[3].loc[j,'vertex'] for j in range(0, len(dfs[3]))]
        coords = [dfs[3].loc[j,'x':'z'].to_list() for j in range(0, len(dfs[3]))]
        
        write_cif(filename, polyhedron, space_group_name, space_group, lattice, all_vert_info)

scrape_polyhedra(polyhedra)
scrape_ribbons(ribbons)
scrape_layers(layers)
scrape_nets(nets)

driver.close()
print('Done!')