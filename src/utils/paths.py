from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def project_path(*args):
    return PROJECT_ROOT.joinpath(*args)