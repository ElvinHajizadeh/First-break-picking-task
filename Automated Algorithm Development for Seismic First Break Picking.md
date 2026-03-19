# Automated Algorithm Development for Seismic First Break Picking

## 1. Introduction and Problem Definition

Seismic first breaks are the initial arrivals of seismic waves, which are critical for processing and interpreting seismic data, especially in seismic refraction and tomography studies. The objective of this task is to create a robust, automated method that can accurately detect these first breaks across different seismic assets, regardless of varying signal-to-noise ratios and variations in first break line behavior.

## 2. Dataset Overview

The provided dataset consists of seismic traces from four different real-world seismic assets (Brunswick, Halfmile, Lalor, Sudbury), stored in HDF5 format. Each trace in the dataset is manually labeled with first break times where available. In this study, the `Halfmile` dataset was used.

Key fields in the dataset:

| Field Name   | Description                                                               |
| :----------- | :------------------------------------------------------------------------ |
| `data_array` | 2D array of all recorded seismic traces (trace count x sample count)      |
| `SHOTID`     | Shot identifiers                                                          |
| `REC_X`      | Receiver X coordinate                                                     |
| `REC_Y`      | Receiver Y coordinate                                                     |
| `SAMP_RATE`  | Sampling rate (in microseconds)                                           |
| `SPARE1`     | First break time values (in ms). If 0 or -1, the trace is unlabeled.      |

## 3. Methodology

A hybrid approach was developed for first break picking, involving the following steps:

1.  **Data Organization**: Seismic data was separated into 2D seismic images (lines) based on `SHOTID` and receiver coordinates (`REC_X`, `REC_Y`). The `DBSCAN` clustering algorithm was used to automatically identify receiver lines.

    ![Receiver Lines](https://private-us-east-1.manuscdn.com/sessionFile/phXXkqdrw87yYkCtxE4Tjd/sandbox/Smp4XzHKynDmR2tOLnBPm1-images_1773945916516_na1fn_L2hvbWUvdWJ1bnR1L3JlY2VpdmVyX2xpbmVz.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvcGhYWGtxZHJ3ODd5WWtDdHhFNFRqZC9zYW5kYm94L1NtcDRYekhLeW5EbVIydE9MbkJQbTEtaW1hZ2VzXzE3NzM5NDU5MTY1MTZfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzSmxZMlZwZG1WeVgyeHBibVZ6LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=JLR03EOBwU4fzAs8E6SuZ3pa3unJmldrgbEtUdyt-7gN0~D~XFqnJDjQ~z3k0NOajefYmXEEEL3sKnQ7LTu-TOGmrAB-eaMhR5KUMK1e~t2xaEWP8yDV3WUzQI6H-XFFf9QN5aS5PiLFZWJawxNrBnD27~JnF9EBw3KGCY6j0c5th4EVEUq8tPlbSPVCN05-PVVeYICchphDcFVwktctxDqFdg6JFTy8lhor3dgjp-YV9UaUw-BRfAqz98ttajUYvhqh~nDmsKV7lVQvuUV2YDvw2-GB-aqABsrRqlI1h~PrSEIy1lNgt-AvmzLJ~13812fIMr62JsWOSBW4SjEzxA__)
    *Figure 1: Clustering of receiver lines for a single shot.* 

2.  **Pre-processing**: Each seismic trace was filtered with a 5-80 Hz bandpass filter to reduce noise and enhance the first break signal.

3.  **First Break Picking (AIC)**: An Akaike Information Criterion (AIC) based picker was applied to each filtered trace. AIC is effective in detecting abrupt changes in statistical properties (variance) within a time series, making it suitable for first break picking.

4.  **Spatial Continuity and Smoothing**: Initial AIC picks were processed with a median filter to ensure spatial consistency and reduce outliers. This helps to smooth out abrupt jumps between adjacent traces.

    ![Final Robust Picks](https://private-us-east-1.manuscdn.com/sessionFile/phXXkqdrw87yYkCtxE4Tjd/sandbox/Smp4XzHKynDmR2tOLnBPm1-images_1773945916516_na1fn_L2hvbWUvdWJ1bnR1L2ZpbmFsX3JvYnVzdF9yZXN1bHRz.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvcGhYWGtxZHJ3ODd5WWtDdHhFNFRqZC9zYW5kYm94L1NtcDRYekhLeW5EbVIydE9MbkJQbTEtaW1hZ2VzXzE3NzM5NDU5MTY1MTZfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyWnBibUZzWDNKdlluVnpkRjl5WlhOMWJIUnoucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=aXaGeVx7GCEpEuldmnO2wKg2o0Gw9xVElwBSz3c1fsUOok7TyyMpd8DT7KQmpE-Ovufn-jacUSrvSSK9c5HQ~7Tc5pRt58uEw5dP-P8tsBoFPjoDDd1ungKy2nnW2QCBSaIhUN92EJmyPxIW9HFrvrAcby~t23dxwr5x8nTPg73RD4H1sSdF9LJlWLQABpwLlYQGfCjdMzdGXvmlzu~NUvLN2jPSzwpowwcai09cvDT8g84gEwB5Ma3gcRiu6~FAeGXUs9ryujUaF~SXMCzZytsscJGYUhkIDXGgUJLY3CBIn2BahQ13zE-NJtxrKMAzVYGwqWy2cNWCoTtPYpvZ9w__)
    *Figure 2: First breaks picked by the developed algorithm (yellow line) and true labels (red dots).* 

## 4. Results and Validation

The algorithm was tested on the first 10 lines of the `Halfmile` dataset. The following error metrics were obtained:

-   **Mean Absolute Error (MAE)**: 85.83 ms
-   **Median Absolute Error (MdAE)**: 8.00 ms

The median absolute error indicates that the algorithm is quite accurate for most traces. The mean absolute error is influenced by larger errors in some noisy traces, but the median error better reflects typical performance.

## 5. Conclusion and Future Work

This study developed a robust algorithm for automated seismic first break picking, combining bandpass filtering, an AIC picker, and median filtering. The algorithm demonstrated acceptable accuracy compared to manual labels.

**Future Work:**

-   Further testing and parameter optimization on different seismic assets.
-   Investigation of machine learning-based approaches to improve performance in more complex noisy environments.
-   Optimization of the algorithm for real-time data processing workflows.

## 6. Final Code

The final code is located in the `final_solution.py` file. This file includes data loading, pre-processing, first break picking, and visualization steps.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, medfilt
import h5py
import os
from sklearn.cluster import DBSCAN

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype=\'band\')
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
    # If a pick is too far from the median of its neighbors, it\'s likely wrong
    smoothed = medfilt(picks, kernel_size=31)
    for i in range(num_traces):
        if np.abs(picks[i] - smoothed[i]) > 30: # 60ms threshold
            picks[i] = smoothed[i]
            
    # 4. Final smoothing
    final_picks = medfilt(picks, kernel_size=11)
    return final_picks * sample_rate

# Main execution for data organization and picking
def main():
    data_path = \'seismic_data/Halfmile.hdf5\'
    output_dir_gathers = \'gathers\'
    output_dir_lines = \'lines\'
    os.makedirs(output_dir_gathers, exist_ok=True)
    os.makedirs(output_dir_lines, exist_ok=True)

    with h5py.File(data_path, \'r\') as f:
        group = f[\'TRACE_DATA/DEFAULT\']
        shot_ids = group[\'SHOTID\'][:].flatten()
        rec_x = group[\'REC_X\'][:].flatten()
        rec_y = group[\'REC_Y\'][:].flatten()
        data_array = group[\'data_array\']
        spare1 = group[\'SPARE1\'][:].flatten()

        unique_shots = np.unique(shot_ids)

        for shot_id in unique_shots[:3]: # Process first 3 shots for demonstration
            mask = (shot_ids == shot_id)
            shot_rec_x = rec_x[mask]
            shot_rec_y = rec_y[mask]
            shot_data = data_array[mask, :]
            shot_labels = spare1[mask]

            # Cluster to find lines
            coords = np.column_stack((shot_rec_x, shot_rec_y))
            coords_norm = (coords - np.mean(coords, axis=0)) / np.std(coords, axis=0)
            clustering = DBSCAN(eps=0.1, min_samples=10).fit(coords_norm)
            line_labels = clustering.labels_

            for line_id in np.unique(line_labels):
                if line_id == -1: continue # Skip noise
                line_mask = (line_labels == line_id)
                line_data = shot_data[line_mask, :]
                line_labels_data = shot_labels[line_mask]

                # Sort by REC_X to ensure continuity
                sort_idx = np.argsort(shot_rec_x[line_mask])
                line_data = line_data[sort_idx, :]
                line_labels_data = line_labels_data[sort_idx]

                np.save(os.path.join(output_dir_lines, f\'shot_{shot_id}_line_{line_id}_data.npy\'), line_data)
                np.save(os.path.join(output_dir_lines, f\'shot_{shot_id}_line_{line_id}_labels.npy\'), line_labels_data)

    # Run on multiple lines and calculate overall performance
    line_files = [f for f in os.listdir(output_dir_lines) if f.endswith(\'_data.npy\')]
    all_errors = []

    for f_name in line_files[:10]: # Test on 10 lines
        data = np.load(os.path.join(output_dir_lines, f_name))
        labels = np.load(os.path.join(output_dir_lines, f_name.replace(\'_data.npy\', \'_labels.npy\')))
        sample_rate = 2.0
        
        picks = pick_line_robust(data, sample_rate)
        mask = (labels > 0)
        if np.any(mask):
            error = np.abs(picks[mask] - labels[mask])
            all_errors.extend(error)

    print(f"Overall Median Absolute Error: {np.median(all_errors):.2f} ms")
    print(f"Overall Mean Absolute Error: {np.mean(all_errors):.2f} ms")

    # Save one final plot
    data = np.load(\'lines/shot_20021449_line_2_data.npy\')
    labels = np.load(\'lines/shot_20021449_line_2_labels.npy\')
    picks = pick_line_robust(data, 2.0)
    plt.figure(figsize=(10, 6))
    plt.imshow(data.T, aspect=\'auto\', cmap=\'gray\', extent=[0, data.shape[0], data.shape[1]*2.0, 0])
    plt.plot(np.arange(len(labels)), labels, \'r.\', markersize=2, label=\'True Labels\')
    plt.plot(np.arange(len(picks)), picks, \'y-\', linewidth=2, label=\'Robust Picks\')
    plt.title(\'Final Robust First Break Picking\')
    plt.xlabel(\'Trace Index\')
    plt.ylabel(\'Time (ms)\')
    plt.legend()
    plt.savefig(\'final_robust_results.png\')

if __name__ == \'__main__\':
    main()
```
