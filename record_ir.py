import pyrealsense2 as rs
import numpy as np
import cv2
import pathlib

outfile1 = pathlib.Path().home() / 'Videos' / 'ir_recording_1.avi'
outfile2 = pathlib.Path().home() / 'Videos' / 'ir_recording_2.avi'

framerate = 30
framesize = (640, 480)
rs_format = rs.format.y8
fourcc = cv2.VideoWriter_fourcc(*'XVID')

output1 = cv2.VideoWriter(str(outfile1), fourcc, framerate, framesize, 0)
output2 = cv2.VideoWriter(str(outfile2), fourcc, framerate, framesize, 0)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, *framesize, rs_format, framerate)
config.enable_stream(rs.stream.infrared, 2, *framesize, rs_format, framerate)
profile = pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        ir1_frame = frames.get_infrared_frame(1)
        ir2_frame = frames.get_infrared_frame(2)
        if not ir1_frame or not ir2_frame:
            continue
        image1 = np.asanyarray(ir1_frame.get_data())
        image2 = np.asanyarray(ir2_frame.get_data())
        cv2.namedWindow('IR Example 1', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('IR Example 2', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('IR Example 1', image1)
        cv2.imshow('IR Example 2', image2)

        output1.write(image1)
        output2.write(image2)

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
    output1.release()
    output2.release()
