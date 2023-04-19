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
        data_name = p.stem
        symmetry = f"Space Group: {cif[data]['_symmetry_space_group_name_H-M']} ({cif[data]['_symmetry_Int_Tables_number']})"
        crystal_system = cif[data]['_symmetry_cell_setting']
        cell_lenghts = f"a = {cif[data]['_cell_length_a']} Å, b = {cif[data]['_cell_length_b']} Å, c = {cif[data]['_cell_length_c']} Å"
        cell_angles = f"a = b = {90.00} °, g = {120.00} °"
        
        # df_1 = pd.DataFrame({data_name: [symmetry, cell_lenghts, cell_angles]}) 
        info =f"""
        {symmetry}
        {cell_lenghts}
        {cell_angles}
        """
        
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
        # template_file = pd.read_excel('output\_template.xlsx')
        df_2.columns = header
        # final = pd.concat([df_1,df_2])
        # final.to_excel(f'output/{data_name}.xlsx')
        df_2.to_excel(f'output/{data_name}.xlsx')
        
        


# filename = 'output\PD-29-14_Pawley.cif'
# template = 'output\_template.xlsx'


        
# with open(filename, 'r') as f:
#     a = f.readlines()