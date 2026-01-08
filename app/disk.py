from pathlib import Path
import pandas as pd
import sys

def get_disk_path():
    if getattr(sys, 'frozen', False):
        path = Path(sys.executable).resolve().parent
    else:
        path =Path(__file__).resolve().parent 
    return path

def csv_to_disk(data, file_name="output.csv"):
    """Save data csv file on disk"""
    df = pd.DataFrame(data)
    path = get_disk_path() / file_name 
    df.to_csv(path, index=False)

