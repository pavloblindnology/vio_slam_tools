#!/usr/bin/env python

# Compute Tbc matrix from RPY for IMU and camera.

import os
import argparse
import numpy as np
from scipy.spatial.transform import Rotation as R

def main():
	# Parse arguments
	parser = argparse.ArgumentParser(description=
		"Compute T_b_c transformation matrix from IMU to camera based on IMU and camera poses.\n"
		"-------------------------------------\n"
		"Examples:\n"
		"tbc_compute.py -ri 180 0 -90 -ti 0.1 0 0 -rc 0 0 90 -tc 0 0 0.2\n"
		, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-ri', nargs=3, default=[0, 0, 0], help="Rotation RPY for IMU")
	parser.add_argument('-ti', nargs=3, default=[0, 0, 0], help="Translaton XYZ for IMU")
	parser.add_argument('-rc', nargs=3, default=[0, 0, 0], help="Rotation RPY for camera")
	parser.add_argument('-tc', nargs=3, default=[0, 0, 0], help="Translaton XYZ for camera")
	args = parser.parse_args()

	# World -> imu matrix
	#r_wb = R.from_euler('xyz', [179.62, -0.392, -90], degrees=True)
	r_wb = R.from_euler('xyz', args.ri, degrees=True)
	t_wb = np.identity(4)
	t_wb[:3, :3] = r_wb.as_dcm()
	#t_wb[:3, 3] = [0.0827, 0.0225, 0.0425]
	t_wb[:3, 3] = args.ti
	print("World -> IMU matrix\n", t_wb)

	# World -> camera matrix
	#r_wc = R.from_euler('xyz', [-0.24558, 0.213438, 90], degrees=True)
	r_wc = R.from_euler('xyz', args.rc, degrees=True)
	t_wc = np.identity(4)
	t_wc[:3, :3] = r_wb.as_dcm()
	#t_wc[:3, 3] = [-0.1093, 0.0, 0.063]
	t_wc[:3, 3] = args.tc
	print("\nWorld -> camera matrix\n", t_wc)

	# imu -> camera matrix
	t_bc = np.linalg.inv(t_wb) * t_wc
	print("\nIMU -> camera matrix\n", t_bc)

	return

if __name__ == '__main__':
	main()