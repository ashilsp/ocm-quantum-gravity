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
ax1.set_title("MOVIE 17: Radial Stress Balance & Triple-Point Equilibrium\n(Gravitational Stress vs. F_OCM Tensile Locking at r = R_d)", 
              color='#ef4444', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 17: Dynamic Impedance Damping & Core Incompressibility\n(Z_man Viscous Damping & p_P Bulk Modulus Pressure Cushion)", 
              color='#14b8a6', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup
ax1.set_xlim(-4.0, 4.0)
ax1.set_ylim(-4.0, 4.0)
ax1.set_aspect('equal')
ax1.set_xlabel(r'Spatial Axis $x/R_d$', color='white')
ax1.set_ylabel(r'Spatial Axis $y/R_d$', color='white')

# Subplot 2 Setup
r_vals = np.linspace(0.5, 4.0, 300)
ax2.set_xlim(0.5, 4.0)
ax2.set_ylim(0, 1.2)
ax2.set_xlabel(r'Radial Distance $r/R_d$', color='white')
ax2.set_ylabel(r'Normalized Pressure & Damping Factor', color='white')

# Static Elements Subplot 1
angles = np.linspace(0, 2*np.pi, 200)
x_shell = 2.2 * np.cos(angles)
y_shell = 2.2 * np.sin(angles)
ax1.plot(x_shell, y_shell, color='#ef4444', linewidth=2.5, linestyle='--', label=r'Boundary Shell $r = R_d$')
ax1.scatter([0], [0], color='#f97316', s=250, zorder=5, label=r'Incompressible Core ($p_P$)')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#ef4444')

# Static Elements Subplot 2
ax2.axvline(1.0, color='#ef4444', linestyle='--', label=r'Interface $r = R_d$')
p_curve, = ax2.plot([], [], color='#f97316', linewidth=2.5, label=r'Bulk Modulus Cushion ($p_P$)')
z_curve, = ax2.plot([], [], color='#14b8a6', linewidth=2.0, linestyle=':', label=r'Viscous Damping Envelope ($Z_{\mathrm{man}}$)')
ax2.legend(loc='upper right', facecolor='#0d111d', edgecolor='#14b8a6')

# Dynamic Elements Subplot 1
inward_arrows = []
for a in np.linspace(0, 2*np.pi, 8, endpoint=False):
    line, = ax1.plot([], [], color='#3b82f6', linewidth=2.0)
    inward_arrows.append((a, line))

status_A = fig.text(0.28, 0.08, '', color='#ef4444', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ef4444'))
status_B = fig.text(0.72, 0.08, '', color='#14b8a6', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#14b8a6'))

def update(frame):
    t = frame * 0.1
    
    # Update Radial Arrows
    pulse = 0.2 * np.sin(3 * t)
    for a, line in inward_arrows:
        r_start = 3.5 + pulse
        r_end = 2.3
        x_pts = [r_start * np.cos(a), r_end * np.cos(a)]
        y_pts = [r_start * np.sin(a), r_end * np.sin(a)]
        line.set_data(x_pts, y_pts)
        
    # Update Pressure & Damping Curves
    p_profile = np.exp(-10.0 * (r_vals - 1.0)**2) * (1.0 + 0.05 * np.sin(5 * t))
    z_profile = 0.8 * np.exp(-2.0 * abs(r_vals - 1.0)) * (1.0 + 0.02 * np.cos(5 * t))
    
    p_curve.set_data(r_vals, p_profile)
    z_curve.set_data(r_vals, z_profile)
    
    status_A.set_text("TRIPLE-POINT TENSILE LOCKING ACTIVE\nInward gravity F_g balanced by F_OCM = c^4 / G = 1.21e44 N\nRadial shell geometry locked at r = R_d = 3M")
    status_B.set_text("BULK MODULUS & DAMPING ACTIVE\nPlanck Pressure p_P = 4.63e113 Pa prevents core collapse\nImpedance Z_man = 2.50e70 Pa.s damps metric turbulence")

    return [line for _, line in inward_arrows] + [p_curve, z_curve, status_A, status_B]

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie17_Mechanical_Triple_Point.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
