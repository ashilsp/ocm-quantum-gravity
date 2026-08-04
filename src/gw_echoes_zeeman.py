"""
Order Creator Mechanism (OCM) - GW Echoes & Zeeman Engine
Module: gw_echoes_zeeman.py
Description: Solves time-domain gravitational wave echo pulse trains 
             and frequency-domain Zeeman QNM multipole splitting (a > 0).
"""

import numpy as np


def time_domain_echoes(t: np.ndarray, M: float = 10.0, num_echoes: int = 3) -> np.ndarray:
    """
    Computes time-domain GW strain h(t) including primary ringdown 
    and trapped cavity echoes reflecting off R_d = 3M.
    """
    # Primary ringdown
    tau_ring = 3.0
    h_t = 1.1 * np.exp(-t / tau_ring) * np.cos(1.8 * t) * (t >= 0)
    
    # Sub-harmonic echoes at dt_echo intervals
    dt_echo = 14.0  # Normalized cavity travel time ~ 2*R_d / c
    for i in range(1, num_echoes + 1):
        t_center = i * dt_echo
        amplitude = 0.55 * (0.6 ** (i - 1))
        echo_pulse = amplitude * np.exp(-0.6 * (t - t_center)**2) * np.cos(2.2 * (t - t_center))
        h_t += echo_pulse
        
    return h_t


def zeeman_qnm_splitting(omega_grid: np.ndarray, omega_0: float = 3.0, Omega_H: float = 0.6, spin_a: float = 0.7) -> dict:
    """
    Computes the Geometric Zeeman splitting of QNM power spectrum |h(omega)|^2
    for m = {-2, -1, 0, +1, +2} multipole channels driven by H_rot = -Omega_H * L_z.
    """
    spectrum = {}
    m_modes = [-2, -1, 0, 1, 2]
    
    for m in m_modes:
        # Shifted frequency: omega_m = omega_0 + m * Omega_H
        omega_m = omega_0 + m * (Omega_H * spin_a)
        amp = 0.90 if m == 0 else (0.65 if abs(m) == 1 else 0.35)
        spectrum[m] = amp / (1.0 + 45.0 * (omega_grid - omega_m)**2)
        
    return spectrum


if __name__ == "__main__":
    print("--- OCM GW Echoes & Zeeman Splitting Engine Initialized ---")
    t_vals = np.linspace(0, 50, 500)
    strain = time_domain_echoes(t_vals)
    print(f"Time-domain strain calculated across t in [0, 50]. Peak Strain = {np.max(strain):.4f}")
    
    w_vals = np.linspace(0.5, 5.5, 300)
    zeeman_data = zeeman_qnm_splitting(w_vals)
    print(f"Zeeman Multipole Splitting calculated for 5 m-modes ({list(zeeman_data.keys())}).")
