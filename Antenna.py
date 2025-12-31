import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

# Define the frequency and length of the antennas
freq = 100e6  # Hz
length = 3  # meters

# Define the theta and phi angles for the radiation pattern
theta, phi = np.mgrid[0:np.pi:100j, 0:2*np.pi:100j]

# Define a function to calculate the electric field magnitude for a monopole antenna at a given angle
def monopole_electric_field(theta, phi, freq, length):
    c = 3e8  # speed of light
    wavelength = c / freq
    k = 2 * math.pi / wavelength
    eta = 377  # impedance of free space

    E_theta = (1j * eta * k * length / (4 * np.pi)) * np.sin(theta) * np.exp(-1j * k * length * np.cos(theta) / 2)
    E_phi = 0

    E_mag = np.sqrt(np.abs(E_theta)**2 + np.abs(E_phi)**2)

    return E_mag

# Define the physical locations of the antennas
antennas = [(0, 0, 0), (1, 1, 0), (-1, -1, 0)]

# Calculate the electric field magnitude for each antenna at each angle
E_total = np.zeros((len(theta), len(phi)), dtype=complex)

c = 3e8  # speed of light
wavelength = c / freq
k = 2 * math.pi / wavelength

for antenna in antennas:
    x, y, z = antenna
    E_antenna = monopole_electric_field(theta, phi, freq, length)
    phase_shift = np.exp(1j * k * (x * np.sin(theta) * np.cos(phi) + y * np.sin(theta) * np.sin(phi) + z * np.cos(theta)))
    E_total += E_antenna * phase_shift

# Plot the radiation patterns for each antenna in a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Radiation Pattern')
for i, antenna in enumerate(antennas):
    x, y, z = antenna
    E_antenna = np.abs(monopole_electric_field(0, 0, freq, length))
    ax.scatter(x, y, z, s=100, label='Antenna {}'.format(i+1))
    ax.plot_surface(x + E_antenna * np.sin(theta) * np.cos(phi),
                     y + E_antenna * np.sin(theta) * np.sin(phi),
                     z + E_antenna * np.cos(theta),
                     alpha=0.5)
plt.legend()
plt.show()
