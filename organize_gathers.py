import h5py
import numpy as np
import os

path = 'seismic_data/Halfmile.hdf5'
output_dir = 'gathers'
os.makedirs(output_dir, exist_ok=True)

with h5py.File(path, 'r') as f:
    group = f['TRACE_DATA/DEFAULT']
    shot_ids = group['SHOTID'][:].flatten()
    data_array = group['data_array']
    spare1 = group['SPARE1'][:].flatten()
    
    unique_shots, indices = np.unique(shot_ids, return_index=True)
    
    # Process first 5 shots for development
    for i in range(5):
        shot_id = unique_shots[i]
        start_idx = indices[i]
        if i < len(unique_shots) - 1:
            end_idx = indices[i+1]
        else:
            end_idx = len(shot_ids)
            
        shot_data = data_array[start_idx:end_idx, :]
        shot_labels = spare1[start_idx:end_idx]
        
        # Save to a numpy file for easy access
        np.save(os.path.join(output_dir, f'shot_{shot_id}_data.npy'), shot_data)
        np.save(os.path.join(output_dir, f'shot_{shot_id}_labels.npy'), shot_labels)
        print(f"Saved shot {shot_id} with {shot_data.shape[0]} traces.")
