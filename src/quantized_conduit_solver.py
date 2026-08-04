"""
Order Creator Mechanism (OCM) - Quantized Conduit & Scale Synchronization Solver
Module: quantized_conduit_solver.py
Description: Models scale bridging from macro-scale filter (R_d = 3M) down to Planck floor (l_P),
             solves inverse-quartic kappa-flux scaling E_kappa(r) ~ r^-4, and evaluates 
             baryonic-to-quantized phase transcoding.
"""

import numpy as np

# SI Physical Constants
HBAR = 1.054571817e-34    # J s
G = 6.67430e-11           # m^3 kg^-1 s^-2
C = 2.99792458e8          # m/s


def planck_length() -> float:
    """Returns fundamental spatial floor l_P = sqrt(hbar * G / c^3)."""
    return np.sqrt(HBAR * G / (C**3))


def kappa_flux_density_profile(r: float, R_d: float) -> float:
    """
    Computes kappa-flux energy density profile scaling inverse-quartically (r^-4).
    Saturates at maximum tension F_OCM = c^4 / G at r = l_P.
    """
    l_P = planck_length()
    r_effective = max(r, l_P)
    
    # Base density normalized at R_d
    E_P = np.sqrt(HBAR * (C**5) / G)
    rho_P = E_P / (l_P**3)
    
    # Scaling profile from R_d to l_P
    profile = rho_P * ((l_P / r_effective)**4)
    return profile


def phase_transcoding_state(r: float, R_d: float) -> str:
    """
    Determines phase state across spatial transition:
    - Classical Baryonic Fluid (r > R_d)
    - Laminarized Interface Transition (l_P < r <= R_d)
    - Quantized Spacetime Steam (r <= l_P)
    """
    l_P = planck_length()
    if r > R_d:
        return "Classical Baryonic Fluid (Exterior Ice)"
    elif l_P < r <= R_d:
        return "Laminarized Transition Phase (kappa-flux Active)"
    else:
        return "Quantized Spacetime Steam (Planck Floor Reached)"


if __name__ == "__main__":
    print("--- OCM Quantized Conduit Solver Initialized ---")
    
    l_P = planck_length()
    print(f"Planck Spatial Floor (l_P): {l_P:.4e} m")
    
    # Test for 10 Solar Mass Black Hole
    M_test = 10.0 * 1.989e30
    R_d_test = (3.0 * G * M_test) / (C**2)
    print(f"Macroscopic Operational Boundary (R_d): {R_d_test:.4e} m")
    
    # Scale hierarchy factor
    hierarchy_orders = np.log10(R_d_test / l_P)
    print(f"Scale Hierarchy Bridge Span: 10^{hierarchy_orders:.2f} orders of magnitude")
    
    # Test profiles at key coordinates
    for test_r in [R_d_test * 2.0, R_d_test, R_d_test * 1e-10, l_P]:
        rho_k = kappa_flux_density_profile(test_r, R_d_test)
        state = phase_transcoding_state(test_r, R_d_test)
        print(f"Radius r = {test_r:.2e} m -> rho_kappa = {rho_k:.2e} J/m^3 | State: {state}")
