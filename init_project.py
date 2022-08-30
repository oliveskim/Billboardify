import os

def createDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

top50_dir = './data/raw/top50'
structured_dir = './data/structured'

createDir(top50_dir)
createDir(structured_dir)