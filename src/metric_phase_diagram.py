"""
Order Creator Mechanism (OCM) - Supplementary Section S5.2
Module: metric_phase_diagram.py
Description: Implements Algorithm 2 (Metric Phase Boundary Mapper).
             Maps local Tolman temperature and metric pressure to construct the
             P-T phase diagram distinguishing 'Spacetime Ice' (GR) from 'Spacetime Steam' (Oloid core).
"""

import numpy as np

# Physical Constants
G = 6.67430e-11           # m^3 kg^-1 s^-2
C = 2.99792458e8          # m/s
HBAR = 1.054571817e-34     # J s
M_SUN = 1.989e30          # kg


def compute_metric_profiles(r: np.ndarray, M: float, eta_0: float = 1.0e-3, kappa: float = 1.0) -> tuple:
    """
    Computes local Tolman temperature T_metric(r) and metric continuum pressure P_metric(r).
    """
    R_s = 2.0 * G * M / (C**2)
    f_r = 1.0 - (R_s / r)
    f_r = np.maximum(f_r, 1e-6)  # Regularization
    
    # Tolman Local Temperature
    T_hawking = (HBAR * (C**3)) / (8.0 * np.pi * G * M)
    T_metric = T_hawking / np.sqrt(f_r)
    
    # Metric Continuum Pressure Profile
    P_metric = (3.0 * (eta_0**2) / kappa) * (1.0 / ((r**4) * np.sqrt(f_r)))
    
    return T_metric, P_metric


def map_metric_phase_diagram(M: float, N_P: int = 100, N_T: int = 100) -> dict:
    """
    Implements Algorithm 2 to classify regions into:
    1: Spacetime Ice (r >= 3M, Ordered GR)
    2: Spacetime Steam (M < r < 3M, Disordered Oloid Fluid)
    0: Unphysical Singular Region (Not present in OCM)
    """
    R_d = 3.0 * G * M / (C**2)
    r_grid = np.linspace(1.01 * (G*M/(C**2)), 6.0 * (G*M/(C**2)), 500)
    
    T_prof, P_prof = compute_metric_profiles(r_grid, M)
    
    # Construct Phase Grid Matrix D(P, T)
    P_grid = np.logspace(np.log10(np.min(P_prof)), np.log10(np.max(P_prof)), N_P)
    T_grid = np.logspace(np.log10(np.min(T_prof)), np.log10(np.max(T_prof)), N_T)
    
    D = np.zeros((N_P, N_T))
    
    for i, P in enumerate(P_grid):
        for j, T in enumerate(T_grid):
            # Invert profile to estimate effective radius
            dist = np.abs(T_prof - T) / np.max(T_prof) + np.abs(P_prof - P) / np.max(P_prof)
            r_eff = r_grid[np.argmin(dist)]
            
            if r_eff >= R_d:
                D[i, j] = 1  # Spacetime Ice
            elif r_eff > (G * M / (C**2)):
                D[i, j] = 2  # Spacetime Steam
            else:
                D[i, j] = 0  # Forbidden
                
    return {
        "P_grid": P_grid,
        "T_grid": T_grid,
        "phase_matrix": D,
        "R_d": R_d
    }


if __name__ == "__main__":
    print("--- OCM Supplementary S5.2: Metric Phase Diagram Mapper Initialized ---")
    M_test = 10.0 * M_SUN
    phase_data = map_metric_phase_diagram(M=M_test, N_P=50, N_T=50)
    
    ice_count = np.sum(phase_data['phase_matrix'] == 1)
    steam_count = np.sum(phase_data['phase_matrix'] == 2)
    
    print(f"Phase Matrix Grid Mapped: {phase_data['phase_matrix'].shape}")
    print(f"Spacetime Ice (GR) Cells: {ice_count}")
    print(f"Spacetime Steam (Fluid) Cells: {steam_count}")
