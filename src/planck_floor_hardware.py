"""
Order Creator Mechanism (OCM) - Planck Floor & Hardware Limits Solver
Module: planck_floor_hardware.py
Description: Computes master Planckian specs (l_P, t_P, p_P, Z_man, I_OCM),
             models the r^{-4} Casimir pressure repulsive floor at r -> l_P,
             and verifies finite mass density regulation.
"""

import numpy as np

# Fundamental Constants (SI)
HBAR = 1.054571817e-34    # J s
G = 6.67430e-11           # m^3 kg^-1 s^-2
C = 2.99792458e8          # m/s


def master_planck_specifications() -> dict:
    """
    Computes fundamental OCM Planck scale hardware constants.
    """
    l_P = np.sqrt(HBAR * G / (C**3))
    t_P = np.sqrt(HBAR * G / (C**5))
    V_P = l_P**3
    E_P = np.sqrt(HBAR * (C**5) / G)
    f_OCM = 1.0 / t_P
    F_OCM = (C**4) / G
    p_P = (C**7) / (HBAR * (G**2))
    Z_man = p_P / f_OCM
    P_P = (C**5) / G
    rho_max = (3.0 * (C**2)) / (8.0 * np.pi * G * (l_P**2))
    dot_M_max = np.sqrt(HBAR * C / G) / t_P
    I_OCM = 1.0 / (t_P * np.log(2.0))

    return {
        "l_P": l_P,
        "t_P": t_P,
        "V_P": V_P,
        "E_P": E_P,
        "f_OCM": f_OCM,
        "F_OCM": F_OCM,
        "p_P": p_P,
        "Z_man": Z_man,
        "P_P": P_P,
        "rho_max": rho_max,
        "dot_M_max": dot_M_max,
        "I_OCM": I_OCM,
    }


def casimir_repulsive_pressure(r: float, C_casimir: float = 1.0) -> float:
    """
    Computes r^{-4} scaling Casimir pressure at small radii near r -> l_P.
    """
    l_P = np.sqrt(HBAR * G / (C**3))
    r_effective = max(r, l_P)
    return C_casimir / (r_effective**4)


if __name__ == "__main__":
    print("--- OCM Master Planck Specifications & Hardware Limits ---")
    
    specs = master_planck_specifications()
    print(f"Planck Length (l_P):        {specs['l_P']:.3e} m")
    print(f"Planck Time (t_P):          {specs['t_P']:.3e} s")
    print(f"Refresh Rate (f_OCM):       {specs['f_OCM']:.3e} Hz")
    print(f"Planck Pressure (p_P):      {specs['p_P']:.3e} Pa")
    print(f"Vacuum Impedance (Z_man):   {specs['Z_man']:.3e} Pa s")
    print(f"Max Density (rho_max):      {specs['rho_max']:.3e} kg/m^3")
    print(f"Info Throughput (I_OCM):    {specs['I_OCM']:.3e} bits/s")
    
    # Floor pressure check
    p_floor = casimir_repulsive_pressure(specs['l_P'])
    print(f"Geometric Floor Casimir Pressure at l_P: {p_floor:.3e} (Normalized)")
