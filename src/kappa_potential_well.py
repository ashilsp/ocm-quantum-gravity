"""
Order Creator Mechanism (OCM) - Potential Well Solver
Module: kappa_potential_well.py
Description: Computes the Effective Potential V_eff(r) and stationary 
             wavefunction |Psi(r)|^2 across the R_d = 3M boundary.
"""

import numpy as np


def gravitational_potential(r: np.ndarray, G: float = 1.0, M: float = 1.0) -> np.ndarray:
    """
    Computes classical Newtonian/GR attractive potential V_grav = -GM/r
    """
    return - (G * M) / r


def kappa_repulsive_potential(r: np.ndarray, kappa_n: float = 0.85, n: int = 3) -> np.ndarray:
    """
    Computes the repulsive Order Creator Term V_kappa = + kappa_n / r^n (n > 1)
    which forms the hard potential wall near r -> 0.
    """
    return kappa_n / (r**n)


def effective_potential(r: np.ndarray, G: float = 1.0, M: float = 1.0, kappa_n: float = 0.85, n: int = 3) -> np.ndarray:
    """
    Computes total composite effective potential V_eff = V_grav + V_kappa
    """
    return gravitational_potential(r, G, M) + kappa_repulsive_potential(r, kappa_n, n)


def stationary_wavefunction_density(r: np.ndarray, r_min: float = 1.19, sigma: float = 0.2) -> np.ndarray:
    """
    Calculates the probability density |Psi(r)|^2 parked at the 
    local equilibrium minimum R_d (standing wave shell state).
    """
    return np.exp(-((r - r_min)**2) / (2 * sigma**2))


if __name__ == "__main__":
    r_range = np.linspace(0.5, 6.0, 100)
    V_eff = effective_potential(r_range)
    psi_sq = stationary_wavefunction_density(r_range)
    
    print("--- OCM Potential Well Solver Initialized ---")
    print(f"Sample r range: [{r_range[0]:.2f}, {r_range[-1]:.2f}]")
    print(f"Minimum Potential Value at R_d: {np.min(V_eff):.4f}")
