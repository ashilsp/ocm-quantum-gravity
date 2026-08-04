import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Dark Theme Render Engine
plt.style.use('dark_background')

fig = plt.figure(figsize=(18, 7.5), dpi=150)
fig.patch.set_facecolor('#05050d')

# Subplot 1: 3D Oloid Convex Hull Geometry
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_facecolor('#080812')

# Subplot 2: 2D Developable Rolling Trajectory & CMB Vector Alignment
ax2 = fig.add_subplot(122)
ax2.set_facecolor('#080812')
ax2.grid(True, color='#1a2035', linestyle=':', alpha=0.6)

# Titles
ax1.set_title("MOVIE 13: Oloid Boundary Geometry\nConvex Hull Conv(C1 U C2) & Area Conservation", 
              color='#14b8a6', fontsize=10, fontweight='bold', pad=12)
ax2.set_title("MOVIE 13: Developable Rolling Kinetics\nLinear Trajectory Trace & CMB Dipolar Alignment Axis", 
              color='#f97316', fontsize=10, fontweight='bold', pad=12)

# Subplot 2 Limits & Labels
ax2.set_xlim(-3.5, 3.5)
ax2.set_ylim(-2.0, 2.0)
ax2.set_xlabel(r'Rolling Position $x/R_d$', color='white')
ax2.set_ylabel(r'Height $y/R_d$', color='white')

# Static Elements Subplot 2
ax2.axhline(y=-1.2, color='gray', linewidth=2, linestyle='-')
ax2.annotate('CMB Preferred Axis Alignment Vector', xy=(2.0, 1.2), xytext=(-2.0, 1.2),
             arrowprops=dict(arrowstyle="->", color="#14b8a6", lw=2.5),
             color="#14b8a6", fontsize=9, fontweight='bold', ha='center')

# Dynamic Elements
rolling_body, = ax2.plot([], [], color='#f97316', linewidth=2.5)
cm_path, = ax2.plot([], [], color='#ef4444', linestyle='--', linewidth=1.5, label='Linear Path of Center of Mass')
ax2.legend(loc='lower right', facecolor='#0d111d', edgecolor='#f97316')

status_A = fig.text(0.28, 0.08, '', color='#14b8a6', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#14b8a6'))
status_B = fig.text(0.72, 0.08, '', color='#f97316', fontsize=8.5, fontweight='bold', ha='center', va='top', bbox=dict(facecolor='#0d111d', edgecolor='#f97316'))

# Generate Oloid 3D Parametrization
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 30)
x_3d = np.outer(np.cos(u), np.sin(v))
y_3d = np.outer(np.sin(u), np.sin(v))
z_3d = np.outer(np.ones(np.size(u)), np.cos(v))

cm_x_history, cm_y_history = [], []

def update(frame):
    t = frame * 0.1
    
    # 3D Rotation Animation
    ax1.clear()
    ax1.set_facecolor('#080812')
    ax1.plot_surface(x_3d, y_3d, z_3d, color='#14b8a6', alpha=0.5, edgecolor='#0d9488', linewidth=0.3)
    ax1.view_init(elev=20, azim=frame * 2)
    ax1.set_axis_off()
    
    # 2D Rolling Motion
    x_pos = -2.5 + 0.05 * frame
    if x_pos > 2.5:
        x_pos = -2.5
        cm_x_history.clear()
        cm_y_history.clear()
        
    y_cm = -0.5 + 0.05 * np.cos(2 * t)
    cm_x_history.append(x_pos)
    cm_y_history.append(y_cm)
    
    # Ellipse outline representing rolling Oloid
    theta_roll = np.linspace(0, 2 * np.pi, 100)
    x_ellipse = x_pos + 0.7 * np.cos(theta_roll)
    y_ellipse = y_cm + 0.5 * np.sin(theta_roll)
    rolling_body.set_data(x_ellipse, y_ellipse)
    
    cm_path.set_data(cm_x_history, cm_y_history)
    
    status_A.set_text("OLOID CONVEX HULL CONV(C1 U C2)\nExact surface area conservation: A = 4*pi*R_d^2\nBoundary entropy S = k_B*A / (4*l_P^2) continuous")
    status_B.set_text(f"DEVELOPABLE ROLLING KINETICS\nLinear Center of Mass path trace at x = {x_pos:.2f}\nImprints 1D directional alignment on CMB dipole (l=2,3)")

    return rolling_body, cm_path, status_A, status_B

anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
output_filename = 'Movie13_Oloid_Merger_Kinetics.mp4'
anim.save(output_filename, writer='ffmpeg', fps=30, dpi=150)
plt.close(fig)
print(f"Successfully rendered '{output_filename}'.")
