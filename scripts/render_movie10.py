import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# High-Resolution Dark Theme
plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(9, 8), dpi=150)
fig.patch.set_facecolor('#05050d')
ax.set_facecolor('#080812')
ax.set_aspect('equal')
ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Title & Bounds
ax.set_title("MOVIE 10: Resolution of Missing Pulsar Paradox\n(Pulsar-to-Magnetar Transmutation & Flux Compression)", 
             color='#a855f7', fontsize=10, fontweight='bold', pad=12)
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_xlabel(r'Radial Radius $r/R_{\mathrm{NS}}$', color='white')
ax.set_ylabel(r'Transverse Radius $y/R_{\mathrm{NS}}$', color='white')

# Core Boundaries
ns_boundary = plt.Circle((0, 0), 2.5, color='#3b82f6', alpha=0.15, fill=True)
ax.add_patch(ns_boundary)
rd_shell = plt.Circle((0, 0), 0.4, color='#ef4444', fill=False, linewidth=2.0)
ax.add_patch(rd_shell)

# Field Lines
theta = np.linspace(0, 2*np.pi, 200)
field_lines = [ax.plot([], [], color='#ec4899', linewidth=1.5, alpha=0.8)[0] for _ in range(6)]

# Burst Flares
burst_lines = [ax.plot([], [], color='#f59e0b', linewidth=2.0, linestyle='--')[0] for _ in range(4)]

status_box = fig.text(0.5, 0.05, '', color='#a855f7', fontsize=9, fontweight='bold', ha='center', va='bottom', 
                      bbox=dict(facecolor='#0d111d', edgecolor='#a855f7'))

def update(frame):
    t = frame * 0.1
    comp = 1.0 + 0.1 * (t % 30)
    
    # Dynamic Field Compression
    for idx, line in enumerate(field_lines):
        r_scale = (0.6 + 0.3 * idx) / comp
        x = r_scale * np.cos(theta)
        y = (r_scale * 0.5) * np.sin(theta)
        line.set_data(x, y)
        
    # Reconnection Energy Burst
    burst_active = (t % 30) > 20
    for idx, line in enumerate(burst_lines):
        if burst_active:
            angle = idx * np.pi / 2.0
            r_vec = np.linspace(0.4, 3.2, 50)
            x = r_vec * np.cos(angle) + 0.1 * np.sin(10 * r_vec)
            y = r_vec * np.sin(angle) + 0.1 * np.cos(10 * r_vec)
            line.set_data(x, y)
        else:
            line.set_data([], [])
            
    B_val = 1.0e12 * (comp**2)
    status_text = (f"PBH CORE CAPTURE AT R_d = 3M\n"
                   f"Flux Conservation Phi_B = const | B_Rd = {B_val:.2e} Gauss\n"
                   f"Radio Beaming Quenched | Magnetar FRB Outburst Active: {burst_active}")
    status_box.set_text(status_text)
    
    return field_lines + burst_lines + [status_box]

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie10_Missing_Pulsar_Transmutation.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
