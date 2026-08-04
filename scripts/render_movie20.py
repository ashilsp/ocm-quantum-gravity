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
ax1.set_title("MOVIE 20: Dual-Layered Scale Hierarchy (R_d -> l_P Bridge)\n(Macroscopic Fluid Filter at R_d & Geometric Floor at l_P)", 
              color='#6366f1', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 20: Inverse-Quartic kappa-Flux Density & Phase Transcoding\n(Energy Scaling E_kappa ~ r^-4 & Baryonic-to-Quantized Transition)", 
              color='#ec4899', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup
ax1.set_xlim(-3.0, 3.0)
ax1.set_ylim(-3.0, 3.0)
ax1.set_aspect('equal')
ax1.set_xlabel(r'Spatial Axis $x/R_d$', color='white')
ax1.set_ylabel(r'Spatial Axis $y/R_d$', color='white')

# Subplot 2 Setup
r_space = np.logspace(-2, 1, 300)
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlim(1e-2, 10)
ax2.set_ylim(1e-2, 1e8)
ax2.set_xlabel(r'Normalized Radius $r/R_d$', color='white')
ax2.set_ylabel(r'Normalized Energy Density $\rho_\kappa / \rho_0$', color='white')

# Static Elements Subplot 1
angles = np.linspace(0, 2*np.pi, 200)
x_rd = 2.0 * np.cos(angles)
y_rd = 2.0 * np.sin(angles)
ax1.plot(x_rd, y_rd, color='#6366f1', linewidth=2.5, linestyle='--', label=r'Operational Boundary $R_d = 3M$')
ax1.scatter([0], [0], color='#ec4899', s=120, zorder=5, label=r'Planck Floor $l_P$')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#6366f1')

# Static Elements Subplot 2
ax2.axvline(1.0, color='#6366f1', linestyle='--', label=r'Operational Boundary $r = R_d$')
ax2.axvline(0.01, color='#ec4899', linestyle=':', label=r'Planck Floor $r = l_P$')

# Dynamic Elements
inflowing_particles, = ax1.plot([], [], 'o', color='#38bdf8', markersize=5, label='Infalling Mass Quanta')
kappa_curve, = ax2.plot([], [], color='#ec4899', linewidth=2.5, label=r'kappa-Flux Profile $E_\kappa \propto r^{-4}$')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#6366f1')
ax2.legend(loc='upper right', facecolor='#0d111d', edgecolor='#ec4899')

status_A = fig.text(0.28, 0.08, '', color='#6366f1', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#6366f1'))
status_B = fig.text(0.72, 0.08, '', color='#ec4899', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ec4899'))

# Initial Particle Positions
np.random.seed(42)
p_radii = np.random.uniform(0.1, 2.8, 60)
p_angles = np.random.uniform(0, 2*np.pi, 60)

def update(frame):
    t = frame * 0.05
    
    # Inward spiraling particle motion
    r_curr = np.mod(p_radii - 0.2 * t, 2.8) + 0.02
    x_p = r_curr * np.cos(p_angles + t)
    y_p = r_curr * np.sin(p_angles + t)
    inflowing_particles.set_data(x_p, y_p)
    
    # Update Kappa Flux Profile
    rho_profile = (1.0 / (r_space + 1e-3))**4 * (1.0 + 0.1 * np.sin(5 * t))
    kappa_curve.set_data(r_space, rho_profile)
    
    status_A.set_text("SCALE BRIDGING ACTIVE\nR_d = 3M acts as macroscopic fluid filter\nl_P = 1.62e-35 m acts as non-zero spatial floor")
    status_B.set_text("BARYONIC TRANSCODING ACTIVE\nEnergy density scales inverse-quartically (r^-4)\nMass transcoded into quantized Spacetime Steam at floor")

    return inflowing_particles, kappa_curve, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie20_Quantized_Conduit.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
