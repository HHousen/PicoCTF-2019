import os
import tarfile
# pip install tqdm
from tqdm import tqdm

for i in tqdm(range(1000, 0, -1), desc="Extracting"):
    current_file = str(i) + '.tar'
    next_file = str(i-1) + '.tar'

    my_tar = tarfile.open(current_file)
    my_tar.extractall()
    my_tar.close()
    os.remove(current_file)
    os.remove("filler.txt")

