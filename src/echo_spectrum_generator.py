"""
Order Creator Mechanism (OCM) - Supplementary Section S5.1
Module: echo_spectrum_generator.py
Description: Implements Algorithm 1 (OCM Sub-Harmonic Echo Spectrum Generator).
             Down-converts high-frequency metric fluctuations via a sub-harmonic cascade 
             across acoustic shells at R_d = 3M into the observable gravitational wave band (10 Hz - 5 kHz).
"""

import numpy as np

# Physical Constants
G = 6.67430e-11           # m^3 kg^-1 s^-2
C = 2.99792458e8          # m/s
M_SUN = 1.989e30          # kg
F_OCM = 1.85e43           # Metric refresh frame rate [Hz]


def generate_echo_spectrum(M_f: float, epsilon_kappa: float = 0.01, N_n: int = 5, f_min: float = 10.0, f_max: float = 5000.0, num_bins: int = 500) -> dict:
    """
    Implements Algorithm 1 to calculate the observable sub-harmonic echo Power Spectral Density (PSD).
    """
    # Fundamental cavity frequency f_fundamental = c^3 / (2 * pi * G * M_f)
    f_fundamental = (C**3) / (2.0 * np.pi * G * M_f)
    
    # Observable frequency grid
    f_obs = np.linspace(f_min, f_max, num_bins)
    psd = np.zeros_like(f_obs)
    
    # Sub-harmonic resonant frequencies: f_n = f_fundamental * (1 / n)
    f_harmonics = [f_fundamental / n for n in range(1, N_n + 1)]
    
    # Evaluate sub-harmonic energy transfer into observable bins
    for i, f in enumerate(f_obs):
        power = 0.0
        for f_n in f_harmonics:
            # Lorentzian acoustic resonance profile centered at f_n
            gamma = 0.05 * f_n
            lorentzian = (gamma**2) / ((f - f_n)**2 + gamma**2)
            power += (epsilon_kappa**2) * lorentzian
        psd[i] = power / N_n
        
    return {
        "M_f_solar": M_f / M_SUN,
        "f_fundamental_Hz": f_fundamental,
        "f_harmonics_Hz": f_harmonics,
        "f_obs": f_obs,
        "PSD": psd
    }


if __name__ == "__main__":
    print("--- OCM Supplementary S5.1: Sub-Harmonic Echo Spectrum Solver Initialized ---")
    M_remnant = 60.0 * M_SUN
    echo_data = generate_echo_spectrum(M_f=M_remnant, epsilon_kappa=0.05, N_n=5)
    
    print(f"Remnant Mass: {echo_data['M_f_solar']:.1f} M_sun")
    print(f"Fundamental Cavity Frequency: {echo_data['f_fundamental_Hz']:.2f} Hz")
    print(f"Harmonic Resonances (Hz): {[round(h, 2) for h in echo_data['f_harmonics_Hz']]}")
    print(f"Peak PSD in Observable Band: {np.max(echo_data['PSD']):.4e}")
