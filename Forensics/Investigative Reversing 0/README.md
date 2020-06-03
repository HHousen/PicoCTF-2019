# Investigative Reversing 0

## Problem

> We have recovered a binary and an image. See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-0_4_950a47cfcfc9b661c36603148c77df3d on the shell server.

* [Binary](./mystery)
* [Image](./mystery.png)

## Solution

1. Run `file mystery` which shows its is a ELF executable: `mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld`...
2. Reverse the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). Open it and in the symbol tree click on main. The decompiled main function will show on the right.

    ```c++
    void main(void)

    {
    FILE *flag_stream;
    FILE *image_steam;
    size_t sVar1;
    long in_FS_OFFSET;
    int i;
    int local_50;
    char local_38 [4];
    char local_34;
    char local_33;
    char local_29;
    long local_10;

    local_10 = *(long *)(in_FS_OFFSET + 0x28);
    flag_stream = fopen("flag.txt","r");
    image_steam = fopen("mystery.png","a");
    if (flag_stream == (FILE *)0x0) {
        puts("No flag found, please make sure this is run on the server");
    }
    if (image_steam == (FILE *)0x0) {
        puts("mystery.png is missing, please run this on the server");
    }
    sVar1 = fread(local_38,0x1a,1,flag_stream);
    if ((int)sVar1 < 1) {
                        /* WARNING: Subroutine does not return */
        exit(0);
    }
    puts("at insert");
    fputc((int)local_38[0],image_steam);
    fputc((int)local_38[1],image_steam);
    fputc((int)local_38[2],image_steam);
    fputc((int)local_38[3],image_steam);
    fputc((int)local_34,image_steam);
    fputc((int)local_33,image_steam);
    i = 6;
    while (i < 0xf) {
        fputc((int)(char)(local_38[i] + '\x05'),image_steam);
        i = i + 1;
    }
    fputc((int)(char)(local_29 + -3),image_steam);
    local_50 = 0x10;
    while (local_50 < 0x1a) {
        fputc((int)local_38[local_50],image_steam);
        local_50 = local_50 + 1;
    }
    fclose(image_steam);
    fclose(flag_stream);
    if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                        /* WARNING: Subroutine does not return */
        __stack_chk_fail();
    }
    return;
    }
    ```

3. We can see that the program opens the flag file, and places an encoded version of it at the end of the image file.

    ```
    $ xxd -g 1 mystery.png | tail
    0001e7f0: 82 20 08 82 20 08 82 20 08 82 20 64 1f 32 12 21  . .. .. .. d.2.!
    0001e800: 08 82 20 08 82 20 08 82 20 08 42 f6 21 23 11 82  .. .. .. .B.!#..
    0001e810: 20 08 82 20 08 82 20 08 82 20 64 1f 32 12 21 08   .. .. .. d.2.!.
    0001e820: 82 20 08 82 20 08 82 20 08 42 f6 21 23 11 82 20  . .. .. .B.!#.. 
    0001e830: 08 82 20 08 82 20 08 82 20 64 1f 32 12 21 08 82  .. .. .. d.2.!..
    0001e840: 20 08 82 20 08 82 20 08 42 f6 21 23 11 82 20 08   .. .. .B.!#.. .
    0001e850: 82 20 08 82 20 08 82 20 64 17 ff ef ff fd 7f 5e  . .. .. d......^
    0001e860: ed 5a 9d 38 d0 1f 56 00 00 00 00 49 45 4e 44 ae  .Z.8..V....IEND.
    0001e870: 42 60 82 70 69 63 6f 43 54 4b 80 6b 35 7a 73 69  B`.picoCTK.k5zsi
    0001e880: 64 36 71 5f 35 32 36 36 61 38 35 37 7d           d6q_5266a857}
    ```

4. The encoding works as follows:

    1. Add bytes 0 to 5 (inclusive) to the image.
    2. Loop through the bytes of the flag from 6 to `0xf` (from 6 to 14, inclusive) and add `'\x05'` (5) to each bytes.
    3. Add the 15th byte minus 3 (probably the 15th byte, I am assuming based on the code structure).
    4. Loop through and add the remaining bytes (16 to 25, inclusive).

5. We can reverse this using the [script.py](script.py) and get the flag.

### Flag

`picoCTF{f0und_1t_5266a857}`
