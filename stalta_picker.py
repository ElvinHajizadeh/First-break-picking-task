import numpy as np
import matplotlib.pyplot as plt

def sta_lta(trace, sta_len, lta_len):
    sta = np.zeros(len(trace))
    lta = np.zeros(len(trace))
    
    # Square the trace to get energy
    energy = trace**2
    
    # Calculate STA and LTA
    for i in range(len(trace)):
        if i < lta_len:
            sta[i] = np.mean(energy[max(0, i-sta_len):i+1])
            lta[i] = np.mean(energy[0:i+1])
        else:
            sta[i] = np.mean(energy[i-sta_len:i+1])
            lta[i] = np.mean(energy[i-lta_len:i+1])
            
    ratio = sta / (lta + 1e-10)
    return ratio

def pick_first_break(trace, sta_len=10, lta_len=50, threshold=3.0):
    ratio = sta_lta(trace, sta_len, lta_len)
    picks = np.where(ratio > threshold)[0]
    if len(picks) > 0:
        return picks[0]
    else:
        return 0

# Test on one shot
shot_id = 20021449
data = np.load(f'gathers/shot_{shot_id}_data.npy')
labels = np.load(f'gathers/shot_{shot_id}_labels.npy')
sample_rate = 2.0

predicted_picks = []
for i in range(data.shape[0]):
    pick_idx = pick_first_break(data[i, :])
    predicted_picks.append(pick_idx * sample_rate)

predicted_picks = np.array(predicted_picks)

# Plot results
plt.figure(figsize=(12, 8))
plt.imshow(data.T, aspect='auto', cmap='gray', extent=[0, data.shape[0], data.shape[1]*sample_rate, 0])
plt.plot(np.arange(len(labels)), labels, 'r.', markersize=1, label='True Labels')
plt.plot(np.arange(len(predicted_picks)), predicted_picks, 'b.', markersize=1, label='STA/LTA Picks')
plt.title(f'STA/LTA First Break Picking - Shot {shot_id}')
plt.xlabel('Trace Index')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('stalta_results.png')
print("Saved results to stalta_results.png")
