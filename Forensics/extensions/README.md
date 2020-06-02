# extensions

## Problem

> This is a really weird text file TXT? Can you find the flag?

* [TXT File](./flag.txt)

## Solution

1. A quick file type check with `file` reveals that we have a PNG file instead of a TXT file:

    ```bash
    file flag.txt
    flag.txt: PNG image data, 1697 x 608, 8-bit/color RGB, non-interlaced
    ```

2. Change the filename to flag.png and get the flag:

    ![Image with flag](flag.png)

3. [Katana](https://github.com/JohnHammond/katana) can solve this challenge:

    ```bash
    Target completed in 7.29 seconds after 6105 unit cases
    tesseract(/data/targets/flag.txt) ➜
    picoCTF{now_you_know_about_extensions} - (copied)
    ```

### Flag

`picoCTF{now_you_know_about_extensions}`
