# vio_slam_tools
Tools to prepare frames &amp; telemetry data for VIO SLAM

##Tools

* `get_frames_data.py` - For each frame timestamp interpolates data from topic files `LocalPoseTopic.txt` and `SensorGPSTopic.txt`. 

* `topic2csv.py` - Converts topic data file to CSV file (for VIO ORB_SLAM3).

* `tbc_compute.py` - Compute `T_b_c` transformation matrix from IMU to camera based on IMU and camera poses in base frame (for VIO ORB_SLAM3).
