using PolaronMobility
using DelimitedFiles

# Physical constants
const hbar = const ħ = 1.05457162825e-34;                   # kg m2 / s
const eV = const q = const ElectronVolt = 1.602176487e-19;  # kg m2 / s2
const me=MassElectron = 9.10938188e-31;                     # kg
const Boltzmann = const kB =  1.3806504e-23;                # kg m2 / K s2
const ε_0 = 8.854E-12                       #Units: C2N−1m−2, permittivity of free space
const cm1=2.997e10                                          # cm-1 to Herz

input_data = readdlm("../../processed_data/mobility_input.csv", ',', skipstart=1)

mobilities = []
for d in eachrow(input_data)
    println(d)
    # Set variables
    T = 300
    eps_inf = d[1]
    eps_total = d[2]
    omega = d[3]*cm1
    n_mass = d[4]
    p_mass = d[5]

    # Calculate mobility_electron and mobility_hole
    mobility_electron = polaronmobility(T, eps_inf, eps_total, omega, n_mass)
    mobility_hole = polaronmobility(T, eps_inf, eps_total, omega, p_mass)
    push!(mobilities, [mobility_electron.Hμ[1], mobility_hole.Hμ[1]])

end

# Tidy
mobilities = hcat(mobilities...)
mobilities = permutedims(mobilities)
# Write to file
writedlm("../../processed_data/mobility_output.csv", mobilities, ",")
