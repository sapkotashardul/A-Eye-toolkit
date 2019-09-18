import h5py
import tensorflow as tf
import numpy as np
import os

def classify_generator(batch_size, filepath):
	batch_size = batch_size
	channels = 1
	edge_negligence = 15
	count = 0
	while count < 1000:
		count = count + 1
		for datapath in os.listdir(filepath):
			with h5py.File(filepath + '/' + datapath, 'r') as h5f:
				X_dset = h5f['X']
				image_3d = np.zeros((batch_size, 128, 192, 64, channels))
				label_3d = np.zeros((batch_size, 2))
				for i in range(int(((X_dset.shape[0] - (X_dset.shape[0] % batch_size))/batch_size))):
					for j in range(batch_size):
						image_3d[j,:,:,:,0] = X_dset[i * batch_size + j]
					yield (image_3d)
