import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Dark Theme Render Engine ---
plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.8), dpi=150)
fig.patch.set_facecolor('#05050d')
fig.subplots_adjust(bottom=0.35, top=0.88, wspace=0.25, left=0.06, right=0.95)

for ax in (ax1, ax2):
    ax.set_facecolor('#080812')
    ax.set_aspect('equal')
    ax.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Titles
ax1.set_title("MOVIE 8: Thermonuclear R_d Sparking Mechanism\n(Sub-Chandrasekhar Type Ia Supernova Trigger)", color='#ff5555', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 9: Pulsar-to-Magnetar Transmutation\n(Flux Compression & FRB Gamma Outbursts)", color='#aa55ff', fontsize=10, fontweight='bold', pad=12)

# Panel Limits
ax1.set_xlim(-3.5, 3.5)
ax1.set_ylim(-3.5, 3.5)
ax2.set_xlim(-3.5, 3.5)
ax2.set_ylim(-3.5, 3.5)

# Background Structures
wd_core = plt.Circle((0, 0), 2.8, color='#0284c7', alpha=0.2, linestyle='--', linewidth=1.5, fill=True)
ax1.add_patch(wd_core)

ns_core = plt.Circle((0, 0), 2.5, color='#7e22ce', alpha=0.2, linestyle='--', linewidth=1.5, fill=True)
ax2.add_patch(ns_core)

# Dynamic Elements
spark_front = plt.Circle((0, 0), 0.1, color='#ef4444', fill=False, linewidth=2.5)
ax1.add_patch(spark_front)

pbh_node_1 = plt.Circle((0, 0), 0.3, color='#f59e0b', fill=True)
ax1.add_patch(pbh_node_1)

pbh_node_2 = plt.Circle((0, 0), 0.25, color='#ef4444', fill=True)
ax2.add_patch(pbh_node_2)

# Magnetic field loops for Panel B
theta_vals = np.linspace(0, 2*np.pi, 200)
field_lines = [ax2.plot([], [], color='#ec4899', linewidth=1.2, alpha=0.8)[0] for _ in range(4)]

status_A = fig.text(0.28, 0.10, '', color='#ff5555', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ff5555'))
status_B = fig.text(0.72, 0.10, '', color='#aa55ff', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#aa55ff'))

def update(frame):
    t = frame * 0.1
    
    # Detonation Wave Expansion in Movie 8
    radius = min(2.8, 0.3 + 0.1 * (t % 25))
    spark_front.set_radius(radius)
    
    # Magnetic Flux Compression in Movie 9
    comp_factor = min(2.0, 0.5 + 0.05 * t)
    for idx, line in enumerate(field_lines):
        r_scale = (0.8 + 0.4 * idx) / comp_factor
        x = r_scale * np.cos(theta_vals)
        y = (r_scale * 0.5) * np.sin(theta_vals)
        line.set_data(x, y)
        
    status_A.set_text(f"QUANTUM REFLECTION AT R_d ACTIVE\nLocal temperature T_Rd = {1.2 + 0.1*t:.2f}e9 K > T_ign\nOutward Carbon Detonation Wave Front = {radius:.2f} R_WD")
    status_B.set_text(f"PBH CORE CAPTURE IN PROGRESS\nMagnetic flux compressed: B_Rd > 10^15 Gauss\nRadio beaming quenched -> Magnetar FRB burst active")

    return [spark_front, pbh_node_1, pbh_node_2, status_A, status_B] + field_lines

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'MovieS8_S9_Spark_Transmutation.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
