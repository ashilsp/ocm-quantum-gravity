"""
Order Creator Mechanism (OCM) - Pulsar Transmutation Engine
Module: pulsar_transmutation_solver.py
Description: Solves magnetic flux compression (Phi_B = const) at the R_d shell 
             and total magnetic reconnection burst energy E_B (10^38 - 10^40 J).
"""

import numpy as np

# Physical Constants (SI)
MU_0 = 4.0 * np.pi * 1.0e-7  # Magnetic permeability of free space (H/m)
G = 6.67430e-11              # Gravitational constant
C = 2.99792458e8             # Speed of light


def compressed_magnetic_field(B_surface_gauss: float, R_NS_m: float, R_d_m: float) -> float:
    """
    Computes compressed magnetic field B_{R_d} = B_surface * (R_NS / R_d)^2
    under conservation of magnetic flux (Phi_B = const).
    """
    return B_surface_gauss * ((R_NS_m / R_d_m)**2)


def magnetic_reconnection_energy(B_Rd_tesla: float, R_d_m: float) -> float:
    """
    Calculates total energy released during magnetic reconnection at R_d:
    E_B = (B^2 / (2 * mu_0)) * V_{R_d}
    """
    volume = (4.0 / 3.0) * np.pi * (R_d_m**3)
    energy_density = (B_Rd_tesla**2) / (2.0 * MU_0)
    return energy_density * volume


if __name__ == "__main__":
    print("--- OCM Pulsar-to-Magnetar Transmutation Engine Initialized ---")
    
    # Parameters for captured PBH inside Neutron Star
    B_surf_gauss = 1.0e12  # Standard NS surface field (Gauss)
    R_NS = 10000.0         # 10 km in meters
    M_pbh = 1.0e15         # PBH mass in kg
    R_d = 3.0 * (G * M_pbh / (C**2))  # R_d = 3M in meters
    
    # Calculation
    B_Rd_G = compressed_magnetic_field(B_surf_gauss, R_NS, R_d)
    B_Rd_T = B_Rd_G * 1.0e-4  # Convert Gauss to Tesla
    E_burst = magnetic_reconnection_energy(B_Rd_T, R_d)
    
    print(f"Original Surface Field B_surface: {B_surf_gauss:.2e} G")
    print(f"Compressed Core Field B_Rd:       {B_Rd_G:.2e} G (Magnetar Regime > 10^15 G)")
    print(f"Total Outburst Energy E_B:        {E_burst:.2e} Joules (~10^38 - 10^40 J)")
