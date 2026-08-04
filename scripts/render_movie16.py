import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Dark Theme Render Engine
plt.style.use('dark_background')

fig = plt.figure(figsize=(18, 7.5), dpi=150)
fig.patch.set_facecolor('#05050d')

# Subplot 1: Radial Phase Transition & Hovering Drop
ax1 = fig.add_subplot(121)
ax1.set_facecolor('#080812')
ax1.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Subplot 2: Thermodynamic P-T Phase Diagram
ax2 = fig.add_subplot(122)
ax2.set_facecolor('#080812')
ax2.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Titles
ax1.set_title("MOVIE 16: Microscopic Quantum Leidenfrost Interface at R_d\n(Standing Wave Cushion, Matter Hovering & Packetized Melting)", 
              color='#ef4444', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 16: Spacetime P-T Thermodynamic Phase Diagram\n(E_P Boiling Threshold, Steam Phase & Hawking Condensation)", 
              color='#14b8a6', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup
ax1.set_xlim(-3.0, 3.0)
ax1.set_ylim(-3.0, 3.0)
ax1.set_xlabel(r'Radial Position $r/R_d$', color='white')
ax1.set_ylabel(r'Interface Depth $z$', color='white')

# Subplot 2 Setup
ax2.set_xlim(0, 3.0)
ax2.set_ylim(0, 3.0)
ax2.set_xlabel(r'Energy Density / Temp $T/E_P$', color='white')
ax2.set_ylabel(r'Pressure $P/p_P$', color='white')

# Static Elements Subplot 1
ax1.axhline(0, color='#ef4444', linewidth=2.5, linestyle='--', label=r'Boiling Shell $r = R_d = 3M$')
ax1.fill_between([-3, 3], 0, 3, color='#3b82f6', alpha=0.1, label='Spacetime Ice (Smooth Continuum)')
ax1.fill_between([-3, 3], -3, 0, color='#f97316', alpha=0.15, label='Spacetime Steam (Quantized Phase)')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#ef4444')

# Static Elements Subplot 2
T_axis = np.linspace(0, 2.0, 100)
P_boundary = 0.5 * T_axis**2
ax2.plot(T_axis, P_boundary, color='#14b8a6', linewidth=2.5, label='Ice-Steam Phase Boundary')
ax2.scatter([2.0], [2.0], color='#ef4444', s=120, zorder=5, label=r'Boiling Point ($E_P, p_P$)')
ax2.legend(loc='upper left', facecolor='#0d111d', edgecolor='#14b8a6')

# Dynamic Elements
droplet, = ax1.plot([], [], 'o', color='white', markersize=14, label='Infalling Baryonic Matter')
cushion_wave, = ax1.plot([], [], color='#ef4444', linewidth=2.0)
packet_stream, = ax1.plot([], [], 'v', color='#f97316', markersize=6)

phase_pt, = ax2.plot([], [], 'o', color='#f97316', markersize=10)

status_A = fig.text(0.28, 0.08, '', color='#ef4444', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ef4444'))
status_B = fig.text(0.72, 0.08, '', color='#14b8a6', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#14b8a6'))

x_wave = np.linspace(-3, 3, 200)

def update(frame):
    t = frame * 0.1
    
    # Leidenfrost Hovering Motion
    hover_y = 0.5 + 0.1 * np.sin(3 * t)
    droplet.set_data([0], [hover_y])
    
    # Cushion Standing Wave
    y_wave = 0.2 * np.sin(10 * x_wave - 5 * t) * np.exp(-x_wave**2 / 2.0)
    cushion_wave.set_data(x_wave, y_wave)
    
    # Packetized Melt Stream
    p_y = np.array([0.0 - ((t * 0.5 + i * 0.4) % 2.5) for i in range(6)])
    p_x = np.zeros_like(p_y)
    packet_stream.set_data(p_x, p_y)
    
    # P-T Trajectory
    T_curr = min(0.5 + 0.03 * frame, 2.5)
    P_curr = min(0.125 + 0.02 * frame, 2.5)
    phase_pt.set_data([T_curr], [P_curr])
    
    status_A.set_text(f"QUANTUM LEIDENFROST EFFECT ACTIVE\nHover height y = {hover_y:.2f} R_d above boundary\nStanding wave acoustic cushion preventing direct gravitational collapse")
    status_B.set_text(f"THERMODYNAMIC IGNITION AT E_P\nCurrent State: T/E_P = {T_curr:.2f}, P/p_P = {P_curr:.2f}\nVacuum unzips into quantized conducting steam phase")

    return droplet, cushion_wave, packet_stream, phase_pt, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie16_Leidenfrost_Phase_Transition.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
