import numpy as np
import matplotlib.pyplot as plt
import os

shot_id = 20021449
data = np.load(f'gathers/shot_{shot_id}_data.npy')
labels = np.load(f'gathers/shot_{shot_id}_labels.npy')

# Sample rate is 2ms (2000 microseconds)
sample_rate = 2.0

plt.figure(figsize=(12, 8))
# Plot the seismic data as an image
# Transpose to have time on Y-axis and traces on X-axis
plt.imshow(data.T, aspect='auto', cmap='gray', extent=[0, data.shape[0], data.shape[1]*sample_rate, 0])
plt.colorbar(label='Amplitude')

# Plot the labels (first break times)
# Labels are in msec
plt.plot(np.arange(len(labels)), labels, 'r.', markersize=1, label='First Break Labels')

plt.title(f'Shot Gather {shot_id}')
plt.xlabel('Trace Index')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('shot_gather_visualization.png')
print("Saved visualization to shot_gather_visualization.png")
