"""
Order Creator Mechanism (OCM) - Perturbation & Transition Engine
Module: fermi_decay_solver.py
Description: Solves time-dependent perturbation theory and Fermi's Golden Rule
             decay from chaotic inflow states (Psi_k) into ground state (Psi_0).
"""

import numpy as np

# Constants
HBAR = 1.054571817e-34  # J s


def turbulent_matrix_element(angular_momentum_l: int, coupling_lambda: float = 0.1) -> float:
    """
    Computes the matrix element <Psi_0 | V_turb | Psi_k>.
    High angular momentum modes (l >> 1) suffer exponential damping at R_d = 3M.
    """
    return coupling_lambda * np.exp(-0.5 * angular_momentum_l)


def fermis_golden_rule_rate(matrix_element: float, density_of_states: float = 1.0) -> float:
    """
    Calculates transition rate W_{0 -> k} = (2*pi / hbar) * |<Psi_0|V|Psi_k>|^2 * rho(E)
    """
    return (2.0 * np.pi / HBAR) * (matrix_element**2) * density_of_states


def laminar_decay_profile(t: np.ndarray, initial_turbulent_energy: float = 1.0, decay_rate: float = 2.5) -> np.ndarray:
    """
    Computes the exponential energy dissipation profile dropping into E_0.
    """
    return initial_turbulent_energy * np.exp(-decay_rate * t)


if __name__ == "__main__":
    print("--- OCM Perturbation & Fermi Decay Solver ---")
    l_modes = [0, 1, 2, 4, 8]
    for l in l_modes:
        V_matrix = turbulent_matrix_element(angular_momentum_l=l)
        W_rate = fermis_golden_rule_rate(V_matrix)
        print(f"Mode l={l}: Matrix Element = {V_matrix:.4e}, Decay Rate W = {W_rate:.4e} s^-1")
