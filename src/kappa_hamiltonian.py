"""
Order Creator Mechanism (OCM) - Core Physics Engine
Module: kappa_hamiltonian.py
Description: Computes the operational boundary limits at R_d = 3M, 
             Planckian density cutoffs, and metric decay rates.
"""

import numpy as np

# Physical Constants (SI Units)
G = 6.67430e-11        # Gravitational constant (m^3 kg^-1 s^-2)
C = 2.99792458e8       # Speed of light (m/s)
HBAR = 1.054571817e-34 # Reduced Planck constant (J s)

# OCM Universal Constants
L_P = np.sqrt(HBAR * G / C**3)      # Planck Length (~1.616e-35 m)
T_P = np.sqrt(HBAR * G / C**5)      # Planck Time (~5.391e-44 s)
RHO_MAX = 3 * C**2 / (8 * np.pi * G * L_P**2) # Max Density (~5.15e96 kg/m^3)
F_OCM = C**4 / G                    # Planck Tension (~1.21e44 N)


def operational_boundary_radius(M_solar: float) -> float:
    """
    Computes the R_d = 3M operational boundary for a given mass (in Solar Mass units).
    """
    M_kg = M_solar * 1.98847e30
    M_geom = G * M_kg / (C**2)
    return 3.0 * M_geom


def check_singularity_prevention(r_array: np.ndarray, M_solar: float) -> np.ndarray:
    """
    Enforces the geometric floor (r >= l_P), ensuring no divide-by-zero 
    errors or infinities occur at r = 0.
    """
    R_d = operational_boundary_radius(M_solar)
    # Floor spatial scale at l_P
    r_effective = np.maximum(r_array, L_P)
    
    # Normalized curvature metric indicator (bounded near r -> 0)
    curvature_indicator = (R_d / r_effective)**3
    return curvature_indicator


if __name__ == "__main__":
    print(f"--- OCM Framework Initialized ---")
    print(f"Planck Length Floor (l_P): {L_P:.4e} m")
    print(f"Planck Mass Density Limit (rho_max): {RHO_MAX:.4e} kg/m^3")
    print(f"Operational Boundary (R_d) for 10 M_sun BH: {operational_boundary_radius(10):.4e} m")
