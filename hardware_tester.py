from recorder import Recorder, OUTPUT_DIR
import pandas as pd
from os.path import getsize
import time


class HardwareTester:

    def __init__(self):
        self.results = []

    def run_test(self, framerate, framesize, test_length=10):
        print(f'testing with framerate={framerate}, framesize={framesize}')
        recorder = Recorder(framerate, framesize)
        n_write_ops = 0
        total_write_time = 0
        end = time.time() + test_length
        while time.time() <= end:
            frame = recorder.aquire_frame()
            write_start = time.time()
            recorder.write_frame(frame)
            total_write_time += time.time() - write_start
            n_write_ops += 1
        recorder.exit()
        results = {
            'target_framerate': framerate,
            'resolution': framesize,
            'test_len_secs': test_length,
            'n_write_ops': n_write_ops,
            'avg_write_time': total_write_time / n_write_ops,
            'allowable_write_time': 1 / framerate,
            'file_size_my': getsize(str(recorder.outfile)) * 10e-6
        }
        self.results.append(results)

    def compile_results(self, save=True):
        self.results = pd.DataFrame(self.results)
        if save:
            self.results.to_csv(str(OUTPUT_DIR / 'testing_results.csv'))


if __name__ == "__main__":
    tester = HardwareTester()
    for framerate in [6, 15, 30]:
        tester.run_test(framerate=framerate, framesize=(1280, 720), test_length=10)
        time.sleep(1)
    for framerate in [6, 15, 30, 60, 90]:
        for framesize in [(848, 480), (640, 480), (640, 360), (480, 720), (424, 240)]:
            tester.run_test(framerate=framerate, framesize=framesize)
            time.sleep(1)
    tester.compile_results()







