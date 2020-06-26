import openmc
import openmc.model
import numpy as np

model = openmc.model.Model()

###############################################################################
# Materials

fuel_31 = openmc.Material(name='UO2 fuel at 3.1% wt enrichment')
fuel_31.set_density('atom/b-cm', 6.86463E-02)
fuel_31.add_nuclide('U234', 6.11864E-06)
fuel_31.add_nuclide('U235', 7.18132E-04)
fuel_31.add_nuclide('U236', 3.29861E-06)
fuel_31.add_nuclide('U238', 2.21546E-02)
fuel_31.add_nuclide('O16' , 4.57642E-02)

helium = openmc.Material(name='Helium for gap')
helium.set_density('atom/b-cm',  2.68714E-5)
helium.add_nuclide('He4', 2.68714E-5)

zirc4 = openmc.Material(name='Zircaloy 4')
zirc4.set_density('atom/b-cm', 4.33818E-02)
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
zirc4.add_nuclide('Fe54', 8.68307E-06)
zirc4.add_nuclide('Fe56', 1.36306E-04)
zirc4.add_nuclide('Fe57', 1.36306E-04)
zirc4.add_nuclide('Fe58', 4.18926E-07)
zirc4.add_nuclide('Cr50', 3.30121E-06)
zirc4.add_nuclide('Cr52', 6.36606E-05)
zirc4.add_nuclide('Cr53', 7.21860E-06)
zirc4.add_nuclide('Cr54', 1.79686E-06)
zirc4.add_nuclide('Hf174', 3.54138E-09)
zirc4.add_nuclide('Hf176', 1.16423E-07)
zirc4.add_nuclide('Hf177', 4.11686E-07)
zirc4.add_nuclide('Hf178', 6.03806E-07)
zirc4.add_nuclide('Hf179', 3.01460E-07)
zirc4.add_nuclide('Hf180', 7.76449E-07)

water_600 = openmc.Material(name='Borated water at 600 K with 1300 ppm')
water_600.set_density('atom/b-cm', 7.01765E-02)
water_600.add_nuclide('O16', 2.33753E-02)
water_600.add_nuclide('H1', 4.67505E-02)
water_600.add_nuclide('B10', 1.00874E-05)
water_600.add_nuclide('B11', 4.06030E-05)
water_600.add_s_alpha_beta('c_H_in_H2O')

###############################################################################
# Geometry

# Instantiate zCylinder surfaces
fuel_or = openmc.ZCylinder(r=0.4096, name='Fuel OR')
clad_ir = openmc.ZCylinder(r=0.4180, name='Clad IR')
clad_or = openmc.ZCylinder(r=0.4750, name='Clad OR')
gt_ir   = openmc.ZCylinder(r=0.5610, name='Guide Tube IR')
gt_or   = openmc.ZCylinder(r=0.6020, name='Guide Tube OR')

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

# Instantiate a Lattice
lattice_2a = openmc.RectLattice()
lattice_2a.lower_left = [-10.71, -10.71]
lattice_2a.pitch      = [1.2600, 1.2600]
                          # 1        2       3      4       5        6       7       8       9       10     11       12      13     14      15      16      17
lattice_2a.universes  = [[u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 1
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 2
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 3
                         [u_fuel, u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_fuel], # 4
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 5
                         [u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel], # 6
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 7
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 8
                         [u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel], # 9
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 10
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 11
                         [u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel], # 12
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 13
                         [u_fuel, u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_fuel], # 14
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_gt  , u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 15
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel], # 16
                         [u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel, u_fuel]] # 17

lat_inner = openmc.Cell(
    name='assembly inside',
    fill=lattice_2a,
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

# Instantiate a Settings object, set all runtime parameters, and export to XML
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
    openmc.MaterialFilter([fuel_31, helium, zirc4, water_600]),
    openmc.ParticleFilter(['neutron', 'photon', 'electron', 'positron'])
]
tally.scores = ['fission', 'heating-local']
model.tallies = openmc.Tallies([tally])

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
    total_heating = heating['mean'].sum()
    fission = df[df.score == 'fission']['mean'].sum()
    return total_heating / fission * 1e-6

print('Neutron only')
Ed = mev_per_fission(df_neutron, 'heating-local')
print(f'{Ed:.2f} MeV/fission')
print(df_neutron.to_string())
print()

print('Coupled neutron-photon')
Ed = mev_per_fission(df_neutron_photon, 'heating')
print(f'{Ed:.2f} MeV/fission')

heating = df_neutron_photon[df_neutron_photon.score == 'heating'].copy()
heating['percent'] = heating['mean'] / heating['mean'].sum()
print(heating.to_string())
print(heating.groupby('material').sum())
