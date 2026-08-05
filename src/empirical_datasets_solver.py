"""
Order Creator Mechanism (OCM) - Supplementary Datasets Solver
Module: empirical_datasets_solver.py
Description: Evaluates empirical LVK peak power ratios against P_P = c^5 / G
             and JWST high-z SMBH accretion bounds against M_dot_max = c^3 / G.
"""

import numpy as np

# Physical SI Constants
C = 2.99792458e8          # m/s
G = 6.67430e-11           # m^3 kg^-1 s^-2
M_SUN = 1.989e30          # kg
SEC_PER_YEAR = 31557600.0  # seconds in a Julian year


def planck_power() -> float:
    """Computes Planck Power Ceiling P_P = c^5 / G in Watts."""
    return (C**5) / G


def max_mass_flux() -> dict:
    """Computes OCM Hydrodynamic Mass-Flux Bandwidth M_dot_max = c^3 / G."""
    m_dot_kg_s = (C**3) / G
    m_dot_solar_s = m_dot_kg_s / M_SUN
    m_dot_solar_yr = m_dot_solar_s * SEC_PER_YEAR
    return {
        "M_dot_max_kg_s": m_dot_kg_s,
        "M_dot_max_solar_s": m_dot_solar_s,
        "M_dot_max_solar_yr": m_dot_solar_yr
    }


def analyze_lvk_catalog() -> list:
    """
    Catalog of representative LVK GW events with peak luminosity ratios P_peak / P_P.
    """
    P_P = planck_power()
    lvk_events = [
        {"id": "GW150914", "P_peak_W": 3.6e49},
        {"id": "GW151226", "P_peak_W": 3.3e49},
        {"id": "GW170104", "P_peak_W": 3.1e49},
        {"id": "GW170608", "P_peak_W": 3.4e49},
        {"id": "GW170814", "P_peak_W": 3.7e49},
        {"id": "GW170817 (BNS)", "P_peak_W": 0.01e49},
        {"id": "GW190412", "P_peak_W": 2.8e49},
        {"id": "GW190521", "P_peak_W": 3.7e49},
        {"id": "GW190814 (NSBH)", "P_peak_W": 1.6e49},
        {"id": "GW200105", "P_peak_W": 0.6e49},
        {"id": "GW200115", "P_peak_W": 0.8e49},
    ]
    
    for ev in lvk_events:
        ev["ratio_P_P"] = ev["P_peak_W"] / P_P
        ev["satisfies_ocm_ceiling"] = ev["ratio_P_P"] <= 1.0e-3
        
    return lvk_events


def analyze_jwst_quasars() -> list:
    """
    Catalog of JWST high-z SMBHs evaluated against Eddington growth and M_dot_max.
    """
    bw = max_mass_flux()
    quasars = [
        {"id": "UHZ1", "z": 10.1, "age_Myr": 470, "M_obs_solar": 4.0e7, "eddington_factor": 2.2},
        {"id": "J0313-1806", "z": 7.64, "age_Myr": 670, "M_obs_solar": 1.6e9, "eddington_factor": 1.8},
        {"id": "J1342+0928", "z": 7.54, "age_Myr": 680, "M_obs_solar": 7.8e8, "eddington_factor": 1.6},
        {"id": "J1007+2115", "z": 7.51, "age_Myr": 690, "M_obs_solar": 1.5e9, "eddington_factor": 1.7},
        {"id": "GN-z11", "z": 10.6, "age_Myr": 440, "M_obs_solar": 1.6e6, "eddington_factor": 2.5},
        {"id": "CEERS-1019", "z": 8.68, "age_Myr": 570, "M_obs_solar": 9.0e6, "eddington_factor": 1.4},
    ]
    
    for q in quasars:
        q["M_dot_max_solar_s"] = bw["M_dot_max_solar_s"]
        q["capacity_ratio"] = (q["M_obs_solar"] / (q["age_Myr"] * 1e6 * SEC_PER_YEAR)) / bw["M_dot_max_solar_s"]
        
    return quasars


if __name__ == "__main__":
    print("--- OCM Supplementary Datasets Solver Initialized ---")
    
    P_P = planck_power()
    print(f"Planck Power Ceiling (P_P): {P_P:.4e} W")
    
    lvk_data = analyze_lvk_catalog()
    print(f"\n--- LVK Peak Gravitational Luminosity Evaluation ---")
    for ev in lvk_data[:3]:
        print(f"Event {ev['id']}: Peak Power = {ev['P_peak_W']:.2e} W | Ratio P/P_P = {ev['ratio_P_P']:.2e} | Capped: {ev['satisfies_ocm_ceiling']}")
        
    jwst_data = analyze_jwst_quasars()
    print(f"\n--- JWST High-z Quasar Accretion Evaluation ---")
    for q in jwst_data[:3]:
        print(f"Object {q['id']} (z={q['z']}): Mass = {q['M_obs_solar']:.2e} M_sun | Classical Req = {q['eddington_factor']}x Eddington | Bandwidth Fraction = {q['capacity_ratio']:.2e}")
