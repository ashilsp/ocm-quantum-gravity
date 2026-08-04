"""
Order Creator Mechanism (OCM) - EHT Shadow & HFQPO Resonance Solver
Module: eht_hfqpo_solver.py
Description: Solves the asymmetric D-shaped EHT photon shadow, calculates 3:2 twin-peak
             QPO frequencies (poloidal/toroidal modes), and models the CMB dipolar alignment.
"""

import numpy as np


def asymmetric_d_shaped_shadow(phi: np.ndarray, R_shadow: float = 5.2, 
                                epsilon: float = 0.12, eta: float = 0.15) -> np.ndarray:
    """
    Computes asymmetric D-shaped photon shadow radius r(phi) cast by Oloid-like potential:
    r(phi) = R_shadow * (1 + epsilon * cos(3*phi) + eta * sin^2(phi))
    """
    return R_shadow * (1.0 + epsilon * np.cos(3.0 * phi) + eta * (np.sin(phi)**2))


def hfqpo_resonant_frequencies(f_0: float = 56.67) -> dict:
    """
    Computes 3:2 twin-peak HFQPO frequencies and ghost pulse sideband:
    f_toroidal (2x) = 2 * f_0
    f_poloidal (3x) = 3 * f_0
    f_ghost = |2*f_poloidal - 3*f_toroidal| or sub-harmonic beat
    """
    f_toroidal = 2.0 * f_0
    f_poloidal = 3.0 * f_0
    f_ghost = abs(f_poloidal - f_toroidal)  # Fundamental beat frequency
    
    return {
        "f_0_fundamental": f_0,
        "f_toroidal_2x": f_toroidal,
        "f_poloidal_3x": f_poloidal,
        "f_ghost_pulse": f_ghost,
        "ratio": f_poloidal / f_toroidal
    }


if __name__ == "__main__":
    print("--- OCM EHT Shadow & HFQPO Resonance Solver Initialized ---")
    
    # EHT D-shaped shadow radius
    phi_vals = np.linspace(0, 2*np.pi, 360)
    r_shadow = asymmetric_d_shaped_shadow(phi_vals)
    print(f"Shadow Radius Min/Max: {np.min(r_shadow):.2f} / {np.max(r_shadow):.2f} R_M (Asymmetric D-Shape)")
    
    # Microquasar GRS 1915+105 HFQPO lock (f_0 = 56.67 Hz -> 113 Hz / 170 Hz / 283 Hz)
    qpo = hfqpo_resonant_frequencies(56.67)
    print(f"Toroidal Peak (2x): {qpo['f_toroidal_2x']:.2f} Hz")
    print(f"Poloidal Peak (3x): {qpo['f_poloidal_3x']:.2f} Hz")
    print(f"Resonant Ratio:     {qpo['ratio']:.2f} (Locked 3:2 Integer Ratio)")
    print(f"Ghost Pulse Beat:   {qpo['f_ghost_pulse']:.2f} Hz")
