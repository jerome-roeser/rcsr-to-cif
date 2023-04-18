from CifFile import ReadCif
import pandas as pd




filename = 'output\PD-29-14_Pawley.cif'
template = 'output\_template.xlsx'


with open(filename, 'r') as f:
    cif = ReadCif(f)
    
df = pd.read_excel(template)
print(df)

data = cif.visible_keys[0]
lattice_parameter = []
symmetry = f"Space Group: {cif[data]['_symmetry_space_group_name_H-M']} ({cif[data]['_symmetry_Int_Tables_number']})"
crystal_system = cif[data]['_symmetry_cell_setting']
cell_lenghts = f"a = {cif[data]['_cell_length_a']} Å, b = {cif[data]['_cell_length_b']} Å, c = {cif[data]['_cell_length_c']} Å"
cell_angles = f"a = b = {90.00} °, g = {120.00} °"
 
df_1 = pd.DataFrame({data: [symmetry, cell_lenghts, cell_angles]})   
df_2 = pd.DataFrame({'Atom label': cif[data]['_atom_site_label'],
                       'Atom type' : cif[data]['_atom_site_type_symbol'],
                       'x' : cif[data]['_atom_site_fract_x'],
                       'y': cif[data]['_atom_site_fract_y'],
                       'z': cif[data]['_atom_site_fract_z']
                       })

# with open(filename, 'r') as f:
#     a = f.readlines()