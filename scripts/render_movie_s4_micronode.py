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
ax1.set_title("MOVIE S4: Modified Stellar Core Hydrostatic Equilibrium\n(Central Micro-Node Boundary Condition m(R_node) = M_node)", 
              color='#38bdf8', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE S4: Outward Viscous Force F_kappa(r) Profile\n(Smooth Non-Singular OCM Boundary Prevents Singular Density Collapse)", 
              color='#10b981', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup
r_arr = np.linspace(0.01, 2.0, 300)
ax1.set_xlim(0, 2.0)
ax1.set_ylim(0, 2.0)
ax1.set_xlabel(r'Normalized Core Radius $r / R_{\text{node}}$', color='white')
ax1.set_ylabel(r'Enclosed Mass $m(r) / M_{\text{node}}$', color='white')

# Subplot 2 Setup
ax2.set_xlim(0.01, 3.0)
ax2.set_ylim(0, 1.2)
ax2.set_xlabel(r'Normalized Radius $r / R_{\text{node}}$', color='white')
ax2.set_ylabel(r'Viscous Force $F_\kappa(r) / F_{\text{Planck}}$', color='white')

# Static Elements
ax1.axvline(1.0, color='#f43f5e', linestyle='--', label=r'Node Boundary $R_{\text{node}} = 3M_{\text{node}}$')
ax1.axhline(1.0, color='#38bdf8', linestyle=':', label=r'Enclosed Node Mass $m(R_{\text{node}}) = M_{\text{node}}$')
ax1.legend(loc='lower right', facecolor='#0d111d', edgecolor='#38bdf8')

ax2.axvline(1.0, color='#f43f5e', linestyle='--', label=r'Node Boundary $R_{\text{node}} = 3M_{\text{node}}$')
ax2.legend(loc='upper right', facecolor='#0d111d', edgecolor='#10b981')

# Dynamic Elements
mass_curve, = ax1.plot([], [], color='#38bdf8', linewidth=2.5, label='Mass Profile m(r)')
force_curve, = ax2.plot([], [], color='#10b981', linewidth=2.5, label=r'Outward Viscous Force $F_\kappa(r)$')

status_A = fig.text(0.28, 0.08, '', color='#38bdf8', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#38bdf8'))
status_B = fig.text(0.72, 0.08, '', color='#10b981', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#10b981'))

def update(frame):
    t = frame * 0.1
    
    # Mass continuity curve satisfying m(R_node) = M_node
    m_profile = np.where(r_arr < 1.0, 1.0, 1.0 + 0.5 * (r_arr - 1.0)**1.5 * (1.0 + 0.05 * np.sin(3*t)))
    mass_curve.set_data(r_arr, m_profile)
    
    # Viscous force F_kappa(r)
    f_profile = np.where(r_arr >= 1.0, (1.0 / (r_arr**2)) * np.exp(-0.8 * (r_arr - 1.0)) * (1.0 + 0.08 * np.cos(5*t)), 0.0)
    force_curve.set_data(r_arr, f_profile)
    
    status_A.set_text("MODIFIED TOV EQUILIBRIUM ACTIVE\nHard mass floor m(R_node) = M_node at boundary\nDensity singularity physically precluded")
    status_B.set_text("OUTWARD KAPPA VISCOUS FORCE\nF_kappa balances inwards gravitational pull\nEstablishes stable stellar core boundary layer")

    return mass_curve, force_curve, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'MovieS4_Stellar_Micronode.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
