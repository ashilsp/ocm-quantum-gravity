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
ax1.set_title("MOVIE 18: Microscopic Planck Frame Rate & Heisenberg Floor\n(Geometric Bell Vibration f_OCM = 1.85e43 Hz & Zero-Point Cushion)", 
              color='#06b6d4', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 18: Macro-Scale Sub-Harmonic GW Echo Cascade\n(Cavity Downscaling f_n = f_OCM / N_n -> kHz Echoes)", 
              color='#a855f7', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup
ax1.set_xlim(-3.0, 3.0)
ax1.set_ylim(-3.0, 3.0)
ax1.set_aspect('equal')
ax1.set_xlabel(r'Spatial Axis $x/R_d$', color='white')
ax1.set_ylabel(r'Spatial Axis $y/R_d$', color='white')

# Subplot 2 Setup
time_pts = np.linspace(0, 50, 500)
ax2.set_xlim(0, 50)
ax2.set_ylim(-1.2, 1.2)
ax2.set_xlabel(r'Post-Merger Time $\Delta t$ (ms)', color='white')
ax2.set_ylabel(r'Strain Amplitude $h(t)$', color='white')

# Static Elements Subplot 1
angles = np.linspace(0, 2*np.pi, 200)
x_rd = 2.0 * np.cos(angles)
y_rd = 2.0 * np.sin(angles)
ax1.plot(x_rd, y_rd, color='#ef4444', linewidth=2.5, linestyle='--', label=r'Cavity Boundary $r = R_d = 3M$')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#ef4444')

# Dynamic Elements
micro_ripples, = ax1.plot([], [], color='#06b6d4', linewidth=1.5, alpha=0.8)
macro_echo, = ax2.plot([], [], color='#a855f7', linewidth=2.0, label='GW Post-Merger Echoes (kHz)')
ax2.legend(loc='upper right', facecolor='#0d111d', edgecolor='#a855f7')

status_A = fig.text(0.28, 0.08, '', color='#06b6d4', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#06b6d4'))
status_B = fig.text(0.72, 0.08, '', color='#a855f7', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#a855f7'))

def update(frame):
    t = frame * 0.1
    
    # Microscopic High-Frequency Oscillations
    r_micro = 1.0 + 0.15 * np.sin(20 * angles - 10 * t)
    x_micro = r_micro * np.cos(angles)
    y_micro = r_micro * np.sin(angles)
    micro_ripples.set_data(x_micro, y_micro)
    
    # Macro GW Echo Waveform
    echo_signal = np.exp(-time_pts / 20.0) * np.sin(0.8 * time_pts) * (1.0 + 0.3 * np.sin(0.15 * time_pts - t))
    macro_echo.set_data(time_pts, echo_signal)
    
    status_A.set_text("GEOMETRIC BELL ACTIVE\nPlanck frame rate f_OCM = 1.85e43 Hz\nHeisenberg zero-point energy floor Delta_E = 0.5 E_P prevents singularity")
    status_B.set_text("SUB-HARMONIC GW ECHOES ACTIVE\nMicro f_OCM downscaled by quantum mode number N_n\nMacro echoes at f_n ~ 1.2 kHz observing trapped cavity resonance")

    return micro_ripples, macro_echo, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie18_Geometric_Bell_Heisenberg.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
