# data_augmentation.py
import numpy as np
import pandas as pd

def augment_data(df, target_size=10000):
    current_size = len(df)
    new_data = []

    while len(new_data) + current_size < target_size:
        row = df.sample(1).iloc[0]
        # Add noise and jitter to simulate real variations
        new_row = row.copy()
        new_row['resonance_wavelength'] += np.random.normal(0, 5)
        new_row['refractive_index'] += np.random.normal(0, 0.01)
        new_row['thickness'] += np.random.normal(0, 2)
        new_row['intensity_profile'] = [i + np.random.normal(0, 0.01) for i in new_row['intensity_profile']]
        new_data.append(new_row)

    augmented_df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
    return augmented_df