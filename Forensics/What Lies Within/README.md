# What Lies Within

## Problem

> Theres something in the building. Can you retrieve the flag?

* [Image](buildings.png)

## Solution

1. This is a challenge where [the flag is hidden in the least significant bit of each pixel value](https://www.boiteaklou.fr/Steganography-Least-Significant-Bit.html).
2. The flag can be extracted with zsteg:

    ```bash
    zsteg buildings.png 
    b1,r,lsb,xy         .. text: "^5>R5YZrG"
    b1,rgb,lsb,xy       .. text: "picoCTF{h1d1ng_1n_th3_b1t5}"
    b1,abgr,msb,xy      .. file: PGP Secret Sub-key -
    b2,b,lsb,xy         .. text: "XuH}p#8Iy="
    b3,abgr,msb,xy      .. text: "t@Wp-_tH_v\r"
    b4,r,lsb,xy         .. text: "fdD\"\"\"\" "
    b4,r,msb,xy         .. text: "%Q#gpSv0c05"
    b4,g,lsb,xy         .. text: "fDfffDD\"\""
    b4,g,msb,xy         .. text: "f\"fff\"\"DD"
    b4,b,lsb,xy         .. text: "\"$BDDDDf"
    b4,b,msb,xy         .. text: "wwBDDDfUU53w"
    b4,rgb,msb,xy       .. text: "dUcv%F#A`"
    b4,bgr,msb,xy       .. text: " V\"c7Ga4"
    b4,abgr,msb,xy      .. text: "gOC_$_@o"
    ```

3. Visit [HackTricks](https://book.hacktricks.xyz/stego/stego-tricks) for more information. Steghide is used for JPG images and Zsteg is used for PNGs.
4. [Katana](https://github.com/JohnHammond/katana) can solve this challenge:

    ```bash
    Target completed in 2.57 seconds after 14215 unit cases
    zsteg(/data/targets/buildings.png) ➜
    picoCTF{h1d1ng_1n_th3_b1t5} - (copied)
    ```

### Flag

`picoCTF{h1d1ng_1n_th3_b1t5}`
