import sys
import cv2
import json
import os.path as osp
import glob
from tqdm import tqdm
import argparse
import os

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='body pose')
	parser.add_argument('--data_dir', type=str, default="")
	args = parser.parse_args()

	data_dir = args.data_dir
	path_list = glob.glob(osp.join(data_dir, '*.mkv'))
	# path_list.sort()
	for video_filename in tqdm(path_list):
		fnm = osp.basename(video_filename)

		# Initialize the library, if the library is not found, add the library path as argument
		pykinect.initialize_libraries(track_body=True)

		# Start playback
		playback = pykinect.start_playback(video_filename)

		playback_config = playback.get_record_configuration()
		# print(playback_config)

		playback_calibration = playback.get_calibration()

		# Start body tracker
		bodyTracker = pykinect.start_body_tracker(calibration=playback_calibration)

		cv2.namedWindow(f'[{fnm}] Depth image with skeleton',cv2.WINDOW_NORMAL)
		idx = -1
		while playback.isOpened():

			# Get camera capture
			capture = playback.update()
			idx += 1

			# Get body tracker frame
			try:
				body_frame = bodyTracker.update(capture=capture)
			except:
				continue

			bodies = body_frame.get_bodies()
			fnm_base = osp.splitext(fnm)[0]
			sav_dir = osp.join(data_dir, fnm_base)
			os.makedirs(sav_dir, exist_ok=True)

			with open(osp.join(sav_dir, str(idx)+".json"), "w") as json_file:
				if len(bodies) > 0:
					json.dump(bodies[0].json(), json_file)
				else:
					print(f'no body in {fnm}')

			# Get the colored depth
			ret, depth_color_image = capture.get_colored_depth_image()

			# Get the colored body segmentation
			ret, body_image_color = body_frame.get_segmentation_image()

			if not ret:
				continue

			# Combine both images
			combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)

			# Draw the skeletons
			combined_image = body_frame.draw_bodies(combined_image)

			# Overlay body segmentation on depth image
			cv2.imshow('Depth image with skeleton',combined_image)

			# Press q key to stop
			if cv2.waitKey(1) == ord('q'):
				break