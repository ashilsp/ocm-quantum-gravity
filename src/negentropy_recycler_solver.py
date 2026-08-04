"""
Order Creator Mechanism (OCM) - Negentropy Recycler Solver
Module: negentropy_recycler_solver.py
Description: Models modified Planck distribution weighted by quantum transmission |T(E)|^2 
             and calculates the negentropy entropy rate balance dS_out/dt = dS_in/dt - kappa*(dI/dt).
"""

import numpy as np

# Physical Constants (SI)
H = 6.62607015e-34       # Planck constant (J s)
C = 2.99792458e8         # Speed of light (m/s)
K_B = 1.380649e-23       # Boltzmann constant (J/K)


def modified_planck_radiance(nu: float, T_rd: float, T_prob: float) -> float:
    """
    Computes phase-encoded modified Planck spectral radiance:
    I(nu, T_Rd) = (8 * pi * h * nu^3 / c^3) * |T(E)|^2 / (exp(h*nu / (k_B * T_Rd)) - 1)
    """
    exponent = (H * nu) / (K_B * T_rd)
    if exponent > 700:  # Overflow protection
        return 0.0
    
    base_planck = (8.0 * np.pi * H * (nu**3)) / (C**3)
    thermal_factor = 1.0 / (np.exp(exponent) - 1.0)
    
    return base_planck * (abs(T_prob)**2) * thermal_factor


def entropy_output_rate(dS_in_dt: float, kappa: float, dI_dt: float) -> float:
    """
    Calculates outgoing entropy rate under active negentropy flux N = -kappa * (dI/dt):
    dS_out/dt = dS_in/dt - kappa * (dI/dt)
    """
    return dS_in_dt - (kappa * dI_dt)


if __name__ == "__main__":
    print("--- OCM Negentropy Recycler Solver Initialized ---")
    
    # Test Parameters
    T_shell = 1.0e11         # QGP Shell Temperature (K)
    test_freq = 1.0e22       # High-frequency Gamma-Ray (Hz)
    transmission_prob = 0.05 # Barrier tunneling probability |T(E)|^2
    
    radiance = modified_planck_radiance(test_freq, T_shell, transmission_prob)
    print(f"Modified Spectral Radiance I(nu): {radiance:.4e} J*s/m^3")
    
    # Entropy export balance check
    S_in_rate = 10.0   # Incoming chaotic entropy rate
    kappa_coef = 1.5   # Negentropy coupling constant
    I_rate = -5.0      # Information export rate
    
    S_out_rate = entropy_output_rate(S_in_rate, kappa_coef, I_rate)
    print(f"Incoming Entropy Rate (dS_in/dt):  {S_in_rate:.2f}")
    print(f"Outgoing Entropy Rate (dS_out/dt): {S_out_rate:.2f} (Low-entropy coherent export)")
