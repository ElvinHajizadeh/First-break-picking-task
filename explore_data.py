import h5py
import numpy as np

path = 'seismic_data/Halfmile.hdf5'
with h5py.File(path, 'r') as f:
    print("Keys in the file:")
    print(list(f.keys()))
    
    group = f['TRACE_DATA/DEFAULT']
    print("\nKeys in TRACE_DATA/DEFAULT:")
    print(list(group.keys()))
    
    # Check some keys
    for key in ['data_array', 'SHOTID', 'SAMP_RATE', 'SPARE1', 'SAMP_NUM']:
        if key in group:
            data = group[key]
            print(f"\n{key}:")
            print(f"  Shape: {data.shape}")
            print(f"  Dtype: {data.dtype}")
            if len(data.shape) == 1:
                print(f"  Sample values: {data[:5]}")
            else:
                print(f"  Sample values (first trace, first 5 samples): {data[0, :5]}")
