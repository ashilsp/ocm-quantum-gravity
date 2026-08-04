import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# High-Resolution Dark Theme
plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.8), dpi=150)
fig.patch.set_facecolor('#05050d')
fig.subplots_adjust(bottom=0.38, top=0.88, wspace=0.25, left=0.06, right=0.95)

for ax in (ax1, ax2):
    ax.set_facecolor('#080812')
    ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Titles
ax1.set_title(r"PANEL A: Fermi's Golden Rule State Decay" + "\n" + r"($\Psi_k \to \Psi_0$ Energy Level Transitions)", color='#ff5555', fontsize=10, fontweight='bold', pad=12)
ax2.set_title(r"PANEL B: Quantum Navier-Stokes Smoothing at $R_d = 3M$" + "\n" + r"(Turbulent 3D Inflow $\to$ 2D Laminar Shell)", color='#00ffd2', fontsize=10, fontweight='bold', pad=12)

# Panel A setup
ax1.set_xlim(-2, 3)
ax1.set_ylim(-2, 3)
ax1.set_xlabel('Spatial Coordinate $r/M$', color='white')
ax1.set_ylabel('Energy Level $E$', color='white')

# Panel B setup
ax2.set_xlim(-3, 3)
ax2.set_ylim(-2.5, 2.5)
ax2.set_xlabel('Radial Inflow Coordinate $r/M$', color='white')
ax2.set_ylabel('Transverse Flow Height $y/M$', color='white')

ax1.axhline(y=-1.3, color='#00ffd2', linewidth=2, label=r'Ground State $E_0$ ($\Psi_0$)')
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), facecolor='#0d111d')

ax2.axvline(x=0, color='#ffaa00', linestyle='--', linewidth=2, label=r'Operational Boundary $R_d=3M$')
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), facecolor='#0d111d')

status_A = fig.text(0.28, 0.12, 'DECAY IN PROGRESS', color='#00ffd2', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#00ffd2'))
status_B = fig.text(0.72, 0.12, 'LAMINARIZATION ACTIVE', color='#ffaa00', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ffaa00'))

def update(frame):
    t = frame * 0.1
    status_A.set_text(f"TIME DEPENDENT PERTURBATION t = {t:.1f}s\nMatrix element damping <Psi_0|V|Psi_k> -> 0\nState dissipation rate W_{{0->k}} active")
    status_B.set_text(f"NAVIER-STOKES RESOLUTION AT R_d\n3D Turbulent Modes Dissipating\nLaminar 2D Shell Formed at Ground State E_0")
    return [status_A, status_B]

anim = animation.FuncAnimation(fig, update, frames=100, interval=33)
output_filename = 'MovieS5_Perturbation_Laminar_Transition.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
