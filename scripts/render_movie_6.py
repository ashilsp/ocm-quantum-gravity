import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Dark Theme Render Engine ---
plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.8), dpi=150)
fig.patch.set_facecolor('#05050d')
fig.subplots_adjust(bottom=0.38, top=0.88, wspace=0.25, left=0.06, right=0.95)

for ax in (ax1, ax2):
    ax.set_facecolor('#080812')
    ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Subplot Titles
ax1.set_title(r"PANEL A: Gravitational Wave Echoes $h(t)$" + "\n" + r"(Sub-Harmonic Reflections off $R_d = 3M$ Cavity)", 
              color='#00ffd2', fontsize=10, fontweight='bold', pad=12)
ax2.set_title(r"PANEL B: Geometric Zeeman Splitting $|h(\omega)|^2$" + "\n" + r"(Rotational Multipole Splitting $\Delta \omega = \Omega_H$)", 
              color='#ff55ff', fontsize=10, fontweight='bold', pad=12)

# Panel A Limits & Labels
ax1.set_xlim(0, 50)
ax1.set_ylim(-1.2, 1.2)
ax1.set_xlabel(r'Post-Merger Time $t$', color='white')
ax1.set_ylabel(r'GW Strain $h(t)$', color='white')

# Panel B Limits & Labels
ax2.set_xlim(0.5, 5.5)
ax2.set_ylim(0, 1.2)
ax2.set_xlabel(r'Frequency $\omega$', color='white')
ax2.set_ylabel(r'Power Spectral Density $|h(\omega)|^2$', color='white')

# Static Reference Elements
t_grid = np.linspace(0, 50, 1000)
w_grid = np.linspace(0.5, 5.5, 500)

# Unsplit QNM Peak (a = 0)
ax2.plot(w_grid, 1.05 / (1 + 25*(w_grid-3.0)**2), color='gray', linestyle='--', alpha=0.7, label=r'$a=0$ Unsplit Peak')

# Legend Anchors
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), facecolor='#0d111d', edgecolor='#00ffd2')
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), facecolor='#0d111d', edgecolor='#ff55ff')

# Dynamic Graphics Lines
line_strain, = ax1.plot([], [], color='#00ffd2', linewidth=2, label=r'OCM Ringdown Echoes')
lines_zeeman = [ax2.plot([], [], color='#ff55ff', linewidth=1.8)[0] for _ in range(5)]

# Telemetry Text
status_A = fig.text(0.28, 0.12, '', color='#00ffd2', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#00ffd2'))
status_B = fig.text(0.72, 0.12, '', color='#ff55ff', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ff55ff'))

def update(frame):
    t_curr = frame * 0.5
    
    # Time-domain wave progressive generation
    mask = t_grid <= t_curr
    tau_ring = 3.0
    h_t = 1.1 * np.exp(-t_grid / tau_ring) * np.cos(1.8 * t_grid)
    
    dt_echo = 14.0
    for i in range(1, 4):
        t_center = i * dt_echo
        amplitude = 0.55 * (0.6 ** (i - 1))
        h_t += amplitude * np.exp(-0.6 * (t_grid - t_center)**2) * np.cos(2.2 * (t_grid - t_center))
        
    line_strain.set_data(t_grid[mask], h_t[mask])
    
    # Dynamic Spin Parameter Ramp (0 to 0.8)
    spin_a = min(0.8, t_curr / 30.0)
    Omega_H = 0.6 * spin_a
    m_modes = [-2, -1, 0, 1, 2]
    
    for idx, m in enumerate(m_modes):
        w_m = 3.0 + m * Omega_H
        amp = 0.90 if m == 0 else (0.65 if abs(m) == 1 else 0.35)
        psd = amp / (1.0 + 45.0 * (w_grid - w_m)**2)
        lines_zeeman[idx].set_data(w_grid, psd)
        
    status_A.set_text(f"CAVITY REFLECTION ACTIVE (t = {t_curr:.1f})\nTrapped mode pulses at intervals dt_echo ~ 2R_d/c\nSub-harmonic pulses 1, 2, 3 generating")
    status_B.set_text(f"KERR SPIN PARAMETER a = {spin_a:.2f}\nRotational Hamiltonian H_rot = -Omega_H * L_z active\nDegenerate QNM peak split into 2l+1 = 5 multipoles")

    return [line_strain, status_A, status_B] + lines_zeeman

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie6_GW_Echoes_Zeeman_Splitting.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
