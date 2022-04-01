# Topic utils

import csv
import time
import yaml
from collections import OrderedDict
from collections.abc import MutableMapping

def _flatten_dict_gen(d, parent_key, sep):
	'''Parse frames timestamps (https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/).'''
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		if isinstance(v, MutableMapping):
			yield from flatten_dict(v, new_key, sep=sep).items()
		else:
			yield new_key, v


def flatten_dict(d = MutableMapping, parent_key = '', sep = '.'):
	return dict(_flatten_dict_gen(d, parent_key, sep))


def parse_topic_file(fname, keys):
	'''Parse general topic file.'''
	data = []
	# Open YAML
	try:
		start = time.time()
		
		# Parse each YAML doc individually and only needed keys (much faster) 
		i = 0
		with open(fname, 'r') as file:
			for line in file:
				# Show progress
				if i % 1000 == 0:
					print('Parsing line %i' % (i), end='\r')
				i += 1
				# Skip this line
				if (line.startswith('LocalPoseTopic')):
					continue
				# Start of YAML document
				if (line == 'topic:\n'):
					yaml_doc = ""
					continue
				# End of YAML document, parse
				if (line == '===\n'):
					data_line = yaml.safe_load(yaml_doc)
					# Sort by keys
					data_line_ordered = OrderedDict()
					for key in keys:
						if (key in data_line):
							data_line_ordered[key] = data_line[key]
					data.append(data_line_ordered)
					continue
				# Use only needed keys for YAML to speed-up parsing 
				line = line.lstrip()
				delim_pos = line.find(':')
				if (delim_pos >= 0):
					key = line[:delim_pos]
					if (key in keys):
						yaml_doc += line
		print("")

		# Parse whole text file
		# with open(fname, 'r') as file:
		# 	text = file.read()
		# 	# Reformat to multiple YAML documents
		# 	text1 = text.replace('===\n', '---\n')
		# 	# Parse
		# 	data = list(yaml.safe_load_all(text1))

		end = time.time()
		print("Parse time (s): %.1f" % (end - start))
	except:
		print("Error attempting to load YAML: " + fname)
		return []
	
	return data

def write_frames(frames, fname):
	'''Write frames data.'''
	print("----------Writing %s" % (fname))
	start = time.time()
	iframe = 0
	with open(fname, 'w') as file:
		writer = csv.writer(file)
		for frame in frames:
			# Show progress
			if (iframe % 1000 == 0):
				print('Writing frame %i / %i' % (iframe, len(frames)), end='\r')
			iframe += 1

			frame_flatten = flatten_dict(frame)
			# Write header
			if (iframe == 1):
				file.write('#' + ', '.join(frame_flatten.keys())+'\n')
			# Write row
			writer.writerow(frame_flatten.values())
			#file.write(yaml.dump(frame, width=float("inf"), default_flow_style=True))
	print("")
	end = time.time()
	print("Write time (s): %.1f" % (end - start))
