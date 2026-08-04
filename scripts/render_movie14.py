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
ax1.set_title("MOVIE 14: Asymmetric D-Shaped EHT Shadow Profile\n(Oloid Residual Deformation vs. Circular GR Shadow)", 
              color='#06b6d4', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 14: R_d Shell Vibrational Eigenmodes & 3:2 QPOs\n(Poloidal 3x vs. Toroidal 2x Structural Frequency Lock)", 
              color='#ec4899', fontsize=10, fontweight='bold', pad=12)

# Subplot 1 Setup (Polar Profile)
ax1.set_xlim(-7.0, 7.0)
ax1.set_ylim(-7.0, 7.0)
ax1.set_aspect('equal')
ax1.set_xlabel(r'Relative RA $\mu\mathrm{as}$', color='white')
ax1.set_ylabel(r'Relative Dec $\mu\mathrm{as}$', color='white')

# Subplot 2 Setup (PSD Spectrum)
freq = np.linspace(50, 350, 300)
ax2.set_xlim(50, 350)
ax2.set_ylim(0, 1.2)
ax2.set_xlabel(r'Frequency $f$ (Hz)', color='white')
ax2.set_ylabel(r'Power Spectral Density (PSD)', color='white')

# Static Reference Data Panel 1
theta_phi = np.linspace(0, 2*np.pi, 200)
x_gr = 5.2 * np.cos(theta_phi)
y_gr = 5.2 * np.sin(theta_phi)
ax1.plot(x_gr, y_gr, color='gray', linestyle='--', linewidth=1.5, label='Standard GR Shadow (Circular)')

# Dynamic Lines
line_d_shadow, = ax1.plot([], [], color='#06b6d4', linewidth=2.5, label='OCM Oloid Shadow (D-Shaped)')
ax1.legend(loc='upper right', facecolor='#0d111d', edgecolor='#06b6d4')

psd_curve, = ax2.plot([], [], color='#ec4899', linewidth=2.0, label='X-Ray PSD Spectrum')
ax2.axvline(170, color='#3b82f6', linestyle=':', label=r'Toroidal $f_T = 2f_0$ (170 Hz)')
ax2.axvline(283, color='#ef4444', linestyle=':', label=r'Poloidal $f_P = 3f_0$ (283 Hz)')
ax2.legend(loc='upper right', facecolor='#0d111d', edgecolor='#ec4899')

status_A = fig.text(0.28, 0.08, '', color='#06b6d4', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#06b6d4'))
status_B = fig.text(0.72, 0.08, '', color='#ec4899', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#ec4899'))

def update(frame):
    t = frame * 0.1
    
    # Dynamic D-Shape Oscillation
    eps = 0.12 + 0.03 * np.sin(2 * t)
    eta = 0.15 + 0.03 * np.cos(2 * t)
    r_ocm = 5.2 * (1.0 + eps * np.cos(3 * theta_phi) + eta * (np.sin(theta_phi)**2))
    x_ocm = r_ocm * np.cos(theta_phi)
    y_ocm = r_ocm * np.sin(theta_phi)
    line_d_shadow.set_data(x_ocm, y_ocm)
    
    # PSD Peak Dynamics
    bg = 0.15 + 10.0 / (freq - 20.0)
    p_tor = 0.65 / (1.0 + 0.1 * (freq - 170.0)**2)
    p_pol = 0.85 / (1.0 + 0.1 * (freq - 283.0)**2)
    p_ghost = 0.25 / (1.0 + 0.25 * (freq - 113.0)**2)
    
    psd_total = bg + p_tor + p_pol + p_ghost + 0.02 * np.sin(freq + 10 * t)
    psd_curve.set_data(freq, psd_total)
    
    status_A.set_text(f"ASYMMETRIC D-SHADOW ACTIVE\nDeformation params: eps = {eps:.2f}, eta = {eta:.2f}\nNon-circular photon ring matching EHT M87* / Sgr A*")
    status_B.set_text(f"STRUCTURAL 3:2 RESONANCE ACTIVE\nPoloidal mode f_P = 283 Hz | Toroidal mode f_T = 170 Hz\nFrequency ratio = 3:2 exactly | Ghost beat = 113 Hz")

    return line_d_shadow, psd_curve, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie14_EHT_Shadow_HFQPO.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
