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
ax1.set_title("MOVIE 15: Classical GR Singular Collapse\n(Continuous Inflow, Infinite Density rho -> inf, Divide-by-Zero)", 
              color='#ef4444', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 15: OCM Quantized Hardware Floor\n(Packetized Discrete Inflow at t_P, Propped Open by l_P Floor)", 
              color='#14b8a6', fontsize=10, fontweight='bold', pad=12)

# Subplot Setups
ax1.set_xlim(-3.0, 3.0)
ax1.set_ylim(-3.0, 3.0)
ax1.set_xlabel(r'Radial Axis $r/R_d$', color='white')
ax1.set_ylabel(r'Conduit Depth $z$', color='white')

ax2.set_xlim(-3.0, 3.0)
ax2.set_ylim(-3.0, 3.0)
ax2.set_xlabel(r'Radial Axis $r/R_d$', color='white')
ax2.set_ylabel(r'Conduit Depth $z$', color='white')

# Static Elements Subplot 1 (GR Funnel)
z_gr = np.linspace(-2.5, 2.5, 200)
x_gr_left = -0.5 * (z_gr + 2.6)**0.7
x_gr_right = 0.5 * (z_gr + 2.6)**0.7
ax1.plot(x_gr_left, z_gr, color='#ef4444', linewidth=1.5)
ax1.plot(x_gr_right, z_gr, color='#ef4444', linewidth=1.5)
ax1.scatter([0], [-2.5], color='#ef4444', s=100, zorder=5, label='Singularity r=0')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#ef4444')

# Static Elements Subplot 2 (OCM Quantized Bridge)
z_ocm = np.linspace(-2.5, 2.5, 200)
x_ocm_left = -1.0 - 0.3 * (z_ocm + 2.5)**0.8
x_ocm_right = 1.0 + 0.3 * (z_ocm + 2.5)**0.8
ax2.plot(x_ocm_left, z_ocm, color='#14b8a6', linewidth=2.0)
ax2.plot(x_ocm_right, z_ocm, color='#14b8a6', linewidth=2.0)
ax2.axhline(y=-2.5, xmin=0.33, xmax=0.67, color='#a855f7', linewidth=4.0, label=r'Geometric Floor $\ell_P$')
ax2.legend(loc='upper right', facecolor='#0d111d', edgecolor='#14b8a6')

# Dynamic Elements
gr_stream, = ax1.plot([], [], color='#f87171', linewidth=2.5)
ocm_packets, = ax2.plot([], [], 'o', color='#38bdf8', markersize=8, label='Quantized Packets')

status_A = fig.text(0.28, 0.08, '', color='#ef4444', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ef4444'))
status_B = fig.text(0.72, 0.08, '', color='#14b8a6', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#14b8a6'))

def update(frame):
    t = frame * 0.1
    
    # GR Continuous Flow
    z_stream = np.linspace(2.5, -2.5, 100)
    x_stream = np.zeros_like(z_stream)
    gr_stream.set_data(x_stream, z_stream)
    
    # OCM Discrete Packetized Flow
    packet_z = np.array([2.5 - ((frame * 0.15 + i * 0.7) % 5.0) for i in range(7)])
    packet_z = packet_z[packet_z >= -2.5]
    packet_x = np.zeros_like(packet_z)
    ocm_packets.set_data(packet_x, packet_z)
    
    status_A.set_text("CLASSICAL CONTINUOUS COLLAPSE\nInfinite density rho -> inf at r -> 0\nUnbounded acceleration a -> inf (Mathematical singularity)")
    status_B.set_text(f"OCM QUANTIZED HARDWARE FLOOR\nShutter refresh t_P = 5.39e-44 s | Floor l_P = 1.61e-35 m\nCasimir r^-4 pressure props throat open | Finite density rho_max")

    return gr_stream, ocm_packets, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie15_SpatioTemporal_Quantization.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
