import h5py
import numpy as np
import os
from sklearn.cluster import DBSCAN

path = 'seismic_data/Halfmile.hdf5'
output_dir = 'lines'
os.makedirs(output_dir, exist_ok=True)

with h5py.File(path, 'r') as f:
    group = f['TRACE_DATA/DEFAULT']
    shot_ids = group['SHOTID'][:].flatten()
    rec_x = group['REC_X'][:].flatten()
    rec_y = group['REC_Y'][:].flatten()
    data_array = group['data_array']
    spare1 = group['SPARE1'][:].flatten()
    
    # Process first 3 shots
    unique_shots = np.unique(shot_ids)[:3]
    
    for shot_id in unique_shots:
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
            
            np.save(os.path.join(output_dir, f'shot_{shot_id}_line_{line_id}_data.npy'), line_data)
            np.save(os.path.join(output_dir, f'shot_{shot_id}_line_{line_id}_labels.npy'), line_labels_data)
            print(f"Saved shot {shot_id} line {line_id} with {line_data.shape[0]} traces.")
