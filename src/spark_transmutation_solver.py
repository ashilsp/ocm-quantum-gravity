"""
Order Creator Mechanism (OCM) - Spark & Transmutation Solver
Module: spark_transmutation_solver.py
Description: Solves terminal quantum state decay (n=1 -> |0>), local Rd ignition 
             temperatures for stellar cores, and magnetar magnetic flux compression.
"""

import numpy as np

# Physical Constants (SI)
G = 6.67430e-11          # m^3 kg^-1 s^-2
C = 2.99792458e8         # m/s
K_B = 1.380649e-23       # J/K
M_P = 2.176434e-8        # Planck Mass in kg
E_P = M_P * (C**2)       # Planck Energy in Joules
M_PROTON = 1.6726219e-27 # kg


def discrete_energy_level(n: int) -> float:
    """
    Computes quantized PBH energy level E_n = -E_P / (2 * n^2).
    Ground state n = 1 gives -E_P / 2.
    """
    if n < 1:
        raise ValueError("Principal quantum number n must be >= 1.")
    return -E_P / (2.0 * (n**2))


def rd_ignition_temperature(M_pbh_kg: float, R_d: float) -> float:
    """
    Calculates local thermal kinetic energy spike temperature T_{R_d}
    at the R_d boundary inside a Carbon-Oxygen White Dwarf core.
    """
    # Mean molecular weight mu ~ 2 for fully ionized C-O core
    mu = 2.0
    term = (G * M_pbh_kg * (C**2) / (R_d**3))**0.5
    T_rd = (mu * M_PROTON / K_B) * term
    return float(T_rd)


def compressed_magnetic_field(B_surface: float, R_NS: float, R_d: float) -> float:
    """
    Calculates magnetic flux compression B_{R_d} = B_surface * (R_NS / R_d)^2
    driving Pulsar-to-Magnetar transmutation.
    """
    return B_surface * ((R_NS / R_d)**2)


if __name__ == "__main__":
    print("--- OCM Sparking & Transmutation Solver Initialized ---")
    
    # Ground state energy
    E_1 = discrete_energy_level(1)
    print(f"Ground State Energy (n=1): {E_1:.4e} Joules")
    
    # Thermonuclear spark test (M_PBH ~ 1e15 kg, R_d = 3M)
    M_test = 1.0e15
    R_d_test = 3.0 * (G * M_test / (C**2))
    T_spark = rd_ignition_temperature(M_test, R_d_test)
    print(f"Local R_d Temperature: {T_spark:.4e} K (Ignition Threshold T_ign ~ 1e9 K)")
    
    # Magnetar transmutation check
    B_comp = compressed_magnetic_field(1.0e12, 10000.0, 1.0e-2)
    print(f"Compressed Magnetic Field B_Rd: {B_comp:.4e} Gauss (Magnetar regime > 1e15 G)")
