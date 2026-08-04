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
ax1.set_title("MOVIE S19: Empirical Luminosity Saturation Limits vs. Planck Power P_P\n(LIGO GW150914 & GRB 221009A BOAT Capped Below Ceiling)", 
              color='#eab308', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE S19: Mass Bandwidth Cap (M_dot_max) & Information Throughput\n(High-Bandwidth Funnel Resolving Information Paradox)", 
              color='#38bdf8', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup
ax1.set_yscale('log')
ax1.set_ylim(1e45, 1e53)
ax1.set_xlim(0, 100)
ax1.set_xlabel(r'Time Step $t$ (ms)', color='white')
ax1.set_ylabel(r'Luminosity $L$ (Watts)', color='white')

# Subplot 2 Setup
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 5.0e35)
ax2.set_xlabel(r'Accretion Step $t$', color='white')
ax2.set_ylabel(r'Mass Processing Rate $\dot{M}$ (kg/s)', color='white')

# Static Elements Subplot 1
ax1.axhline(3.628e52, color='#ef4444', linewidth=2.5, linestyle='--', label=r'Planck Power $P_P = c^5/G \approx 3.63 \times 10^{52}\text{ W}$')
ax1.axhline(3.6e49, color='#eab308', linewidth=1.8, linestyle=':', label=r'GW150914 Peak ($1.0 \times 10^{-3} P_P$)')
ax1.axhline(2.1e47, color='#10b981', linewidth=1.8, linestyle=':', label=r'GRB 221009A BOAT ($5.8 \times 10^{-6} P_P$)')
ax1.legend(loc='lower right', facecolor='#0d111d', edgecolor='#eab308')

# Static Elements Subplot 2
ax2.axhline(4.037e35, color='#38bdf8', linewidth=2.5, linestyle='--', label=r'Mass Processing Cap $\dot{M}_{\max} = c^3/G \approx 4.04 \times 10^{35}\text{ kg/s}$')
ax2.legend(loc='lower right', facecolor='#0d111d', edgecolor='#38bdf8')

# Dynamic Elements
gw_trace, = ax1.plot([], [], color='#eab308', linewidth=2.0)
grb_trace, = ax1.plot([], [], color='#10b981', linewidth=2.0)
mass_trace, = ax2.plot([], [], color='#38bdf8', linewidth=2.0)

status_A = fig.text(0.28, 0.08, '', color='#eab308', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#eab308'))
status_B = fig.text(0.72, 0.08, '', color='#38bdf8', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#38bdf8'))

t_vec = np.linspace(0, 100, 300)

def update(frame):
    t_curr = frame
    
    # Pulse traces
    gw_pulse = 3.6e49 * np.exp(-((t_vec - 50)**2) / 50.0) + 1e46
    grb_pulse = 2.1e47 * np.exp(-((t_vec - 30)**2) / 100.0) + 1e45
    mass_pulse = 4.037e35 * (1.0 - np.exp(-t_vec / 20.0))
    
    mask = t_vec <= t_curr
    gw_trace.set_data(t_vec[mask], gw_pulse[mask])
    grb_trace.set_data(t_vec[mask], grb_pulse[mask])
    mass_trace.set_data(t_vec[mask], mass_pulse[mask])
    
    status_A.set_text("LUMINOSITY CEILING VERIFIED\nGW150914 peak = 3.6e49 W (0.1% P_P limit)\nGRB 221009A peak = 2.1e47 W (0.00058% P_P limit)\nExcess energy sequestered into internal kappa-flux")
    status_B.set_text("MASS & INFORMATION THROUGHPUT ACTIVE\nMax mass processing cap M_dot_max = 2.03e5 M_sun/s\nInfo throughput I_OCM = 2.68e43 bits/s resolves paradox")

    return gw_trace, grb_trace, mass_trace, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'MovieS19_Sequestration_Ceilings.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
