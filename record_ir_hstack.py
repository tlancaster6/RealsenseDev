import pyrealsense2 as rs
import numpy as np
import cv2
import pathlib

outfile = pathlib.Path().home() / 'Videos' / 'ir_recording_stacked.avi'

framerate = 30
framesize = (640, 480)
rs_format = rs.format.y8
fourcc = cv2.VideoWriter_fourcc(*'XVID')

output = cv2.VideoWriter(str(outfile), fourcc, framerate, (framesize[0]*2, framesize[1]), 0)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, *framesize, rs_format, framerate)
config.enable_stream(rs.stream.infrared, 2, *framesize, rs_format, framerate)
profile = pipeline.start(config)

device = profile.get_device()
depth_sensor = device.query_sensors()[0]
if depth_sensor.supports(rs.option.emitter_enabled):
    depth_sensor.set_option(rs.option.emitter_enabled, 0)

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

        output.write(np.hstack([image1, image2]))

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
    output.release()
