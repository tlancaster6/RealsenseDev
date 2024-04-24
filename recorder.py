import pyrealsense2 as rs
import cv2
import pathlib
import numpy as np
import time

OUTPUT_DIR = pathlib.Path().home() / 'Videos'

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()


class Recorder:

    def __init__(self, framerate=30, framesize=(640, 480)):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.output_dir = OUTPUT_DIR
        self.rs_format = rs.format.y8
        self.framerate = framerate
        self.framesize = framesize
        self.config, self.pipeline, self.profile, self.serial = self.enable_device()
        self.outfile = OUTPUT_DIR / f"{self.serial}.avi"
        self.writer = cv2.VideoWriter(str(self.outfile), self.fourcc, framerate, (framesize[0]*2, framesize[1]), 0)
        self.framecount = 0

    def enable_device(self):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.infrared, 1, *self.framesize, self.rs_format, self.framerate)
        config.enable_stream(rs.stream.infrared, 2, *self.framesize, self.rs_format, self.framerate)
        profile = pipeline.start(config)

        device = profile.get_device()
        serial = device.get_info(rs.camera_info.serial_number)
        depth_sensor = device.query_sensors()[0]
        if depth_sensor.supports(rs.option.emitter_enabled):
            depth_sensor.set_option(rs.option.emitter_enabled, 0)
        return config, pipeline, profile, serial

    def aquire_frame(self):
        frames = self.pipeline.wait_for_frames()
        ir1_frame = frames.get_infrared_frame(1)
        ir2_frame = frames.get_infrared_frame(2)
        image1 = np.asanyarray(ir1_frame.get_data())
        image2 = np.asanyarray(ir2_frame.get_data())
        return np.hstack([image1, image2])

    def write_frame(self, frame):
        self.writer.write(frame)
        self.framecount += 1

    def record(self, length=10):
        end = time.time() + length
        while time.time() <= end:
            self.write_frame(self.aquire_frame())

    def exit(self):
        self.writer.release()
        self.pipeline.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()


if __name__ == "__main__":
    with Recorder() as recorder:
        recorder.record()





