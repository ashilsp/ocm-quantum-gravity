"""
Order Creator Mechanism (OCM) - Quantum Leidenfrost & Phase Transition Solver
Module: leidenfrost_phase_solver.py
Description: Models thermodynamic phase transitions across the R_d interface,
             calculates E_P vacuum chemical potential ignition threshold, 
             quantum Leidenfrost standing wave cushion pressure, and phase reversion rate.
"""

import numpy as np

# Physical Constants (SI)
HBAR = 1.054571817e-34    # J s
G = 6.67430e-11           # m^3 kg^-1 s^-2
C = 2.99792458e8          # m/s


def planck_chemical_potential() -> float:
    """
    Computes fundamental vacuum chemical potential mu_vac = E_P = sqrt(hbar * c^5 / G).
    """
    return np.sqrt(HBAR * (C**5) / G)


def leidenfrost_cushion_pressure(r: float, R_d: float, E_density: float) -> float:
    """
    Computes quantum Leidenfrost standing wave repulsive cushion pressure near r = R_d.
    Pressure spikes as E_density approaches E_P / l_P^3.
    """
    l_P = np.sqrt(HBAR * G / (C**3))
    E_P = planck_chemical_potential()
    E_P_density = E_P / (l_P**3)
    
    # Normalized ratio of local energy density to Planck energy density
    saturation_ratio = min(E_density / E_P_density, 0.999)
    
    # Acoustic-like standing wave pressure cushion
    p_cushion = (C**7 / (HBAR * G**2)) * (1.0 / (1.0 - saturation_ratio)) * np.exp(-abs(r - R_d) / l_P)
    return p_cushion


def phase_reversion_condensation_rate(mass_accretion_rate: float, 
                                        threshold_rate: float = 4.037e35) -> float:
    """
    Calculates phase reversion (Hawking condensation) rate.
    When mass accretion falls below activation threshold, steam condenses back to ice.
    """
    if mass_accretion_rate >= threshold_rate:
        return 0.0  # Fully active conduit phase
    else:
        # Reversion rate scales with deficit
        return (threshold_rate - mass_accretion_rate) / threshold_rate


if __name__ == "__main__":
    print("--- OCM Quantum Leidenfrost & Phase Transition Solver Initialized ---")
    
    E_P = planck_chemical_potential()
    print(f"Planck Chemical Potential (E_P / mu_vac): {E_P:.4e} J ({E_P / 1.602e-10:.4e} GeV)")
    
    # Test Cushion Pressure at R_d
    R_d_test = 3.0 * 1.477e3  # 3M for solar mass BH (m)
    test_density = 0.95 * (E_P / (1.616e-35)**3)
    
    p_cush = leidenfrost_cushion_pressure(R_d_test, R_d_test, test_density)
    print(f"Leidenfrost Cushion Pressure at R_d:      {p_cush:.4e} Pa")
    
    # Check Reversion Rate under Sub-threshold Accretion
    accretion_sub = 0.2 * 4.037e35
    rev_rate = phase_reversion_condensation_rate(accretion_sub)
    print(f"Sub-threshold Accretion Reversion Rate:   {rev_rate * 100:.2f}% Phase Reversion (Condensation)")
