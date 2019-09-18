   # X contains images of size (300, 440, 3)
# Y contains vecors of size (7,1) : [screen, paper, person close, other, low cognitive load, medium cognitive load, high cognitive load]

#!home/tkal976/.virtualenvs/cv/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import h5py
import eye_focus as eye_focus
import detect_iris as detect_iris

#original frame
FRAME_HEIGHT = 480
FRAME_WIDTH = 640

#cropped frame
IMAGE_WIDTH = 384
IMAGE_HEIGHT = 256
IMAGE_CHANNELS = 64
CAMERA_NO = 0
Y_ADJUSMENT = 60
x1 = 0
x2 = FRAME_HEIGHT
y1 = 0
y2 = FRAME_WIDTH

#user information
user_no = 7
Gender = 1 # Male = 1 | Female = 2
age = 32
eye_color = 1 # Brown = 1 | Black	= 2 | Blue = 3 | Blue-ish green = 4

def paper_low(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("paper_low test is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
		continue
	t1 = int(round(time.time() * 1000))
	while(int(round(time.time() * 1000)) - t1 < 5000):
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
			T.append(1)
			Y.append(np.transpose([0, 1, 0, 0, 1, 0, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def paper_medium(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("paper_medium is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
		continue
	t1 = int(round(time.time() * 1000))
	while(int(round(time.time() * 1000)) - t1 < 5000):
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
			T.append(2)
			Y.append(np.transpose([0, 1, 0, 0, 0, 1, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def paper_high(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("paper_high is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
		continue
	t1 = int(round(time.time() * 1000))
	while(int(round(time.time() * 1000)) - t1 < 5000):
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
			T.append(3)
			Y.append(np.transpose([0, 1, 0, 0, 0, 0, 1]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def screen_low(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("screen_low is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
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
			T.append(4)
			Y.append(np.transpose([1, 0, 0, 0, 1, 0, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def screen_medium_1(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("screen_medium for a non software person is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
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
		# print(i%IMAGE_CHANNELS)
		if(i%IMAGE_CHANNELS == IMAGE_CHANNELS - 1):
			X.append(one_data)
			T.append(5)
			Y.append(np.transpose([1, 0, 0, 0, 0, 1, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def screen_medium_2(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("screen_medium for a software person is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
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
			T.append(6)
			Y.append(np.transpose([1, 0, 0, 0, 0, 1, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def screen_high(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("screen_high is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
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
			T.append(7)
			Y.append(np.transpose([1, 0, 0, 0, 0, 0, 1]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def person_low(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("person_low is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
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
			T.append(8)
			Y.append(np.transpose([0, 0, 1, 0, 1, 0, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def person_medium(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("person_medium is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
		continue
	t1 = int(round(time.time() * 1000))
	while(int(round(time.time() * 1000)) - t1 < 5000):
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
			T.append(9)
			Y.append(np.transpose([0, 0, 1, 0, 0, 1, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def other(X,Y,T,U):
	global x1, x2, y1, y2
	one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
	i = 0
	print("nothing is loaded. Press 's' to start recording data")
	while(chr(cv2.waitKey()) != 's'):
		continue
	t1 = int(round(time.time() * 1000))
	while(int(round(time.time() * 1000)) - t1 < 5000):
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
			T.append(0)
			Y.append(np.transpose([0, 0, 0, 1, 1, 0, 0]))
			print(i)
			one_data = np.zeros((x2-x1, y2-y1, IMAGE_CHANNELS))
		i = i + 1
	print("Finished")

def h5_create(datapath):
	x_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)
	y_shape = (1,7)
	u_shape = (4,1) #user no, gender, age, eye color
	t_shape = (1,1)
	with h5py.File(datapath, mode='a') as h5f:
		xdset = h5f.create_dataset('X', (0,) + x_shape, maxshape=(None,) + x_shape, dtype='uint8', chunks=(128,) + x_shape)
		ydset = h5f.create_dataset('Y', (0,) + y_shape, maxshape=(None,) + y_shape, dtype='uint8', chunks=(128,) + y_shape)
		udset = h5f.create_dataset('U', (0,) + u_shape, maxshape=(None,) + u_shape, dtype='uint8', chunks=(128,) + u_shape)
		tdset = h5f.create_dataset('T', (0,) + t_shape, maxshape=(None,) + u_shape, dtype='uint8', chunks=(128,) + u_shape)

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
	eye_focus.setup_camera(CAMERA_NO, cap)
	y,x = detect_iris.get_cordinates(cap)
	y = y - Y_ADJUSMENT
	print(y)
	if(x < IMAGE_HEIGHT/2):
		x = IMAGE_HEIGHT/2
	if(x > FRAME_HEIGHT - IMAGE_HEIGHT/2):
		x = FRAME_HEIGHT - IMAGE_HEIGHT/2
	if(y < IMAGE_WIDTH/2):
		y = IMAGE_WIDTH/2
	if(y > FRAME_WIDTH - IMAGE_WIDTH/2):
		y = FRAME_WIDTH - IMAGE_WIDTH/2
	return int(x),int(y)

def main():
	cap = cv2.VideoCapture(CAMERA_NO)
	x_center, y_center = crop_and_focus(CAMERA_NO, cap)
	x1 = x_center - int(IMAGE_HEIGHT / 2)
	x2 = x_center + int(IMAGE_HEIGHT / 2)
	y1 = y_center - int(IMAGE_WIDTH / 2)
	y2 = y_center + int(IMAGE_WIDTH / 2)
	print([x1,x2,y1,y2])

	count1 = 0
	while(True):
		count1 = count1 + 1    
		ret, frame1 = cap.read()
		frame  = frame1[ x1:x2 , y1:y2 ].copy()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		cv2.imshow('cropped_frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break

	X = []
	Y = []
	T = []
	U = np.asarray(np.transpose([[user_no,Gender,age,eye_color]])) #user no, gender, age, eye color

	print("Press 's' to start")

	while chr(cv2.waitKey()) != 's':
		continue

	count = 0

	filename = 'tests.h5'

	while(True):
		count = count + 1    
		ret, frame = cap.read()
		print("Select Test")

		g = chr(cv2.waitKey())
		filename = str(user_no) + '_' + g + ".h5"
		print(filename)

		if(g == '0'):
			other(X,Y,T,U)
		if(g == '1'):
			paper_low(X,Y,T,U)
		if(g == '2'):
			paper_medium(X,Y,T,U)
		if(g == '3'):
			paper_high(X,Y,T,U)
		if(g == '4'):
			screen_low(X,Y,T,U)
		if(g == '5'):
			screen_medium_1(X,Y,T,U)
		if(g == '6'):
			screen_medium_2(X,Y,T,U)
		if(g == '7'):
			screen_high(X,Y,T,U)
		if(g == '8'):
			person_low(X,Y,T,U)
		if(g == '9'):
			person_medium(X,Y,T,U)

		if(count == 1):
			break

	X_train = np.asarray(X)
	Y_train = np.asarray(Y)

	T = np.asarray(T)

	h5_create(filename)
	h5_append(filename, U, X_train, Y_train, T)

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
    main()