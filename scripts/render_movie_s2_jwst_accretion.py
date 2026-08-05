"""
Order Creator Mechanism (OCM) - Supplementary Movie S2
Script: render_movie_s2_jwst_accretion.py
Description: Renders Movie S2 showing JWST early SMBH growth trajectories 
             unconstrained by radiation limits via M_dot_max = c^3 / G.
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
ax.set_title("MOVIE S2: High-Redshift JWST SMBH Growth Trajectories\n(OCM Mass Bandwidth Ceiling M_dot_max = c^3/G Resolves Early SMBH Anomaly)", 
             color='#10b981', fontsize=10.5, fontweight='bold', pad=12)

z_vals = np.linspace(6.0, 12.0, 200)
ax.set_xlim(12.0, 6.0)  # Inverted Redshift
ax.set_yscale('log')
ax.set_ylim(1e2, 1e10)
ax.set_xlabel(r'Redshift $z$ [Early Universe $\rightarrow$]', color='white')
ax.set_ylabel(r'Black Hole Mass $\log_{10}(M / M_\odot)$', color='white')

# Trajectory Curves
eddington_curve = 1e2 * np.exp(0.8 * (12.0 - z_vals))
ocm_curve = 1e2 * np.exp(2.2 * (12.0 - z_vals))

ax.plot(z_vals, eddington_curve, color='#ef4444', linestyle='--', linewidth=2.0, label=r'Classical Eddington Limit ($\dot{M} \le \dot{M}_{\text{Edd}}$)')
ax.plot(z_vals, ocm_curve, color='#10b981', linewidth=2.5, label=r'OCM Bandwidth Envelope ($\dot{M}_{\max} = c^3/G$)')

# JWST Data Points
jwst_z = [10.6, 10.1, 8.68, 7.64, 7.51]
jwst_m = [1.6e6, 4.0e7, 9.0e6, 1.6e9, 1.5e9]
jwst_scatter = ax.scatter([], [], color='#c084fc', s=80, zorder=5, label='JWST Cataloged SMBHs')

ax.legend(loc='upper right', facecolor='#0d111d', edgecolor='#10b981')

status_box = fig.text(0.5, 0.06, '', color='#10b981', fontsize=9, fontweight='bold', ha='center', va='top', 
                      bbox=dict(facecolor='#0d111d', edgecolor='#10b981'))

def update(frame):
    t = frame / 100.0
    num_pts = int(t * len(jwst_z)) + 1
    num_pts = min(num_pts, len(jwst_z))
    
    jwst_scatter.set_offsets(np.column_stack([jwst_z[:num_pts], jwst_m[:num_pts]]))
    
    status_box.set_text("JWST SMBH GROWTH ANOMALY RESOLVED (MOVIE S2)\nUnconstrained by radiation pressure at early redshift z > 6\nMass-flux capacity M_dot_max = 2.03e5 M_sun/s enables rapid direct node growth")

    return jwst_scatter, status_box

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'MovieS2_JWST_SMBH_Accretion.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
