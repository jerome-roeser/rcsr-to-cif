from CifFile import ReadCif
import pandas as pd
from pathlib import Path


def convert_cif_to_excel(file):
    with open(file, 'r') as f:
            cif = ReadCif(f)
    
    p = Path(file)        
    data = cif.visible_keys[0]
    data_name = p.stem
    symmetry = f"Space Group: {cif[data]['_symmetry_space_group_name_H-M']} ({cif[data]['_symmetry_Int_Tables_number']})"
    crystal_system = cif[data]['_symmetry_cell_setting']
    cell_lenghts = f"a = {cif[data]['_cell_length_a']} Å, b = {cif[data]['_cell_length_b']} Å, c = {cif[data]['_cell_length_c']} Å"
    cell_angles = f"\u03B1 = \u03B2 = {90.00} °, \u03B3 = {120.00} °"
    
    header = pd.MultiIndex.from_arrays([[data_name, '', '', '', ''], 
                                        [symmetry, '', '', '', ''],
                                        [cell_lenghts, '', '', '', ''],
                                        [cell_angles, '', '', '', ''],
                                        ['Atom label', 'Atom type', 'x', 'y', 'z']])
    df_2 = pd.DataFrame({'Atom label': cif[data]['_atom_site_label'],
                        'Atom type' : cif[data]['_atom_site_type_symbol'],
                        'x' : cif[data]['_atom_site_fract_x'],
                        'y': cif[data]['_atom_site_fract_y'],
                        'z': cif[data]['_atom_site_fract_z']
                        })
    df_2.columns = header
    df_2.to_excel(f'output/{data_name}.xlsx')    

path = Path('output/')
for p in path.iterdir():
    if p.suffix == '.cif':
        print(f'{p.name} -> {p.stem}')
        convert_cif_to_excel(p)
        
