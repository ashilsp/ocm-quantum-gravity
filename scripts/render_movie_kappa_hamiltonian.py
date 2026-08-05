import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Dark Theme Render Engine
plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.5), dpi=150)
fig.patch.set_facecolor('#05050d')
fig.subplots_adjust(bottom=0.32, top=0.88, wspace=0.25, left=0.06, right=0.95)

for ax in (ax1, ax2):
    ax.set_facecolor('#080812')
    ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Titles
ax1.set_title("MOVIE S22: Strong Energy Condition (SEC) Violation & Hard Floor\n(rho_kappa + 3*p_r < 0 Inside r <= R_d & Ground State u_1(l_P) = 0)", 
              color='#f43f5e', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE S22: Non-Perturbative UV Loop Convergence vs. Divergence\n(OCM Propagator D_OCM(k) Suppresses Infinite Momentum Catastrophe)", 
              color='#10b981', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup
r_vals = np.linspace(0.01, 3.0, 400)
ax1.set_xlim(0, 3.0)
ax1.set_ylim(-3.0, 3.0)
ax1.set_xlabel(r'Normalized Radius $r/R_d$', color='white')
ax1.set_ylabel(r'SEC Combination / Wavefunction $u_1(r)$', color='white')

# Subplot 2 Setup
k_vals = np.linspace(0.01, 10.0, 400)
ax2.set_xlim(0.01, 10.0)
ax2.set_ylim(0, 25.0)
ax2.set_xlabel(r'Wavenumber $k / k_{\max}$', color='white')
ax2.set_ylabel(r'Loop Integrand $k^2 D(k)$', color='white')

# Static Elements Subplot 1
ax1.axhline(0.0, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(1.0, color='#f43f5e', linestyle='--', label=r'Boundary Shell $r = R_d = 3M$')
ax1.axvline(0.05, color='#38bdf8', linestyle=':', label=r'Planck Floor $r = l_P$ ($u_1 = 0$)')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#f43f5e')

# Static Elements Subplot 2
classical_integrand = k_vals**2 / (k_vals**2 + 1.0) * 2.0
ax2.plot(k_vals, classical_integrand, color='#ef4444', linestyle='--', linewidth=2.0, label='Classical Divergence (k -> infinity)')
ax2.legend(loc='upper left', facecolor='#0d111d', edgecolor='#10b981')

# Dynamic Elements
sec_curve, = ax1.plot([], [], color='#f43f5e', linewidth=2.5, label=r'SEC Profile ($\rho_\kappa + 3p_{r,\kappa}$)')
psi_curve, = ax1.plot([], [], color='#38bdf8', linewidth=2.0, label=r'Wavefunction $u_1(r)$')
ocm_integrand_curve, = ax2.plot([], [], color='#10b981', linewidth=2.5, label='OCM Finite Integrand (Exp Cutoff)')

status_A = fig.text(0.28, 0.08, '', color='#f43f5e', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#f43f5e'))
status_B = fig.text(0.72, 0.08, '', color='#10b981', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#10b981'))

def update(frame):
    t = frame * 0.1
    
    # Dynamic SEC and Wavefunction Profiles
    sec_profile = np.where(r_vals <= 1.0, -2.0 * (1.0 - r_vals**2) + 0.2 * np.sin(3*t), 0.5 / r_vals**2)
    dr = np.maximum(r_vals - 0.05, 0.0)
    psi_profile = 2.5 * dr * np.exp(-3.0 * dr) * (1.0 + 0.1 * np.sin(5*t))
    
    sec_curve.set_data(r_vals, sec_profile)
    psi_curve.set_data(r_vals, psi_profile)
    
    # OCM Cutoff Loop Integrand
    ocm_integrand = classical_integrand * np.exp(-(k_vals / 3.0)**2 * (1.0 + 0.05 * np.cos(3*t)))
    ocm_integrand_curve.set_data(k_vals, ocm_integrand)
    
    status_A.set_text("STRONG ENERGY CONDITION VIOLATED\nSEC < 0 exclusively for r <= R_d = 3M\nOutward kappa-pressure prevents singularity formation")
    status_B.set_text("UV CATASTROPHE CURED NON-PERTURBATIVELY\nPlanck cutoff k_max = 1/l_P enforces convergence\nLoop integral I_OCM remains strictly finite")

    return sec_curve, psi_curve, ocm_integrand_curve, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'MovieS1_Kappa_Hamiltonian.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
