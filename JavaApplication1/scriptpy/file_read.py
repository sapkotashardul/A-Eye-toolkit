import cv2
import numpy as np
import h5py
import os
import argparse
import sys

def read(filepath):
	with h5py.File(filepath, mode='r') as h5f:
		xdset = h5f['X']
		ydset = h5f['Y']
		udset = h5f['U']
		# print(udset.shape)
		for i in range(xdset.shape[0]):
			print(int(np.floor(i/64)), end = '    ')
			print(i%64)
			sys.stdout.flush()
			cv2.imshow("eye", xdset[int(np.floor(i/64)),:,:,i%64])
			j = cv2.waitKey(2)
			if(j == 27):
				break

def file_handler_folder(data_files_directory):
	for filename in os.listdir(data_files_directory):
		filepath = data_files_directory + '/' +filename
		read(filepath)

def file_handler_single(data_file):
		read(data_file)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--filepath', required=True, help='File path or folder path') #required
	args = parser.parse_args()
	filepath = args.filepath
	print("Press 'Esc' to exit")
	if('.h5' in filepath):
		file_handler_single(filepath)
	else:
		file_handler_folder(filepath)

main()