import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

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
    aic = np.zeros(n)
    for k in range(1, n-1):
        var_before = np.var(trace[:k])
        var_after = np.var(trace[k:])
        if var_before == 0: var_before = 1e-10
        if var_after == 0: var_after = 1e-10
        aic[k] = k * np.log10(var_before) + (n - k - 1) * np.log10(var_after)
    return np.argmin(aic[1:-1]) + 1

# Test on one shot
shot_id = 20021449
data = np.load(f'gathers/shot_{shot_id}_data.npy')
labels = np.load(f'gathers/shot_{shot_id}_labels.npy')
sample_rate = 2.0 # ms
fs = 1000 / sample_rate # Hz

predicted_picks = []
for i in range(data.shape[0]):
    trace = data[i, :]
    # Filter the trace
    filtered_trace = bandpass_filter(trace, 5, 80, fs)
    
    # Use a window around the expected first break to speed up and improve accuracy
    # For now, let's just use the whole trace
    pick_idx = aic_picker(filtered_trace)
    predicted_picks.append(pick_idx * sample_rate)

predicted_picks = np.array(predicted_picks)

# Plot results
plt.figure(figsize=(12, 8))
plt.imshow(data.T, aspect='auto', cmap='gray', extent=[0, data.shape[0], data.shape[1]*sample_rate, 0])
plt.plot(np.arange(len(labels)), labels, 'r.', markersize=1, label='True Labels')
plt.plot(np.arange(len(predicted_picks)), predicted_picks, 'g.', markersize=1, label='AIC Picks')
plt.title(f'AIC First Break Picking - Shot {shot_id}')
plt.xlabel('Trace Index')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('aic_results.png')
print("Saved results to aic_results.png")
