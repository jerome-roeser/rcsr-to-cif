from CifFile import ReadCif
import pandas as pd
from pathlib import Path

path = Path('output/')
for p in path.iterdir():
    if p.suffix == '.cif':
        print(f'{p.name} -> {p.stem}')
        with open(p, 'r') as f:
            cif = ReadCif(f)
            
        data = cif.visible_keys[0]
        lattice_parameter = []
        symmetry = f"Space Group: {cif[data]['_symmetry_space_group_name_H-M']} ({cif[data]['_symmetry_Int_Tables_number']})"
        crystal_system = cif[data]['_symmetry_cell_setting']
        cell_lenghts = f"a = {cif[data]['_cell_length_a']} Å, b = {cif[data]['_cell_length_b']} Å, c = {cif[data]['_cell_length_c']} Å"
        cell_angles = f"a = b = {90.00} °, g = {120.00} °"
        
        df_1 = pd.DataFrame({p.stem: [symmetry, cell_lenghts, cell_angles]})   
        df_2 = pd.DataFrame({'Atom label': cif[data]['_atom_site_label'],
                            'Atom type' : cif[data]['_atom_site_type_symbol'],
                            'x' : cif[data]['_atom_site_fract_x'],
                            'y': cif[data]['_atom_site_fract_y'],
                            'z': cif[data]['_atom_site_fract_z']
                            })
        final = pd.concat([df_1,df_2])
        final.to_excel(f'output/{p.stem}.xlsx')
        p.stem
        


# filename = 'output\PD-29-14_Pawley.cif'
# template = 'output\_template.xlsx'


        
# with open(filename, 'r') as f:
#     a = f.readlines()