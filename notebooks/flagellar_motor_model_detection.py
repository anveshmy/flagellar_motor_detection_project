# %% [markdown]
# # Flagellar Motor Detection Model

# %%
import polars as pl
import numpy as np
import os
import kagglehub
os.chdir("..")
print( "Current working directory: ", os.getcwd() )


# %%
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

# %% [markdown]
# ## Data Preparation

# %%
DATA_DIR = "data/external/3"
data_df = pl.read_csv((DATA_DIR + "/labels.csv"))
data_df

# %%
print(f"Unique Tomograms: {data_df['tomo_id'].n_unique()}")
print(f"Unique Datasets:  {data_df['dataset_id'].n_unique()}")

# %% [markdown]
# ### Visualization of the Dataset

# %%
ex_idx = 69
row = data_df[ex_idx].to_dict()
row

# %%


# %%
fpath= os.path.join(DATA_DIR, "volumes", row["tomo_id"][0]+".npy")
arr= np.load(fpath)
print(arr.shape)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title(row["tomo_id"][0])
ax.imshow(arr[int(row["z"][0]), ...], cmap="gray")
ax.scatter(row["x"][0], row["y"][0], c="red", s=50)

ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

plt.tight_layout()
plt.show()

# %%
SEED= 0
tmp = data_df.groupby("dataset_id").agg(pl.all().sample(n=1, seed=SEED))
tmp = tmp.sample(frac=1, seed=SEED)

# Create figure
fig, axes = plt.subplots(2, 8, figsize=(24, 6))
axes= axes.flatten()

for idx in range(len(axes)):
    row= tmp.iloc[idx].to_dict()

    # Load tomo
    fpath= os.path.join(DATA_DIR, "volumes", row["tomo_id"]+".npy")
    arr= np.load(fpath)

    # Visualize
    # axes[idx].set_title(row["dataset_id"])
    axes[idx].imshow(arr[int(row["z"][0]), ...], cmap="gray")
    axes[idx].scatter(row["x"][0], row["y"][0], c="red", s=50)
    axes[idx].set_xticks([])
    axes[idx].set_yticks([])
    axes[idx].set_frame_on(False)

plt.tight_layout()
plt.show()
plt.show()
