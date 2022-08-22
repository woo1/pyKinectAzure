import sys
import cv2
import os.path as osp

sys.path.insert(1, '../')
import pykinect_azure as pykinect
import time
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='body pose')
	parser.add_argument('--mkv_path', type=str, default="")
	args = parser.parse_args()

	video_filename = args.mkv_path

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Start playback
	playback = pykinect.start_playback(video_filename)

	playback_config = playback.get_record_configuration()
	# print(playback_config)

	cv2.namedWindow('Depth Image',cv2.WINDOW_NORMAL)
	none_bf = 0
	while playback.isOpened():

		# Get camera capture
		capture = playback.update()

		# Get the colored depth
		ret, depth_color_image = capture.get_colored_depth_image()
		
		# Plot the image
		print('depth_color_image', depth_color_image)
		if depth_color_image is not None:
			cv2.imshow('Depth Image',depth_color_image)
		else:
			if none_bf > 10:
				time.sleep(5)
				break

			none_bf += 1

		# Press q key to stop
		if cv2.waitKey(30) == ord('q'): 
			break