import pyrealsense2 as rs


class Recorder:

    def __init__(self):
        self.context = rs.context()
        self.devices = self.context.devices

    def configure_devices(self):
        configs = []
        for device in self.devices:
            serial_number = device.get_info(rs.camera_info.serial_number)
            config = rs.config()
            config.enable_device(str(serial_number))
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.y8, 30)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.y8, 30)
            configs.append(config)
        return configs

    def start(self, config):
        pipeline = rs.pipeline()
        pipeline.start(config)
        return pipeline


recorder = Recorder()
