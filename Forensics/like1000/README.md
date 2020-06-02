# like1000

## Problem

> This .tar file got tarred alot. Also available at /problems/like1000_0_369bbdba2af17750ddf10cc415672f1c.

* [TAR File](./1000.tar)

## Solution

1. Extracting the `1000.tar` file reveals `999.tar` and `filler.txt`. Extracting the `999.tar` file reveals `998.tar` and `filler.txt`.
2. Run the [script.py](script.py) to extract the files in a loop. This script uses the `tarfile` python module as described in [this article](https://www.tutorialspoint.com/How-are-files-extracted-from-a-tar-file-using-Python) and removes the `filler.txt` file after each extraction.
3. We obtain the `flag.png` nested in `1000.tar` file which has the flag: ![Flag image](flag.png)

### Flag

`picoCTF{l0t5_0f_TAR5}`
