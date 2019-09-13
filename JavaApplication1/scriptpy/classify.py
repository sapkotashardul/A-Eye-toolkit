import argparse
import os
import csv
import h5py

import sys
import tensorflow as tf
import numpy as np
from keras.layers import (Activation, Conv3D, Dense, Dropout, Flatten,
                          MaxPooling3D)
from keras.layers.advanced_activations import LeakyReLU
from keras.losses import binary_crossentropy
from keras.models import Sequential
from keras.utils import np_utils

LAYER_ACTIVATION = 'relu'

def main():
    global batch_size
    parser = argparse.ArgumentParser(
        description='simple 3D convolution for action recognition')
    parser.add_argument('--batch', type=int, default=1)
    parser.add_argument('--filepath', required=True, help='directions to folder containing H5 files to be classified')
    parser.add_argument('--folderpath', required=True, help='directions to EyeKnowYou folder')
    parser.add_argument('--resultspath', required=True, help='directions to store result files')
    args = parser.parse_args()

    # Define model
    model = Sequential()
    model.add(Conv3D(32, kernel_size=(3, 3, 15), input_shape=(128, 192, 64, 1), border_mode='same', name='new_input'))
    model.add(Activation('relu'))
    model.add(Conv3D(32, kernel_size=(3, 3, 3), border_mode='same')) #, trainable = False
    model.add(Activation('softmax'))
    model.add(MaxPooling3D(pool_size=(3, 3, 3), border_mode='same'))
    # model.add(Dropout(0.25))

    model.add(Conv3D(64, kernel_size=(3, 3, 3), border_mode='same'))
    model.add(Activation('relu'))
    model.add(Conv3D(64, kernel_size=(3, 3, 3), border_mode='same'))
    model.add(Activation('softmax'))
    model.add(MaxPooling3D(pool_size=(3, 3, 3), border_mode='same'))
    # model.add(Dropout(0.25))

    model.add(Conv3D(64, kernel_size=(3, 3, 3), border_mode='same'))
    model.add(Activation('relu'))
    model.add(Conv3D(64, kernel_size=(3, 3, 3), border_mode='same'))
    model.add(Activation('softmax'))
    model.add(MaxPooling3D(pool_size=(3, 3, 3), border_mode='same'))
    # model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation='sigmoid', name='new_dense_1'))
    # model.add(Dropout(0.25))
    model.add(Dense(2, activation='softmax', name='new_output'))

    batch_size = args.batch
    filepath = args.filepath
    folderpath = args.folderpath
    resultspath = args.resultspath
    checkpoint_direct = folderpath + "/checkpoint/"
    model.load_weights(checkpoint_direct + "eky_weights.hd5")#, by_name=True

    channels = 1 
    print("Running EyeKnowYou Model....")
    sys.stdout.flush()
    for filename in os.listdir(filepath):
        with open(resultspath + '/' + filename.split(".h")[0] + '_results.csv', mode='w') as csv_file:
            print("\nAnalysing file : " + filename)
            sys.stdout.flush()
            result_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow(['Start Frame', 'End Frame', 'Probability of looking at a screen', 'Probability of having high cognitive load','Screen(decision)', 'Cognitive Load(decision)'])
            with h5py.File(filepath + '/' + filename, 'r') as h5f:
                X_dset = h5f['X']
                image_3d = np.zeros((batch_size, 128, 192, 64, channels))
                for i in range(int(X_dset.shape[0])):
                    image_3d[0,:,:,:,0] = X_dset[i]
                    predictions = model.predict(image_3d)
                    print("classifying frames : %6d   to   %6d" %(i * 64,i * 64 + 63))
                    sys.stdout.flush()
                    result_writer.writerow([str(i * 64), str(i * 64 + 63), str(predictions[0][0]), str(predictions[0][1]), str(np.round(predictions[0][0])), str(np.round(predictions[0][1]))])

if __name__ == '__main__':
    main()