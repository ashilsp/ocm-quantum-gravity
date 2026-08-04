"""
Order Creator Mechanism (OCM) - Sequestration Power & Bandwidth Solver
Module: sequestration_power_solver.py
Description: Solves Planck Power ceiling P_P, evaluates empirical LIGO GW150914 
             and GRB 221009A observational ratios, computes mass processing cap M_dot_max, 
             and calculates information throughput I_OCM.
"""

import numpy as np

# SI Physical Constants
HBAR = 1.054571817e-34    # J s
G = 6.67430e-11           # m^3 kg^-1 s^-2
C = 2.99792458e8          # m/s
M_SUN = 1.989e30          # kg


def planck_power_ceiling() -> float:
    """
    Computes absolute Planck power luminosity ceiling P_P = c^5 / G.
    """
    return (C**5) / G


def empirical_power_ratios() -> dict:
    """
    Calculates empirical luminosity saturation ratios relative to P_P.
    """
    P_P = planck_power_ceiling()
    
    # LIGO GW150914 Peak Luminosity (~3.6e49 W)
    L_GW150914 = 3.6e49
    ratio_GW150914 = L_GW150914 / P_P
    
    # GRB 221009A BOAT Peak Gamma-Ray Luminosity (~2.1e47 W)
    L_GRB221009A = 2.1e47
    ratio_GRB221009A = L_GRB221009A / P_P
    
    return {
        "P_P_W": P_P,
        "L_GW150914_W": L_GW150914,
        "ratio_GW150914": ratio_GW150914,
        "L_GRB221009A_W": L_GRB221009A,
        "ratio_GRB221009A": ratio_GRB221009A
    }


def processing_bandwidth_limits() -> dict:
    """
    Calculates mass throughput cap M_dot_max = c^3 / G and information throughput I_OCM.
    """
    M_dot_max_kg_s = (C**3) / G
    M_dot_max_solar_s = M_dot_max_kg_s / M_SUN
    
    t_P = np.sqrt(HBAR * G / (C**5))
    I_OCM_bits_s = 1.0 / (t_P * np.log(2.0))
    
    return {
        "M_dot_max_kg_s": M_dot_max_kg_s,
        "M_dot_max_solar_s": M_dot_max_solar_s,
        "I_OCM_bits_s": I_OCM_bits_s
    }


if __name__ == "__main__":
    print("--- OCM Sequestration Power & Bandwidth Solver Initialized ---")
    
    P_P = planck_power_ceiling()
    print(f"Planck Power Ceiling (P_P):               {P_P:.4e} W")
    
    emp = empirical_power_ratios()
    print(f"LIGO GW150914 Peak Luminosity:           {emp['L_GW150914_W']:.2e} W ({emp['ratio_GW150914']*100:.3f}% P_P)")
    print(f"GRB 221009A BOAT Peak Luminosity:         {emp['L_GRB221009A_W']:.2e} W ({emp['ratio_GRB221009A']*100:.5f}% P_P)")
    
    bw = processing_bandwidth_limits()
    print(f"Max Mass Throughput Cap (M_dot_max):      {bw['M_dot_max_kg_s']:.4e} kg/s ({bw['M_dot_max_solar_s']:.2e} M_sun/s)")
    print(f"Max Information Throughput (I_OCM):      {bw['I_OCM_bits_s']:.4e} bits/s")
