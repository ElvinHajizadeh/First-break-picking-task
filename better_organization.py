import h5py
import numpy as np
import os
import matplotlib.pyplot as plt

path = 'seismic_data/Halfmile.hdf5'
with h5py.File(path, 'r') as f:
    group = f['TRACE_DATA/DEFAULT']
    shot_ids = group['SHOTID'][:].flatten()
    rec_x = group['REC_X'][:].flatten()
    rec_y = group['REC_Y'][:].flatten()
    data_array = group['data_array']
    spare1 = group['SPARE1'][:].flatten()
    
    # Let's look at one shot
    shot_id = 20021449
    mask = (shot_ids == shot_id)
    
    shot_rec_x = rec_x[mask]
    shot_rec_y = rec_y[mask]
    shot_data = data_array[mask, :]
    shot_labels = spare1[mask]
    
    # Plot receiver coordinates to see the lines
    plt.figure(figsize=(8, 8))
    plt.scatter(shot_rec_x, shot_rec_y, c='b', s=1)
    plt.title(f'Receiver Coordinates for Shot {shot_id}')
    plt.xlabel('REC_X')
    plt.ylabel('REC_Y')
    plt.savefig('receiver_coords.png')
    print("Saved receiver coordinates plot to receiver_coords.png")
    
    # Group by receiver lines (e.g., using REC_Y if they are horizontal lines)
    # Or just use a simple clustering/grouping
    # Let's see the unique REC_Y values
    unique_y = np.unique(shot_rec_y)
    print(f"Unique REC_Y values: {len(unique_y)}")
    
    # If there are many unique Y values, they might be slightly different
    # Let's group them if they are close
    from sklearn.cluster import DBSCAN
    coords = np.column_stack((shot_rec_x, shot_rec_y))
    # Normalize coords for clustering
    coords_norm = (coords - np.mean(coords, axis=0)) / np.std(coords, axis=0)
    # Use DBSCAN to find lines
    clustering = DBSCAN(eps=0.1, min_samples=10).fit(coords_norm)
    labels = clustering.labels_
    
    print(f"Found {len(np.unique(labels))} clusters (lines).")
    
    # Plot clusters
    plt.figure(figsize=(8, 8))
    plt.scatter(shot_rec_x, shot_rec_y, c=labels, cmap='tab20', s=5)
    plt.title(f'Receiver Lines (Clusters) for Shot {shot_id}')
    plt.savefig('receiver_lines.png')
    print("Saved receiver lines plot to receiver_lines.png")
