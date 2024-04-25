import seaborn as sns
import pandas as pd

def load_hardware_test_df(path_to_df):
    df = pd.read_csv(str(path_to_df))
    df['resolution'] = df.resolution.apply(eval).apply(lambda x: x[0] * x[1])
    df['is_realtime'] = df.median_time_per_frame < df.allowable_time_per_frame


