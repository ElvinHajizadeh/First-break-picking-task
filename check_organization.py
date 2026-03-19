import h5py
import numpy as np

path = 'seismic_data/Halfmile.hdf5'
with h5py.File(path, 'r') as f:
    group = f['TRACE_DATA/DEFAULT']
    shot_ids = group['SHOTID'][:]
    rec_x = group['REC_X'][:]
    rec_y = group['REC_Y'][:]
    
    print(f"Total traces: {len(shot_ids)}")
    unique_shots = np.unique(shot_ids)
    print(f"Unique shots: {len(unique_shots)}")
    
    # Check first 1000 traces
    print("\nFirst 10 traces:")
    for i in range(10):
        print(f"Trace {i}: SHOTID={shot_ids[i][0]}, REC_X={rec_x[i][0]}, REC_Y={rec_y[i][0]}")
        
    # Check if traces are sorted by SHOTID
    is_sorted = np.all(np.diff(shot_ids.flatten()) >= 0)
    print(f"\nAre traces sorted by SHOTID? {is_sorted}")
