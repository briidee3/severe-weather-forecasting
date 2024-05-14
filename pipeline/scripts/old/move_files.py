# Moving files to finish off compiling image dataset
# Move any files in any dir in current dir to current dir (del old dirs once done.)
# A very basic and rudimentary script, made for a specific use case (not for robustness)
# BD 8-1-23

import os
import subprocess

def move_cur_dir():
    # get list of files in cur dir
    base_dir = os.listdir(".")
    # go thru dirs and move files
    for n in base_dir:
        # if is dir, get files out and del dir
        if os.path.isdir(n):
            sub_dir = "./" + n
            # get files from sub_dir, move to base_dir
            ls_sub_dir = os.listdir(sub_dir)
            for x in ls_sub_dir:
                subprocess.run(["mv", sub_dir + "/" + x, "./"])


# run in base directory (i.e. MPL-organized)
for subdir in os.listdir("."):
    if 'move_files.py' not in subdir:
        os.chdir(os.path.join("./", subdir))
        move_cur_dir()
        os.chdir("../")
