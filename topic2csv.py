#!/usr/bin/env python3

# Convert topic data file to csv.

import os
import argparse
import topic_utils

def main():
	# Parse arguments
	parser = argparse.ArgumentParser(description=
		"Convert topic data file to csv.\n"
		"-------------------------------------\n"
		"Examples:\n"
		"topic2csv.py LocalPoseTopic.txt - extract timestamps from LocalPoseTopic.txt\n"
		"topic2csv.py LocalPoseTopic.txt -k attRate acc - extract gyro & acc from LocalPoseTopic.txt\n"
		, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("infile", type=str, help="Input topic file to process")
	parser.add_argument("-ts", "--ts-key", type=str, default="timeNS", help="Time stamp key in topic file (default: %(default)s)")
	parser.add_argument('-k', '--keys', nargs='*', default=[], help="List of keys to convert")
	parser.add_argument("-o", "--outfile", type=str, default="", help="Output file (default: <file>.csv)")
	args = parser.parse_args()

	# Parse topic
	print("----------Parsing %s" % (args.infile))
	# Parse all keys (including timestamp key)
	keys_all = [args.ts_key]
	keys_all.extend(args.keys)
	data = topic_utils.parse_topic_file(args.infile, keys_all)
	if len(data) == 0:
		return

	# Write data
	# Use input file with csv extension if no outfile is specified
	if (args.outfile == ""):
		args.outfile = os.path.splitext(args.infile)[0] + '.csv'
	topic_utils.write_frames(data, args.outfile)

	return

if __name__ == '__main__':
	main()