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
        if var_before == 0: var_before = 1e-10
        if var_after == 0: var_after = 1e-10
        aic[k] = k * np.log10(var_before) + (n - k - 1) * np.log10(var_after)
    return np.argmin(aic[1:-1]) + 1

def energy_threshold_picker(trace, threshold=2.0):
    energy = trace**2
    mean_energy = np.mean(energy)
    picks = np.where(energy > threshold * mean_energy)[0]
    if len(picks) > 0:
        return picks[0]
    return 0

def hybrid_pick(shot_data, sample_rate):
    fs = 1000 / sample_rate
    num_traces, num_samples = shot_data.shape
    picks = np.zeros(num_traces)
    
    for i in range(num_traces):
        trace = shot_data[i, :]
        filtered_trace = bandpass_filter(trace, 5, 80, fs)
        
        # Use energy threshold to find a rough window
        rough_pick = energy_threshold_picker(filtered_trace)
        
        if rough_pick > 0:
            # Refine with AIC in a window around the rough pick
            window_start = max(0, rough_pick - 50)
            window_end = min(num_samples, rough_pick + 50)
            window = filtered_trace[window_start:window_end]
            refined_pick = aic_picker(window)
            picks[i] = window_start + refined_pick
        else:
            picks[i] = 0
            
    # Apply median filter to smooth the line
    picks = medfilt(picks, kernel_size=15)
    
    return picks * sample_rate

# Test on one shot
shot_id = 20021449
data = np.load(f'gathers/shot_{shot_id}_data.npy')
labels = np.load(f'gathers/shot_{shot_id}_labels.npy')
sample_rate = 2.0

predicted_picks = hybrid_pick(data, sample_rate)

# Plot results
plt.figure(figsize=(12, 8))
plt.imshow(data.T, aspect='auto', cmap='gray', extent=[0, data.shape[0], data.shape[1]*sample_rate, 0])
plt.plot(np.arange(len(labels)), labels, 'r.', markersize=1, label='True Labels')
plt.plot(np.arange(len(predicted_picks)), predicted_picks, 'y-', linewidth=1, label='Hybrid Picks')
plt.title(f'Hybrid First Break Picking - Shot {shot_id}')
plt.xlabel('Trace Index')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('hybrid_results.png')
print("Saved results to hybrid_results.png")

# Calculate error
mask = (labels > 0) & (predicted_picks > 0)
error = np.abs(predicted_picks[mask] - labels[mask])
print(f"Mean Absolute Error: {np.mean(error):.2f} ms")
print(f"Median Absolute Error: {np.median(error):.2f} ms")
