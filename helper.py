# function to generate and save music video
import requests
from visualize import song_analysis, generate_images, save_video
from flask import Response
from image_groups import IMAGE_GROUPS
import random


def choose_classes(im_group):
	if im_group == None:
		im_group = random.sample(IMAGE_GROUPS.keys(), 1)[0]

	if len(IMAGE_GROUPS[im_group]) < 4:
		im_classes = IMAGE_GROUPS[im_group]
	else:
		im_classes = random.sample(IMAGE_GROUPS[im_group], 4)
	return im_classes


def check_entry(preview, video_id, resolution, im_group, jitter,
				depth, truncation, pitch_sensitivity, tempo_sensitivity,
				smooth_factor):

	r = requests.get(preview).status_code

	vis_url = 'http://artificial-artist.eba-cyfpphb2.us-east-1.elasticbeanstalk.com/visualize'

	classes = choose_classes(im_group)

	data = {"preview": preview, "video_id": video_id, "resolution": resolution,
			"classes": classes, "jitter": jitter, "depth": depth,
			"truncation": truncation, "pitch_sensitivity": pitch_sensitivity,
			"tempo_sensitivity": tempo_sensitivity, "smooth_factor": smooth_factor}

	if r == 200:
		try:
			requests.post(vis_url, json=data, timeout=3)
		except:
			pass
		return Response('Accepted', status=202, mimetype='application/json')

	else:
		return Response(f"{str(url)} not found.", status=404,
						mimetype='application/json')


def generate_and_save(preview, video_id, resolution, classes, jitter,
						depth, truncation, pitch_sensitivity, tempo_sensitivity,
						smooth_factor):

	song = requests.get(preview)

	open(f"{video_id}.mp3", 'wb').write(song.content)

	noise_vectors, class_vectors = song_analysis(f"{video_id}.mp3", classes,
												 jitter, depth, truncation,
												 pitch_sensitivity,
												 tempo_sensitivity, smooth_factor)

	tmp_folder_path = generate_images(video_id, noise_vectors, class_vectors, 
										resolution,truncation)

	return save_video(tmp_folder_path, f"{video_id}.mp3", video_id)
