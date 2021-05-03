
import os
import glob

DATA_INPUT_PATH = 'data'
DATA_ORIGINAL_AERIALS_PATH = os.path.join('data', 'aerial')
DATA_OUTPUT_PATH = os.path.join('data', 'out')

COLORS = ['blue','purple','green','orange','red','black']

def filter_by_extension(path, extension):
    extension = '*.' + extension

    q = os.path.join(path,extension)

    return glob.glob(q)