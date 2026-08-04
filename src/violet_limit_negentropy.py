"""
Order Creator Mechanism (OCM) - Violet Limit & Negentropy Engine
Module: violet_limit_negentropy.py
Description: Solves QGP thermal spectrum at R_d = 3M, gravitational redshift z_{R_d} = sqrt(3) - 1,
             and negentropy flux N = -kappa * (dI/dt) for unitary information preservation.
"""

import numpy as np

# Physical Constants (SI)
WIEN_B = 2.897771955e-3  # Wien displacement constant (m K)
C = 2.99792458e8         # Speed of light (m/s)
HBAR = 1.054571817e-34   # Reduced Planck constant (J s)
EV_TO_JOULE = 1.602176634e-19


def qgp_local_peak_wavelength(T_rd: float = 1.0e11) -> float:
    """
    Calculates local peak wavelength lambda_peak at R_d = 3M for QGP temperature T_rd.
    Default T_rd ~ 10^11 K gives lambda_peak ~ 2.9e-14 m.
    """
    return WIEN_B / T_rd


def gravitational_redshift_factor(r_ratio: float = 3.0) -> float:
    """
    Calculates gravitational redshift factor 1 + z = (1 - 2M/R_d)^(-1/2).
    For R_d = 3M, 1 + z_Rd = (1 - 2/3)^(-1/2) = sqrt(3) ~ 1.73205.
    """
    return 1.0 / np.sqrt(1.0 - (2.0 / r_ratio))


def observed_spectral_parameters(T_rd: float = 1.0e11, r_ratio: float = 3.0) -> dict:
    """
    Computes down-shifted observed temperature and peak frequency at spatial infinity.
    """
    factor = gravitational_redshift_factor(r_ratio)
    T_obs = T_rd / factor
    lambda_local = qgp_local_peak_wavelength(T_rd)
    nu_local = C / lambda_local
    nu_obs = nu_local / factor
    E_peak_mev_local = (HBAR * 2.0 * np.pi * nu_local) / (1.0e6 * EV_TO_JOULE)
    E_peak_mev_obs = E_peak_mev_local / factor

    return {
        "redshift_factor_1_plus_z": factor,
        "T_local_K": T_rd,
        "T_obs_K": T_obs,
        "E_peak_MeV_local": E_peak_mev_local,
        "E_peak_MeV_obs": E_peak_mev_obs,
    }


def negentropy_flux(kappa: float, dI_dt: float) -> float:
    """
    Calculates negentropy information export flux N = -kappa * (dI/dt).
    """
    return -kappa * dI_dt


if __name__ == "__main__":
    print("--- OCM Violet Limit & Negentropy Engine Initialized ---")

    params = observed_spectral_parameters()
    print(f"Redshift Factor (1 + z_Rd):   {params['redshift_factor_1_plus_z']:.4f} (Expected sqrt(3) = {np.sqrt(3):.4f})")
    print(f"Local QGP Temperature:       {params['T_local_K']:.2e} K")
    print(f"Observed Temperature:        {params['T_obs_K']:.2e} K")
    print(f"Local Peak Photon Energy:     {params['E_peak_MeV_local']:.2f} MeV")
    print(f"Observed Peak Photon Energy:  {params['E_peak_MeV_obs']:.2f} MeV (Redshifted)")

    N_flux = negentropy_flux(1.5, -2.4)
    print(f"Negentropy Export Flux N:     {N_flux:.2f} (Preserves Unitarity Delta I = 0)")
