import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# High-Resolution Dark Theme Render Engine
plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.8), dpi=150)
fig.patch.set_facecolor('#05050d')
fig.subplots_adjust(bottom=0.35, top=0.88, wspace=0.25, left=0.06, right=0.95)

for ax in (ax1, ax2):
    ax.set_facecolor('#080812')
    ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Subplot Titles
ax1.set_title("MOVIE 11: The Violet Limit Gravitational Redshift\n(Local QGP Spectrum vs. Observed Hard X-Ray Band)", 
              color='#a855f7', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 12: OCM Negentropy Information Engine\n(Unitary Entropy Export N = -kappa * dI/dt at R_d = 3M)", 
              color='#14b8a6', fontsize=10, fontweight='bold', pad=12)

# Panel A Limits & Labels
ax1.set_xlim(0.5, 5.5)
ax1.set_ylim(0, 1.2)
ax1.set_xlabel(r'Log Photon Energy $E$', color='white')
ax1.set_ylabel(r'Spectral Radiance $I(E)$', color='white')

# Panel B Limits & Labels
ax2.set_xlim(-3.5, 3.5)
ax2.set_ylim(-2.5, 2.5)
ax2.set_xlabel(r'Spatial Axis $x/R_d$', color='white')
ax2.set_ylabel(r'Internal Mode Coordinate $y$', color='white')

# Static Reference Data Panel A
x_energy = np.linspace(0.5, 5.5, 300)
local_qgp = 1.1 * (x_energy / 4.6)**3 / (np.exp(2.5 * (x_energy / 4.6)) - 1.0 + 0.1)
ax1.plot(x_energy, local_qgp, color='#8b5cf6', linewidth=2.5, label=r'Local Rest Frame ($T_{R_d} \sim 10^{11}\text{ K}$)')
ax1.axvspan(2.5, 3.8, color='#f97316', alpha=0.2, label='Chandra / NuSTAR Band')
ax1.legend(loc='upper left', facecolor='#0d111d', edgecolor='#a855f7')

# Panel B Static Elements
ax2.axvspan(-0.3, 0.3, color='#14b8a6', alpha=0.3, label=r'Engine Boundary $R_d = 3M$')
ax2.legend(loc='upper right', facecolor='#0d111d', edgecolor='#14b8a6')

# Dynamic Graphical Lines
line_redshifted, = ax1.plot([], [], color='#ef4444', linewidth=2.0, linestyle='--', label=r'Observed Spectrum ($1+z_{R_d} = \sqrt{3}$)')
inflow_wave, = ax2.plot([], [], color='#ef4444', linewidth=2.0, label='High-Entropy Inflow')
outflow_wave, = ax2.plot([], [], color='#3b82f6', linewidth=2.0, label='Low-Entropy Coherent Output')
exhaust_pulse, = ax2.plot([], [], color='#f97316', linewidth=2.0, linestyle=':', label=r'X-Ray Exhaust $\Delta E$')

status_A = fig.text(0.28, 0.10, '', color='#a855f7', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#a855f7'))
status_B = fig.text(0.72, 0.10, '', color='#14b8a6', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#14b8a6'))

def update(frame):
    t = frame * 0.1
    
    # Redshift Dynamic Shift
    shift = 4.6 / (1.0 + min(0.732, t * 0.05))
    obs_qgp = 0.65 * (x_energy / shift)**3 / (np.exp(2.5 * (x_energy / shift)) - 1.0 + 0.1)
    line_redshifted.set_data(x_energy, obs_qgp)
    
    # Panel B Flow Animation
    x_in = np.linspace(-3.2, -0.3, 100)
    y_in = 0.5 * np.sin(5 * x_in - 3 * t) + 0.3 * np.cos(12 * x_in + 2 * t)
    inflow_wave.set_data(x_in, y_in)
    
    x_out = np.linspace(0.3, 3.2, 100)
    y_out = 0.8 * np.sin(3 * x_out - 3 * t)
    outflow_wave.set_data(x_out, y_out)
    
    y_ex = np.linspace(0.3, 2.2, 50)
    x_ex = 0.1 * np.sin(10 * y_ex - 4 * t)
    exhaust_pulse.set_data(x_ex, y_ex)
    
    status_A.set_text(f"GRAVITATIONAL REDSHIFT ACTIVE\nRedshift factor 1 + z = {1.0 + min(0.732, t*0.05):.3f} -> sqrt(3)\nPeak shifted into NuSTAR/Chandra X-Ray window")
    status_B.set_text(f"NEGENTROPY ENGINE PROCESSING (t = {t:.1f})\nNegentropy flux N = -kappa * dI/dt active at R_d = 3M\nEntropy expelled as X-ray exhaust | Delta I = 0 (Unitary)")

    return line_redshifted, inflow_wave, outflow_wave, exhaust_pulse, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie11_12_Violet_Limit_Negentropy.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
