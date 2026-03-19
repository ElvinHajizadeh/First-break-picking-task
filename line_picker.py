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

def pick_line(line_data, sample_rate):
    fs = 1000 / sample_rate
    num_traces, num_samples = line_data.shape
    picks = np.zeros(num_traces)
    
    for i in range(num_traces):
        trace = line_data[i, :]
        filtered_trace = bandpass_filter(trace, 5, 80, fs)
        picks[i] = aic_picker(filtered_trace)
        
    # Smoothing
    picks = medfilt(picks, kernel_size=11)
    return picks * sample_rate

# Test on one line
shot_id = 20021449
line_id = 2
data = np.load(f'lines/shot_{shot_id}_line_{line_id}_data.npy')
labels = np.load(f'lines/shot_{shot_id}_line_{line_id}_labels.npy')
sample_rate = 2.0

predicted_picks = pick_line(data, sample_rate)

# Plot results
plt.figure(figsize=(10, 6))
plt.imshow(data.T, aspect='auto', cmap='gray', extent=[0, data.shape[0], data.shape[1]*sample_rate, 0])
plt.plot(np.arange(len(labels)), labels, 'r.', markersize=2, label='True Labels')
plt.plot(np.arange(len(predicted_picks)), predicted_picks, 'y-', linewidth=2, label='AIC Picks')
plt.title(f'First Break Picking - Shot {shot_id} Line {line_id}')
plt.xlabel('Trace Index')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('line_results.png')
print("Saved results to line_results.png")

# Calculate error
mask = (labels > 0)
error = np.abs(predicted_picks[mask] - labels[mask])
print(f"Mean Absolute Error: {np.mean(error):.2f} ms")
print(f"Median Absolute Error: {np.median(error):.2f} ms")
