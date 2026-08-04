import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Dark Theme Render Engine ---
plt.style.use('dark_background')

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.8), dpi=150)
fig.patch.set_facecolor('#05050d')
fig.subplots_adjust(bottom=0.28, top=0.85, wspace=0.25, left=0.05, right=0.96)

for ax in (ax1, ax2, ax3):
    ax.set_facecolor('#080812')
    ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Titles
ax1.set_title("PANEL A: WKB Barrier Penetration", color='#00ffd2', fontsize=9, fontweight='bold', pad=10)
ax2.set_title("PANEL B: Accretion Saturation Bounds", color='#ffaa00', fontsize=9, fontweight='bold', pad=10)
ax3.set_title(r"PANEL C: UV Resolution ($n=1 \to |0\rangle$)", color='#ff55ff', fontsize=9, fontweight='bold', pad=10)

# Panel A setup
r_grid = np.linspace(0.5, 6.5, 300)
V_eff = 0.4 * (r_grid - 2.2)**2 + 1.8 / (r_grid**2) + 0.5
ax1.plot(r_grid, V_eff, color='#3b82f6', linewidth=2.5, label=r'$V_{\mathrm{eff}}(r)$')
ax1.axvline(x=2.2, color='#ef4444', linestyle='--', linewidth=1.5, label=r'$R_d = 3M$')
ax1.set_xlim(0.5, 6.5)
ax1.set_ylim(0, 4.5)
ax1.set_xlabel(r'Radial Radius $r$', color='white')
ax1.set_ylabel(r'Potential $V_{\mathrm{eff}}(r)$', color='white')
ax1.legend(loc='upper right', facecolor='#0d111d')

# Panel B setup
M_grid = np.linspace(0, 6.5, 200)
ax2.plot(M_grid, 0.45 * M_grid**2, color='gray', linestyle='--', linewidth=1.5, label=r'Classical GR ($\dot{M} \propto M^2$)')
ax2.axhline(y=2.4, color='#ef4444', linestyle='--', linewidth=1.5, label=r'$\dot{M}_{\max} = c^3/G$')
ax2.set_xlim(0, 6.5)
ax2.set_ylim(0, 4.2)
ax2.set_xlabel(r'PBH Mass $M$', color='white')
ax2.set_ylabel(r'Accretion Rate $\dot{M}$', color='white')
ax2.legend(loc='upper left', facecolor='#0d111d')

# Panel C setup
ax3.axhline(y=3.6, color='white', linewidth=1.5, label=r'$n=3$')
ax3.axhline(y=2.6, color='white', linewidth=1.5, label=r'$n=2$')
ax3.axhline(y=1.4, color='#ef4444', linewidth=2, label=r'$n=1$ ($E_1 = E_P$)')
ax3.axhline(y=0.2, color='#3b82f6', linestyle='--', linewidth=1.5, label=r'$|0\rangle$ Vacuum')
ax3.set_xlim(0, 5)
ax3.set_ylim(-0.5, 4.5)
ax3.set_xlabel(r'State Transition Axis', color='white')
ax3.set_ylabel(r'Energy Level $E$', color='white')
ax3.legend(loc='upper right', facecolor='#0d111d')

# Animated Lines
line_ocm_acc, = ax2.plot([], [], color='#ef4444', linewidth=2.5, label='OCM Saturation')
burst_point, = ax3.plot([], [], 'o', color='#f59e0b', markersize=10)

def update(frame):
    t = frame * 0.1
    
    # Panel B saturation curve build
    mask = M_grid <= min(6.5, t)
    ocm_curve = np.minimum(0.45 * M_grid[mask]**2, 2.4)
    line_ocm_acc.set_data(M_grid[mask], ocm_curve)
    
    # Panel C transition drop
    y_pos = max(0.2, 1.4 - 0.2 * (t % 10))
    burst_point.set_data([2.5], [y_pos])
    
    return line_ocm_acc, burst_point

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie7_PBH_Micro_Quantum_Dynamics.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
