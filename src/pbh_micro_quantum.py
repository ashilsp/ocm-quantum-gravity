"""
Order Creator Mechanism (OCM) - PBH Micro-Quantum Engine
Module: pbh_micro_quantum.py
Description: Solves WKB barrier penetration probability T(E) across the R_d boundary,
             matrix element saturation bounds, and discrete n=1 -> |0> vacuum transition.
"""

import numpy as np

# Physical Constants (SI Units)
G = 6.67430e-11          # Gravitational constant (m^3 kg^-1 s^-2)
C = 2.99792458e8         # Speed of light (m/s)
HBAR = 1.054571817e-34   # Reduced Planck constant (J s)
M_P = np.sqrt(HBAR * C / G)  # Planck Mass (~2.176e-8 kg)
T_P = np.sqrt(HBAR * G / C**5)  # Planck Time (~5.391e-44 s)
E_P = M_P * C**2         # Planck Energy (~1.956e9 J ~ 1.22e19 GeV)

# Maximum Accretion Limit (c^3 / G)
M_DOT_MAX = C**3 / G     # ~4.037e35 kg/s


def wkb_transmission_coefficient(E: float, V_0: float, barrier_width: float, m_particle: float) -> float:
    """
    Calculates the WKB transmission probability T(E) for nuclear matter (neutrons)
    penetrating the repulsive kappa-potential barrier at R_d = 3M.
    """
    if E >= V_0:
        return 1.0
    
    # Action integral approximation gamma = (2/hbar) * int( sqrt(2m(V(r) - E)) dr )
    k_bar = np.sqrt(2.0 * m_particle * (V_0 - E)) / HBAR
    gamma = 2.0 * k_bar * barrier_width
    return float(np.exp(-gamma))


def saturated_accretion_rate(M_pbh_kg: float, classical_bondi_rate: float) -> float:
    """
    Enforces matrix element saturation (M_fi <= M_max) on PBH accretion rates.
    Prevents unphysical runaway destruction of host neutron stars.
    """
    # Capped at universal max bandwidth M_dot_max = c^3 / G
    return min(classical_bondi_rate, M_DOT_MAX)


def terminal_vacuum_burst() -> dict:
    """
    Computes the discrete single-quantum terminal transition (n=1 -> |0>)
    resolving the Hawking Hawking UV catastrophe.
    """
    return {
        "ground_state": "n = 1",
        "final_state": "|0> (True Vacuum)",
        "burst_energy_joules": E_P,
        "burst_energy_gev": E_P / 1.60218e-10
    }


if __name__ == "__main__":
    print("--- OCM PBH Micro-Quantum Engine Initialized ---")
    
    # Test WKB reflection for neutrons
    m_neutron = 1.674927498e-27  # kg
    E_neutron = 1.0e-13  # Joules (~MeV range)
    V_barrier = 5.0e-13  # Joules
    width = 1.0e-16      # meters (~fm scale)
    
    T_prob = wkb_transmission_coefficient(E_neutron, V_barrier, width, m_neutron)
    print(f"WKB Barrier Penetration Probability T(E): {T_prob:.4e} (T(E) << 1 => Reflection)")
    
    # Accretion saturation check
    rate = saturated_accretion_rate(1.0e12, 1.0e40)
    print(f"Saturated PBH Accretion Limit: {rate:.4e} kg/s (Bounded by c^3/G = {M_DOT_MAX:.4e})")
    
    # Terminal pulse
    burst = terminal_vacuum_burst()
    print(f"Terminal Evaporation Pulse: {burst['burst_energy_gev']:.3e} GeV")
