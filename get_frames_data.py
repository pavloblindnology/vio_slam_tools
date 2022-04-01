#!/usr/bin/env python3

# Get frames data from topic files.

import os
import copy
import csv
import time
import argparse
from collections import OrderedDict
import topic_utils

itopic = 0

def parse_frames(fname):
	'''Parse frames timestamps.'''
	frames = []
	with open(fname, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			frames.append(OrderedDict({'ts': int(row[0]), 'png': row[1]}))

	return frames

def interpolate_data(frames, data, ts_key, keys, suff_key, method, extrapolate = True):
	'''Interpolate general frames data.'''
	n_data = len(data)
	i = 0
	iframe = 0
	start = time.time()
	for frame in frames:
		# Show progress
		if iframe % 10 == 0:
			print('Interpolating frame %i / %i' % (iframe, len(frames)), end='\r')
		iframe += 1

		ts_frame = frame['ts']
		for i in range(i, n_data):
			ts_data = data[i][ts_key] * 0.001 # Nanoseconds to microseconds
			if (ts_data > ts_frame):
				break
			i += 1
		# Pre-extrapolate
		if (i == 0):
			if extrapolate:
				for key in keys:
					frame[key+suff_key] = data[i][key]
		# Post-extrapolate
		elif (i == n_data):
			if extrapolate:
				for key in keys:
					frame[key+suff_key] = data[-1][key]
			else:
				# No need to continue for the rest of the frames
				break
		# Interpolate
		else:
			ts_data_prev = data[i-1][ts_key] * 0.001 # Nanoseconds to microseconds
			# Linear
			if (method == "linear"):
				w = (ts_frame - ts_data_prev) / (ts_data - ts_data_prev)
			# Nearest
			else:
				if (ts_frame - ts_data_prev > ts_data - ts_frame):
					w = 1.0
				else:
					w = 0.0
			for key in keys:
				val = data[i][key]
				val_prev = data[i-1][key]
				if type(val) is dict:
					frame[key+suff_key] = {}
					for sub_key in val:
						frame[key+suff_key][sub_key] = (1-w)*val_prev[sub_key] + w*val[sub_key]
				else:
					frame[key+suff_key] = (1-w)*val_prev + w*val
	print("")
	end = time.time()
	print("Interpolate time (s): %.1f" % (end - start))

	return frames

def add_topic_data(frames, fname, ts_key, keys, method = 'nearest', extrapolate = True):
	'''Add general topic data to frames.'''
	print("----------Processing %s" % (fname))
	# Parse all keys (including timestamp key)
	keys_all = copy.deepcopy(keys)
	keys_all.append(ts_key)
	data = topic_utils.parse_topic_file(fname, keys_all)
	if len(data) == 0:
		return
	# Add topic index as suffix to keys (bcz topics can have duplicate keys)
	global itopic
	if (itopic > 0):
		suff_key = str(itopic)
	else:
		suff_key = ''
	frames = interpolate_data(frames, data, ts_key, keys, suff_key, method, extrapolate)
	itopic += 1
	return frames

def main():
	# Parse arguments
	parser = argparse.ArgumentParser(description=
		"Get frames data from topic files.\n"
		"-------------------------------------\n"
		"For every frame from frames.txt, get interpolated data from:\n"
		"LocalPoseTopic.txt - pos, vel, att (nearest neighbor interpolation).\n"
		"SensorGPSTopic.txt - pos (renamed to pos1, linear interpolation).\n"
		"Constant extrapolation is used for both topic files.\n"
		"Output results to CSV file. Nested dictionaries are flattened.\n"
		"Examples:\n"
		"get_frames_data.py - process current directory\n"
		"get_frames_data.py ./0382-frames - process '0382-frames' directory\n"
		"get_frames_data.py ./0382-frames -o 0382-frames_data.txt - process\n"
		"'0382-frames' directory, output to 0382-frames_data.txt file.\n"
		, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("dir", nargs='?', type=str, default=".", help="Folder to process (default: %(default)s)")
	parser.add_argument("-ts", "--ts-key", type=str, default="timeNS", help="Time stamp key in topic file (default: %(default)s)")
	parser.add_argument("-o", "--outfile", type=str, default="frames_data.txt", help="Output file (default: %(default)s)")
	args = parser.parse_args()

	# Read frames file
	frames = parse_frames(os.path.join(args.dir, 'frames.txt'))

	# Parse topic files
	frames = add_topic_data(frames, os.path.join(args.dir, 'LocalPoseTopic.txt'),
		args.ts_key, ['pos', 'vel', 'att'], 'nearest', True)

	frames = add_topic_data(frames, os.path.join(args.dir, 'SensorGPSTopic.txt'),
		args.ts_key, ['pos'], 'linear', True)

	# Write frames data
	topic_utils.write_frames(frames, os.path.join(args.dir, args.outfile))

	return

if __name__ == '__main__':
	main()