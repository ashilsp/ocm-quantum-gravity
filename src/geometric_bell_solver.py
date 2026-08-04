"""
Order Creator Mechanism (OCM) - Geometric Bell & Heisenberg Stabilization Solver
Module: geometric_bell_solver.py
Description: Solves Planck frame rate f_OCM, computes Heisenberg zero-point energy floor,
             and models sub-harmonic GW echo downscaling across cavity mode numbers N_n.
"""

import numpy as np

# SI Physical Constants
HBAR = 1.054571817e-34    # J s
G = 6.67430e-11           # m^3 kg^-1 s^-2
C = 2.99792458e8          # m/s


def planck_frame_rate() -> float:
    """
    Computes fundamental frame rate of spacetime f_OCM = 1 / t_P = sqrt(c^5 / (hbar * G)).
    """
    t_P = np.sqrt(HBAR * G / (C**5))
    return 1.0 / t_P


def heisenberg_zero_point_floor() -> dict:
    """
    Computes Heisenberg vacuum zero-point pressure floor Delta_E = hbar / (2 * t_P) = 0.5 * E_P.
    """
    t_P = np.sqrt(HBAR * G / (C**5))
    E_P = np.sqrt(HBAR * (C**5) / G)
    Delta_E_min = HBAR / (2.0 * t_P)
    
    return {
        "t_P": t_P,
        "E_P": E_P,
        "Delta_E_min": Delta_E_min,
        "ratio_to_E_P": Delta_E_min / E_P
    }


def subharmonic_gw_echo_frequencies(M_solar: float = 30.0) -> dict:
    """
    Calculates macro-scale sub-harmonic GW echo frequency f_n from micro f_OCM.
    f_n = f_OCM / N_n, where N_n ~ (M / m_P) * log(M / m_P).
    """
    f_OCM = planck_frame_rate()
    M_kg = M_solar * 1.989e30
    m_P = np.sqrt(HBAR * C / G)
    
    # Quantum mode downscaling integer N_n
    N_n = (M_kg / m_P) * np.log(M_kg / m_P)
    f_echo = f_OCM / N_n
    
    return {
        "M_solar": M_solar,
        "f_OCM": f_OCM,
        "mode_number_N": N_n,
        "f_echo_kHz": f_echo / 1e3
    }


if __name__ == "__main__":
    print("--- OCM Geometric Bell & Heisenberg Stabilization Solver Initialized ---")
    
    f_OCM = planck_frame_rate()
    print(f"Spacetime Frame Rate (f_OCM):         {f_OCM:.4e} Hz")
    
    hb = heisenberg_zero_point_floor()
    print(f"Heisenberg Min Zero-Point Floor (Delta_E): {hb['Delta_E_min']:.4e} J (Exactly {hb['ratio_to_E_P']:.1f} E_P)")
    
    gw = subharmonic_gw_echo_frequencies(30.0)
    print(f"Macro GW Echo Frequency (30 Solar Mass BH): {gw['f_echo_kHz']:.3f} kHz (Downscaled from 10^43 Hz via N_n = {gw['mode_number_N']:.2e})")
