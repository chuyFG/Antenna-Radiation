import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 3e8  # speed of light
f = 2.4e9  # frequency of WiFi signal
lambda_ = c/f  # wavelength
Pt = 20  # transmit power (dBm)
Gt = 0  # transmit antenna gain (dBi)
Gr = 0  # receive antenna gain (dBi)
N = 8  # number of elements in the phased array

# Define antenna positions
x1 = -0.5
y1 = 0
z1 = 0
x2 = 0.5
y2 = 0
z2 = 0

# Create 2D grid of points
x_grid = np.linspace(-2, 2, 100)
y_grid = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x_grid, y_grid, indexing='ij')

# Compute distance between each point and antennas
distances1 = np.sqrt((X-x1)**2 + (Y-y1)**2 + z1**2)
distances2 = np.sqrt((X-x2)**2 + (Y-y2)**2 + z2**2)

# Compute phase shift of each antenna element
theta1 = np.arctan2(Y-y1, X-x1)
theta2 = np.arctan2(Y-y2, X-x2)
phi1 = 2*np.pi*distances1/lambda_
phi2 = 2*np.pi*distances2/lambda_
phase1 = np.exp(1j*(phi1 + theta1))
phase2 = np.exp(1j*(phi2 + theta2))

# Compute radiation pattern for each antenna
theta = np.linspace(0, 2*np.pi, 360)
pattern1 = np.abs(np.sum(np.exp(1j*2*np.pi*(np.arange(N)-N/2)*np.sin(theta))/N))**2
pattern2 = np.abs(np.sum(np.exp(1j*2*np.pi*(np.arange(N)-N/2)*np.sin(theta))/N))**2

# Compute total radiated power
P = (Pt + Gt + Gr + 10*np.log10(np.abs(phase1 + phase2)**2) + 10*np.log10(pattern1) + 10*np.log10(pattern2))

# Create heatmap of radiated power
fig, ax = plt.subplots()
heatmap = ax.pcolormesh(X, Y, P, cmap='jet')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_title('Radiated Power of Two Phased Array Antennas')
cbar = fig.colorbar(heatmap)
cbar.set_label('Power (dBm)')
plt.show()