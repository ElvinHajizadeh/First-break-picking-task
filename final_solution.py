import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, medfilt

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def aic_picker(trace):
    n = len(trace)
    if n < 10: return 0
    aic = np.zeros(n)
    for k in range(1, n-1):
        var_before = np.var(trace[:k])
        var_after = np.var(trace[k:])
        if var_before <= 0: var_before = 1e-10
        if var_after <= 0: var_after = 1e-10
        aic[k] = k * np.log10(var_before) + (n - k - 1) * np.log10(var_after)
    return np.argmin(aic[1:-1]) + 1

def pick_line_robust(line_data, sample_rate):
    fs = 1000 / sample_rate
    num_traces, num_samples = line_data.shape
    picks = np.zeros(num_traces)
    
    # 1. Filter
    filtered_data = np.zeros_like(line_data)
    for i in range(num_traces):
        filtered_data[i, :] = bandpass_filter(line_data[i, :], 5, 80, fs)
    
    # 2. AIC Picks
    for i in range(num_traces):
        picks[i] = aic_picker(filtered_data[i, :])
    
    # 3. Spatial Continuity: Use a moving window to reject outliers
    # If a pick is too far from the median of its neighbors, it's likely wrong
    smoothed = medfilt(picks, kernel_size=31)
    for i in range(num_traces):
        if np.abs(picks[i] - smoothed[i]) > 30: # 60ms threshold
            picks[i] = smoothed[i]
            
    # 4. Final smoothing
    final_picks = medfilt(picks, kernel_size=11)
    return final_picks * sample_rate

# Run on multiple lines and calculate overall performance
import os
line_files = [f for f in os.listdir('lines') if f.endswith('_data.npy')]
all_errors = []

for f_name in line_files[:10]: # Test on 10 lines
    data = np.load(os.path.join('lines', f_name))
    labels = np.load(os.path.join('lines', f_name.replace('_data.npy', '_labels.npy')))
    sample_rate = 2.0
    
    picks = pick_line_robust(data, sample_rate)
    mask = (labels > 0)
    if np.any(mask):
        error = np.abs(picks[mask] - labels[mask])
        all_errors.extend(error)

print(f"Overall Median Absolute Error: {np.median(all_errors):.2f} ms")
print(f"Overall Mean Absolute Error: {np.mean(all_errors):.2f} ms")

# Save one final plot
data = np.load('lines/shot_20021449_line_2_data.npy')
labels = np.load('lines/shot_20021449_line_2_labels.npy')
picks = pick_line_robust(data, 2.0)
plt.figure(figsize=(10, 6))
plt.imshow(data.T, aspect='auto', cmap='gray', extent=[0, data.shape[0], data.shape[1]*2.0, 0])
plt.plot(np.arange(len(labels)), labels, 'r.', markersize=2, label='True Labels')
plt.plot(np.arange(len(picks)), picks, 'y-', linewidth=2, label='Robust Picks')
plt.title('Final Robust First Break Picking')
plt.xlabel('Trace Index')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('final_robust_results.png')
