import os

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)