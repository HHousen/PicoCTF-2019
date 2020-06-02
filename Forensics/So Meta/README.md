# So Meta

## Problem

> Find the flag in this picture. You can also find the file in /problems/so-meta_3_6dc950904c3ee41f324ae8d9f142f2b8.

* [Image](pico_img.png)

## Solution

1. The flag is hidden in the EXIF data of the image. Use `exiftool` and `grep`:

    ```bash
    $ exiftool pico_img.png | grep Artist
    Artist                          : picoCTF{s0_m3ta_43f253bb}
    ```

2. [Katana](https://github.com/JohnHammond/katana) can solve this challenge:

    ```bash
    Target completed in 0.21 seconds after 1847 unit cases
    grep(/data/targets/pico_img.png) ➜ 
    picoCTF{s0_m3ta_43f253bb} - (copied)
    ```

### Flag

`picoCTF{s0_m3ta_43f253bb}`
