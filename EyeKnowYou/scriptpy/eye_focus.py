import os
import numpy as np 
import cv2

AUTO_FOCUS_1 = 'uvcdynctrl -d video'
AUTO_FOCUS_2 = ' --set=\'Focus, Auto\' '
SET_FOCUS_1 = 'uvcdynctrl --device=video'
SET_FOCUS_2 = ' --set=\'Focus (absolute)\' '
FOCUL_CONTINUITY = 5
FOCUS_ATTEMPTS = 5
BLUR_ERROR = 3
INITIAL_OPTIMAL_FOCUS = 25

max_thresh = 50
blur_thresh = 150
max_focus_level = 40
min_focus_level = 10
focus_level = 1
schmidtrigger = 10
max_flag = False
optimal_focal_level = INITIAL_OPTIMAL_FOCUS

def disable_autofocus(camera):
	auto_focus = 0
	AUTO_FOCUS = AUTO_FOCUS_1 + str(camera) + AUTO_FOCUS_2 + str(auto_focus)
	response = os.popen(AUTO_FOCUS).read()
	print(response)
	print("if no error messege was printed just above, succesfully disabled autofocus\n")

def enable_autofocus(camera):
	auto_focus = 1
	AUTO_FOCUS = AUTO_FOCUS_1 + str(camera) + AUTO_FOCUS_2 + str(auto_focus)
	response = os.popen(AUTO_FOCUS).read()
	print(response)
	print("if no error messege was printed just above, succesfully enabled autofocus\n")

def set_focus(camera, focus_level):
	SET_FOCUS = SET_FOCUS_1 + str(camera) + SET_FOCUS_2 + str(focus_level)
	focus_resoponse = os.popen(SET_FOCUS).read()

def image_is_out_of_focus(image, prev_sharpness):
	global schmidtrigger
	global max_thresh
	global blur_thresh
	global max_focus_level
	global min_focus_level
	global max_flag
	global focus_level
	global optimal_focal_level

	sharpness = cv2.Laplacian(image, cv2.CV_64F).var()
	diff = sharpness - prev_sharpness
	if(sharpness > max_thresh):
		max_thresh = sharpness
		max_focus_level = focus_level + schmidtrigger
		min_focus_level = focus_level - schmidtrigger
		optimal_focal_level = focus_level
	# print(blur_thresh)
	if(sharpness < blur_thresh):
		return True, sharpness
	else:
		return False, sharpness

def manual_focus(camera, cap):
	disable_autofocus(camera)
	print("Focus using 'i' (in) and 'o' (out) keys of the keyboard. Press 'q' after focusing.\n")
	focus = 30
	while(True):
		ret, frame = cap.read()
		image = cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2GRAY)
		cv2.imshow('focusing',frame)
		j = cv2.waitKey(1)
		if j == ord('q') :
			break
		elif j == ord('i'):
			focus = focus + 1
			set_focus(camera, focus)
		elif j == ord('o'):
			focus = focus - 1
			set_focus(camera, focus)

def calibrate(camera, cap):
	global schmidtrigger
	global max_thresh
	global blur_thresh
	global max_focus_level
	global min_focus_level
	global focus_level
	global optimal_focal_level

	disable_autofocus(camera)

	focus_level = min_focus_level
	not_focused = True
	focus_toggle = False
	focused_frames = 0
	increment = 1
	toggle_count = 0
	try_count = 0
	prev_sharpness = 0
	local_maximum = max_thresh
	local_max_focus_level = max_focus_level
	local_min_focus_level = min_focus_level
	max_not_found = True
	local_optimal_focus = INITIAL_OPTIMAL_FOCUS

	while(True):
		res = input("\n\nTurn your face towards the monitor. look at the middle of the monitor, keep your eyes open wide. This is will only take 5-10 seconds. Try to keep a low blinking frequency and type c and pres enter to start calibration. ")
		if(res == 'c'):
			break

	while(not_focused):
		status = "Calibrating Camera" + "|" + "-" * focus_level + "|"
		print(status, end="\r")
		ret, frame = cap.read()
		image = cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2GRAY)
		cv2.imshow('focusing',frame)
		cv2.waitKey(3)
		if(max_not_found):
			for xx in range(1):
				while(focus_level < local_max_focus_level):
					focus_level = focus_level + 1
					set_focus(camera, focus_level)
					ret, frame = cap.read()
					image = cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2GRAY)
					cv2.imshow('focusing',frame)
					cv2.waitKey(3)
					out_of_focus, prev_sharpness = image_is_out_of_focus(image, prev_sharpness)
				while(focus_level > local_min_focus_level):
					focus_level = focus_level - 1
					set_focus(camera, focus_level)
					ret, frame = cap.read()
					image = cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2GRAY)
					cv2.imshow('focusing',frame)
					cv2.waitKey(3)
					out_of_focus, prev_sharpness = image_is_out_of_focus(image, prev_sharpness)
			local_optimal_focus = optimal_focal_level		
			local_maximum = max_thresh
			max_thresh = 0
			blur_thresh = local_maximum - BLUR_ERROR
			max_not_found = False
			local_max_focus_level = optimal_focal_level + schmidtrigger
			local_min_focus_level = optimal_focal_level - schmidtrigger
			focus_level = local_optimal_focus
			set_focus(camera, focus_level)
		out_of_focus, prev_sharpness = image_is_out_of_focus(image, prev_sharpness)
		if(out_of_focus):
			focused_frames = 0
			if(focus_level > local_max_focus_level or focus_level < local_min_focus_level):
				increment = -1 * increment
				try_count = try_count + 1
				if(try_count == FOCUS_ATTEMPTS - 2):
					max_not_found = True
				if(try_count > FOCUS_ATTEMPTS):
					print("Calibration Unsuccessful. Please Try again if ncessary. Falling bacl to local optimal value = " + str(local_optimal_focus))
					set_focus(camera, local_optimal_focus)
					break
			focus_level = focus_level + increment
			set_focus(camera, focus_level)
		else:
			focused_frames = focused_frames + 1
		if(focused_frames > FOCUL_CONTINUITY):
			not_focused = False 
			print("Calibration Successful !!!")


def setup_camera(camera, cap, mode="manual"):
	if(mode == "manual"):
		manual_focus(camera, cap)
	else:
		calibrate(camera, cap)
	print("Camera succesfully calibrated\n")


# camera = 1
# cap = cv2.VideoCapture(camera)
# setup_camera(camera, cap)


# while(True):
# 	ret, frame = cap.read()
# 	cv2.imshow('frame_cropped',frame)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 	    break
# cap.release()
# cv2.destroyAllWindows()




