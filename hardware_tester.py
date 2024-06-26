import cv2

from recorder import Recorder, OUTPUT_DIR
import pandas as pd
import numpy as np
from os.path import getsize
import time


class HardwareTester:

    def __init__(self):
        self.results = []

    def run_test(self, framerate, framesize, test_length=10, codec='H264', save_video=True, save_png=True):
        print(f'testing with framerate={framerate}, framesize={framesize}')
        outfile_suffix = f'{framesize[0]}x{framesize[1]}_{framerate}fps_{codec}'
        recorder = Recorder(framerate, framesize, outfile_suffix, codec)
        per_frame_processing_times = []
        end = time.time() + test_length
        while time.time() <= end:
            framestack = recorder.aquire_frame()
            frame_processing_start = time.time()
            recorder.write_frame(recorder.process_frame(framestack))
            if recorder.framecount > recorder.framerate:
                per_frame_processing_times.append(time.time() - frame_processing_start)
        if save_png:
            cv2.imwrite(str(recorder.outfile.with_suffix('.png')), recorder.process_frame(recorder.aquire_frame()))
        recorder.exit()
        results = {
            'target_framerate': framerate,
            'resolution': framesize,
            'test_len_secs': test_length,
            'n_frames_written': recorder.framecount,
            'avg_time_per_frame': np.mean(per_frame_processing_times),
            'max_time_per_frame': np.max(per_frame_processing_times),
            'median_time_per_frame': np.median(per_frame_processing_times),
            'stdev_time_per_frame': np.std(per_frame_processing_times),
            'allowable_time_per_frame': 1 / framerate,
            'file_size_mb': getsize(str(recorder.outfile)) * 10e-6,
            'codec': recorder.codec_string
        }
        if not save_video:
            recorder.outfile.unlink()
        self.results.append(results)

    def compile_results(self, save=True, outfile_suffix=None):
        self.results = pd.DataFrame(self.results)
        if save:
            filestem = 'testing_results'
            if outfile_suffix is not None:
                filestem = f'{filestem}_{outfile_suffix}'
            self.results.to_csv(str(OUTPUT_DIR / f'{filestem}.csv'))


if __name__ == "__main__":
    for codec in ['H264', 'X264', 'XVID']:
        tester = HardwareTester()
        print(f'\n\ntesting with {codec} codec')
        for framerate in [6, 15, 30]:
            tester.run_test(framerate=framerate, framesize=(1280, 720), test_length=10, codec=codec)
            time.sleep(1)
        for framerate in [6, 15, 30, 60, 90]:
            for framesize in [(848, 480), (640, 480), (640, 360), (480, 270), (424, 240)]:
                tester.run_test(framerate=framerate, framesize=framesize, test_length=10, codec=codec)
                time.sleep(1)
        tester.compile_results(outfile_suffix=codec)







