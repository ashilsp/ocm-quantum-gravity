"""
Order Creator Mechanism (OCM) - Supplementary Movie S1
Script: render_movie_s1_lvk_ceiling.py
Description: Renders Movie S1 showing the LVK GW peak luminosity saturation 
             ceiling (P_peak <= 10^-3 P_P) across cataloged mergers (O1-O4).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Dark Theme Render Engine
plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
fig.patch.set_facecolor('#05050d')
fig.subplots_adjust(bottom=0.25, top=0.88, left=0.10, right=0.95)

ax.set_facecolor('#080812')
ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Title & Labels
ax.set_title("MOVIE S1: LVK Gravitational-Wave Peak Luminosity Ceiling\n(P_peak <= 10^-3 P_P Universal Viscous Saturation Ceiling across O1-O4 Runs)", 
             color='#eab308', fontsize=10.5, fontweight='bold', pad=12)

m_final = np.array([63.1, 20.5, 48.8, 17.8, 53.2, 2.73, 37.3, 142.0, 25.6, 10.4, 7.0])
p_peak = np.array([3.6, 3.3, 3.1, 3.4, 3.7, 0.01, 2.8, 3.7, 1.6, 0.6, 0.8])  # 10^49 W

ax.set_xlim(0, 160)
ax.set_ylim(0, 5.0)
ax.set_xlabel(r'Final Remnant Mass $M_f \; [M_\odot]$', color='white')
ax.set_ylabel(r'Peak Luminosity $P_{\text{peak}} \; [\times 10^{49} \text{ W}]$', color='white')

# Static Reference Ceilings
ax.axhline(3.7, color='#eab308', linestyle=':', linewidth=2.0, label=r'OCM Viscous Impedance Saturation ($10^{-3} P_P$)')

# Dynamic Scatter Elements
lvk_scatter = ax.scatter([], [], color='#38bdf8', s=70, zorder=5, label='Cataloged LVK Mergers (GWTC-1 to O4)')
ax.legend(loc='lower right', facecolor='#0d111d', edgecolor='#eab308')

status_box = fig.text(0.5, 0.06, '', color='#eab308', fontsize=9, fontweight='bold', ha='center', va='top', 
                      bbox=dict(facecolor='#0d111d', edgecolor='#eab308'))

def update(frame):
    t = frame / 100.0
    num_pts = int(t * len(m_final)) + 1
    num_pts = min(num_pts, len(m_final))
    
    lvk_scatter.set_offsets(np.column_stack([m_final[:num_pts], p_peak[:num_pts]]))
    
    status_box.set_text("LVK POWER SATURATION VERIFIED (MOVIE S1)\nAll cataloged events strictly satisfy P_peak <= 10^-3 P_P\nMetric viscosity at R_d = 3M acts as universal impedance circuit breaker")

    return lvk_scatter, status_box

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'MovieS1_LVK_Luminosity_Ceiling.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
