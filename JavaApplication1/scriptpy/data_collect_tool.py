#Left anonymous for review

#dependencies
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import h5py
import eye_focus as eye_focus
import detect_iris as detect_iris
import argparse
from pathlib import Path
import datetime
import platform

#original frame size
FRAME_HEIGHT = 480
FRAME_WIDTH = 640

#cropped frame dimensions
IMAGE_WIDTH = 384
IMAGE_HEIGHT = 256
IMAGE_CHANNELS = 64
CAMERA_NO = 1

#default crop
x1 = 0
x2 = FRAME_HEIGHT
y1 = 0
y2 = FRAME_WIDTH

#default user information
user_no = 100
Gender = 1 # Male = 1 | Female = 2
age = 32
eye_color = 1 # Brown = 1 | Black	= 2 | Blue = 3 | Green = 4

def run_task(X,Y,U,screen,cogload):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("\ntask is loaded. Press 's' to start recording data. Data Recording will be started after 3 seconds after pressing 's'\nPlease press 'Esc' key to stop data recording and save the file")
	while(chr(cv2.waitKey()) != 's'):
		continue
	t1 = int(round(time.time() * 1000))
	while(int(round(time.time() * 1000)) - t1 < 3000):
		continue
	while True:		
		ret, frame = cap.read()
		frame  = frame[x1:x2, y1:y2]
		gray = cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2GRAY)
		cv2.imshow("eye", gray)
		j = cv2.waitKey(2)
		if(j == 27):
			break
		one_data[:,:,i%IMAGE_CHANNELS] = gray
		if(i%IMAGE_CHANNELS == IMAGE_CHANNELS - 1):
			X.append(one_data)
			Y.append(np.transpose([screen, 0, 0, 0, cogload, 0, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("\nFinished\n")

def h5_create(datapath):
	x_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)
	y_shape = (1,7)
	u_shape = (4,1) #user no, gender, age, eye color
	t_shape = (1,1)
	with h5py.File(datapath, mode='a') as h5f:
		xdset = h5f.create_dataset('X', (0,) + x_shape, maxshape=(None,) + x_shape, dtype='uint8', chunks=(128,) + x_shape)
		ydset = h5f.create_dataset('Y', (0,) + y_shape, maxshape=(None,) + y_shape, dtype='uint8', chunks=(128,) + y_shape)
		udset = h5f.create_dataset('U', (0,) + u_shape, maxshape=(None,) + u_shape, dtype='uint8', chunks=(128,) + u_shape)
		tdset = h5f.create_dataset('T', (0,) + t_shape, maxshape=(None,) + t_shape, dtype='uint8', chunks=(128,) + t_shape)

def h5_append(datapath, U, X, Y, T):
	x_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)
	y_shape = (1,7)
	u_shape = (1,4) #user no, gender, age, eye color
	t_shape = (1,1)
	with h5py.File(datapath, mode='a') as h5f:
		xdset = h5f['X']
		ydset = h5f['Y']
		udset = h5f['U']
		tdset = h5f['T']
		
		for i in range(X.shape[0]):
			xdset.resize(xdset.shape[0]+1, axis=0)
			xdset[-1:] = X[i]
			print(xdset.shape)
		for i in range(X.shape[0]):
			ydset.resize(ydset.shape[0]+1, axis=0)
			ydset[-1:] = Y[i]
			print(ydset.shape)
		for i in range(X.shape[0]):
			udset.resize(udset.shape[0]+1, axis=0)
			udset[-1:] = U[0]
			print(udset.shape)
		for i in range(X.shape[0]):
			tdset.resize(tdset.shape[0]+1, axis=0)
			tdset[-1:] = T[0]
			print(tdset.shape)

def crop_and_focus(CAMERA_NO, cap):
	eye_focus.setup_camera(CAMERA_NO, cap, mode="manual")
	x,y = detect_iris.get_cordinates(cap, mode="manual")
	if(x < IMAGE_HEIGHT/2):
		x = IMAGE_HEIGHT/2
	if(x > FRAME_HEIGHT - IMAGE_HEIGHT/2):
		x = FRAME_HEIGHT - IMAGE_HEIGHT/2
	if(y < IMAGE_WIDTH/2):
		y = IMAGE_WIDTH/2
	if(y > FRAME_WIDTH - IMAGE_WIDTH/2):
		y = FRAME_WIDTH - IMAGE_WIDTH/2
	return int(x),int(y)

#arguements 
parser = argparse.ArgumentParser()

parser.add_argument('--screen', action="store", type=np.uint8, default=0)
parser.add_argument('--cogload', action="store", type=np.uint8, default=0)
parser.add_argument('--tasknumber', action="store", type=np.uint8, default=0)
parser.add_argument('--camera', required=True, type=np.uint8)
parser.add_argument('--filepath', required=True, help='Where to save the file')
args = parser.parse_args()

cogload = args.cogload
screen = args.screen
tasknumber = args.tasknumber
filepath = args.filepath
CAMERA_NO = args.camera

#user information
user_no = np.int(input("enter user number :"))
Gender = input("enter user gender (Male = 1 | Female = 2) : ")
age = input("enter user age :")
eye_color = input("enter eye-color (Brown = 1 | Black = 2 | Blue = 3 | Blue-ish green = 4 | Green = 5 | Other = 6) : ")

cap = cv2.VideoCapture(CAMERA_NO)	
while(True):
	x_center, y_center = crop_and_focus(CAMERA_NO, cap)
	x1 = x_center - int(IMAGE_HEIGHT / 2)
	x2 = x_center + int(IMAGE_HEIGHT / 2)
	y1 = y_center - int(IMAGE_WIDTH / 2)
	y2 = y_center + int(IMAGE_WIDTH / 2)

	ret, frame1 = cap.read()
	frame  = frame1[ x1:x2 , y1:y2 ].copy()
	cv2.imshow('cropped_frame',frame)
	print("Does the image look okay to continue? - 'y' or 'n' (it's okay if about 85\% of the white region is focused and visible) : ")
	if cv2.waitKey() & 0xFF == ord('y'):
		break

# count1 = 0
# while(True):
# 	count1 = count1 + 1    
# 	ret, frame1 = cap.read()
# 	frame  = frame1[ x1:x2 , y1:y2 ].copy()
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	cv2.imshow('cropped_frame',frame)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 	    break

X = []
Y = []
U = np.reshape(np.asarray(np.transpose([np.int(user_no),np.int(Gender),np.int(age),np.int(eye_color)])),[4,1]) #user no, gender, age, eye color

# print("Press 's' to start")

# while chr(cv2.waitKey()) != 's':
# 	continue



run_task(X,Y,U,screen,cogload)

datetime_object = datetime.datetime.now()
if (platform.system() == 'Windows'):
	date_time = datetime_object.strftime("%m-%d-%Y %H;%M;%S")
else :
	date_time = str(datetime_object)
filename = filepath + "user_" + str(user_no) + " " + date_time + ".h5"

X_train = np.asarray(X)
Y_train = np.asarray(Y)

T = np.reshape(np.asarray(tasknumber),[1,1])

h5_create(filename)
h5_append(filename, U, X_train, Y_train, T)

cap.release()
cv2.destroyAllWindows()
