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
    # Calculate variance in a sliding window to avoid log(0)
    aic = np.zeros(n)
    for k in range(1, n-1):
        var_before = np.var(trace[:k])
        var_after = np.var(trace[k:])
        if var_before <= 0: var_before = 1e-10
        if var_after <= 0: var_after = 1e-10
        aic[k] = k * np.log10(var_before) + (n - k - 1) * np.log10(var_after)
    return np.argmin(aic[1:-1]) + 1

def final_pick(shot_data, sample_rate):
    fs = 1000 / sample_rate
    num_traces, num_samples = shot_data.shape
    picks = np.zeros(num_traces)
    
    # 1. Filter data
    filtered_data = np.zeros_like(shot_data)
    for i in range(num_traces):
        filtered_data[i, :] = bandpass_filter(shot_data[i, :], 5, 80, fs)
    
    # 2. Initial AIC picks
    for i in range(num_traces):
        picks[i] = aic_picker(filtered_data[i, :])
    
    # 3. Remove extreme outliers (picks that are too far from their neighbors)
    # Using a large median filter first
    smoothed_picks = medfilt(picks, kernel_size=51)
    
    # 4. Refine: if a pick is too far from the smoothed version, replace it
    for i in range(num_traces):
        if np.abs(picks[i] - smoothed_picks[i]) > 50: # 50 samples = 100ms
            picks[i] = smoothed_picks[i]
            
    # 5. Final smoothing
    final_picks = medfilt(picks, kernel_size=11)
    
    return final_picks * sample_rate

# Test on one shot
shot_id = 20021449
data = np.load(f'gathers/shot_{shot_id}_data.npy')
labels = np.load(f'gathers/shot_{shot_id}_labels.npy')
sample_rate = 2.0

predicted_picks = final_pick(data, sample_rate)

# Plot results
plt.figure(figsize=(12, 8))
plt.imshow(data.T, aspect='auto', cmap='gray', extent=[0, data.shape[0], data.shape[1]*sample_rate, 0])
plt.plot(np.arange(len(labels)), labels, 'r.', markersize=1, label='True Labels')
plt.plot(np.arange(len(predicted_picks)), predicted_picks, 'm-', linewidth=1, label='Final Picks')
plt.title(f'Final First Break Picking - Shot {shot_id}')
plt.xlabel('Trace Index')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('final_results.png')
print("Saved results to final_results.png")

# Calculate error
mask = (labels > 0)
error = np.abs(predicted_picks[mask] - labels[mask])
print(f"Mean Absolute Error: {np.mean(error):.2f} ms")
print(f"Median Absolute Error: {np.median(error):.2f} ms")
