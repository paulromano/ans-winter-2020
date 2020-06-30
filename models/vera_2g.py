import openmc
import numpy as np
from uncertainties import unumpy as unp

model = openmc.model.Model()

###############################################################################
# Materials

fuel_31 = openmc.Material(name='UO2 fuel at 3.1% wt enrichment')
fuel_31.add_nuclide('U234', 6.11864E-06)
fuel_31.add_nuclide('U235', 7.18132E-04)
fuel_31.add_nuclide('U236', 3.29861E-06)
fuel_31.add_nuclide('U238', 2.21546E-02)
fuel_31.add_nuclide('O16', 4.57642E-02)

helium = openmc.Material(name='Helium for gap')
helium.add_nuclide('He4', 2.68714E-5)

zirc4 = openmc.Material(name='Zircaloy 4')
zirc4.add_nuclide('Cr50', 3.30121E-06)
zirc4.add_nuclide('Cr52', 6.36606E-05)
zirc4.add_nuclide('Cr53', 7.21860E-06)
zirc4.add_nuclide('Cr54', 1.79686E-06)
zirc4.add_nuclide('Fe54', 8.68307E-06)
zirc4.add_nuclide('Fe56', 1.36306E-04)
zirc4.add_nuclide('Fe57', 3.14789E-06)
zirc4.add_nuclide('Fe58', 4.18926E-07)
zirc4.add_nuclide('Zr90', 2.18865E-02)
zirc4.add_nuclide('Zr91', 4.77292E-03)
zirc4.add_nuclide('Zr92', 7.29551E-03)
zirc4.add_nuclide('Zr94', 7.39335E-03)
zirc4.add_nuclide('Zr96', 1.19110E-03)
zirc4.add_nuclide('Sn112', 4.68066E-06)
zirc4.add_nuclide('Sn114', 3.18478E-06)
zirc4.add_nuclide('Sn115', 1.64064E-06)
zirc4.add_nuclide('Sn116', 7.01616E-05)
zirc4.add_nuclide('Sn117', 3.70592E-05)
zirc4.add_nuclide('Sn118', 1.16872E-04)
zirc4.add_nuclide('Sn119', 4.14504E-05)
zirc4.add_nuclide('Sn120', 1.57212E-04)
zirc4.add_nuclide('Sn122', 2.23417E-05)
zirc4.add_nuclide('Sn124', 2.79392E-05)
zirc4.add_nuclide('Hf174', 3.54138E-09)
zirc4.add_nuclide('Hf176', 1.16423E-07)
zirc4.add_nuclide('Hf177', 4.11686E-07)
zirc4.add_nuclide('Hf178', 6.03806E-07)
zirc4.add_nuclide('Hf179', 3.01460E-07)
zirc4.add_nuclide('Hf180', 7.76449E-07)

water_600 = openmc.Material(name='Borated water at 600 K with 1300 ppm')
water_600.add_nuclide('O16', 2.48112E-02)
water_600.add_nuclide('H1', 4.96224E-02)
water_600.add_nuclide('B10', 1.07070E-05)
water_600.add_nuclide('B11', 3.30971E-05)
water_600.add_s_alpha_beta('c_H_in_H2O')

ss304 = openmc.Material(name='SS304')
ss304.add_element('C', 3.20895E-04)
ss304.add_nuclide('Si28', 1.58197E-03)
ss304.add_nuclide('Si29', 8.03653E-05)
ss304.add_nuclide('Si30', 5.30394E-05)
ss304.add_nuclide('P31', 6.99938E-05)
ss304.add_nuclide('Cr50', 7.64915E-04)
ss304.add_nuclide('Cr52', 1.47506E-02)
ss304.add_nuclide('Cr53', 1.67260E-03)
ss304.add_nuclide('Cr54', 4.16346E-04)
ss304.add_nuclide('Mn55', 1.75387E-03)
ss304.add_nuclide('Fe54', 3.44776E-03)
ss304.add_nuclide('Fe56', 5.41225E-02)
ss304.add_nuclide('Fe57', 1.24992E-03)
ss304.add_nuclide('Fe58', 1.66342E-04)
ss304.add_nuclide('Ni58', 5.30854E-03)
ss304.add_nuclide('Ni60', 2.04484E-03)
ss304.add_nuclide('Ni61', 8.88879E-05)
ss304.add_nuclide('Ni62', 2.83413E-04)
ss304.add_nuclide('Ni64', 7.21770E-05)

agincd = openmc.Material(name='Ag-In-Cd')
agincd.add_nuclide('Ag107', 2.36159E-02)
agincd.add_nuclide('Ag109', 2.19403E-02)
agincd.add_nuclide('Cd106', 3.41523E-05)
agincd.add_nuclide('Cd108', 2.43165E-05)
agincd.add_nuclide('Cd110', 3.41250E-04)
agincd.add_nuclide('Cd111', 3.49720E-04)
agincd.add_nuclide('Cd112', 6.59276E-04)
agincd.add_nuclide('Cd113', 3.33873E-04)
agincd.add_nuclide('Cd114', 7.84957E-04)
agincd.add_nuclide('Cd116', 2.04641E-04)
agincd.add_nuclide('In113', 3.44262E-04)
agincd.add_nuclide('In115', 7.68050E-03)

###############################################################################
# Geometry

# Instantiate zCylinder surfaces
fuel_or = openmc.ZCylinder(r=0.4096, name='Fuel OR')
clad_ir = openmc.ZCylinder(r=0.4180, name='Clad IR')
clad_or = openmc.ZCylinder(r=0.4750, name='Clad OR')
gt_ir   = openmc.ZCylinder(r=0.5610, name='Guide Tube IR')
gt_or   = openmc.ZCylinder(r=0.6020, name='Guide Tube OR')
aic_ir      = openmc.ZCylinder(r=0.3820, name='AIC Radius')
aic_clad_ir = openmc.ZCylinder(r=0.3860, name='AIC Clad IR')
aic_clad_or = openmc.ZCylinder(r=0.4840, name='AIC Clad OR')

assembly_left   = openmc.XPlane(x0=-10.75, boundary_type='reflective')
assembly_right  = openmc.XPlane(x0= 10.75, boundary_type='reflective')
assembly_back   = openmc.YPlane(y0=-10.75, boundary_type='reflective')
assembly_front  = openmc.YPlane(y0= 10.75, boundary_type='reflective')
assembly_bottom = openmc.ZPlane(z0=-200.0, boundary_type='reflective')
assembly_top    = openmc.ZPlane(z0= 200.0, boundary_type='reflective')

lattice_left    = openmc.XPlane(x0=-10.71)
lattice_right   = openmc.XPlane(x0= 10.71)
lattice_back    = openmc.YPlane(y0=-10.71)
lattice_front   = openmc.YPlane(y0= 10.71)
lattice_bottom  = openmc.ZPlane(z0=-200.0)
lattice_top     = openmc.ZPlane(z0= 200.0)

# fuel rod cell with 3.6 w/o
u_fuel = openmc.model.pin([fuel_or, clad_ir, clad_or], [fuel_31, helium, zirc4, water_600])

# guide tube
u_gt = openmc.model.pin([gt_ir, gt_or], [water_600, zirc4, water_600])

# Ag-In-Cd (AIC) control rod
u_aic = openmc.model.pin(
    surfaces=[aic_ir, aic_clad_ir, aic_clad_or, gt_ir, gt_or],
    items=[agincd, helium, ss304, water_600, zirc4, water_600]
)

lattice_2g = openmc.RectLattice(lattice_id=4)
lattice_2g.lower_left = [-10.71, -10.71]
lattice_2g.pitch      = [1.2600, 1.2600]
                          # 1        2       3      4       5        6       7       8       9       10     11       12      13     14      15      16      17
lattice_2g.universes  = [ [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 1
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 2
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 3
                          [u_fuel, u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_fuel], # 4
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 5
                          [u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel], # 6
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 7
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 8
                          [u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel], # 9
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 10
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 11
                          [u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel], # 12
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 13
                          [u_fuel, u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_fuel], # 14
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_aic , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 15
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 16
                          [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel] ] # 17

lat_inner = openmc.Cell(
    name='assembly inside',
    fill=lattice_2g,
    region=+lattice_left  & -lattice_right  & +lattice_back  & -lattice_front
)
lat_outer = openmc.Cell(
    name='assembly outer',
    fill=water_600,
    region=-lattice_left  | +lattice_right  | -lattice_back  | +lattice_front
)

# fill assembly with cells
u_assembly_2a = openmc.Universe(name='infinity assembly universe 2a')
u_assembly_2a.add_cells([lat_inner, lat_outer])

# lattice of whole core
lattice_core = openmc.RectLattice()
lattice_core.lower_left = [-10.75, -10.75]
lattice_core.pitch      = [21.50, 21.50]
lattice_core.universes  = [[u_assembly_2a]] # 1-by-1 whole core

# Fill cell with the lattice
full_model = openmc.Cell(
    name='full core',
    fill=lattice_core,
    region=+assembly_left & -assembly_right & +assembly_back & -assembly_front
)

model.geometry = openmc.Geometry([full_model])

###############################################################################
# Settings

model.settings.batches = 40
model.settings.inactive = 20
model.settings.particles = 1000
model.settings.temperature = {
	'default' : 600.0,
}

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-10.75, -10.75, -1, 10.75, 10.75, 1]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
model.settings.source = openmc.source.Source(space=uniform_dist)

entropy_mesh = openmc.RegularMesh()
entropy_mesh.lower_left  = [-10.71, -10.71]
entropy_mesh.upper_right = [ 10.71,  10.71]
entropy_mesh.dimension = [10, 10]
model.settings.entropy_mesh = entropy_mesh

###############################################################################
# Analysis

# Get heating in a neutron-only calculation
tally = openmc.Tally(name='heating')
tally.filters = [
    openmc.MaterialFilter([fuel_31, helium, zirc4, ss304, agincd, water_600]),
    openmc.ParticleFilter(['neutron', 'photon', 'electron', 'positron'])
]
tally.scores = ['fission', 'heating-local']

total_tally = openmc.Tally(name='total')
total_tally.scores = ['fission', 'heating-local', 'heating']

model.tallies = openmc.Tallies([tally, total_tally])

sp_path = model.run()
with openmc.StatePoint(sp_path) as sp:
    t = sp.get_tally(name='heating')
    df_neutron = t.get_pandas_dataframe()

# Get heating in a coupled neutron-photon calculation
model.settings.photon_transport = True
model.settings.delayed_photon_scaling = True
model.tallies[0].scores = ['fission', 'heating']
sp_path = model.run()
with openmc.StatePoint(sp_path) as sp:
    t = sp.get_tally(name='heating')
    df_neutron_photon = t.get_pandas_dataframe()

def mev_per_fission(df, score):
    heating = df[df.score == score]
    total_heating = unp.uarray(heating['mean'], heating['std. dev.']).sum()
    fission = df[df.score == 'fission']
    total_fission = unp.uarray(fission['mean'], fission['std. dev.']).sum()
    return total_heating / total_fission * 1e-6

print('Neutron only')
Ed = mev_per_fission(df_neutron, 'heating-local')
print(f'{Ed:.2f} MeV/fission')
print(df_neutron.to_string())
print()

print('Coupled neutron-photon')
Ed = mev_per_fission(df_neutron_photon, 'heating')
print(f'{Ed:.2f} MeV/fission')

heating = df_neutron_photon[df_neutron_photon.score == 'heating'].copy()
print(heating.to_string())

percent = unp.uarray(heating['mean'], heating['std. dev.'])
percent /= percent.sum()
percent_fuel = percent[:4].sum()
percent_clad = percent[8:12].sum()
percent_poison = percent[16:20].sum()
percent_coolant = percent[20:].sum()
print(f'Fuel: {percent_fuel*100}')
print(f'Clad: {percent_clad*100}')
print(f'Coolant: {percent_coolant*100}')
print(f'Poison: {percent_poison*100}')
