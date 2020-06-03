# Investigative Reversing 1

## Problem

> We have recovered a binary and a few images: image, image2, image3. See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-1_4_266adcde17fa2ab2ec454e6c5379ad81 on the shell server.

* [Binary](./mystery)
* [Image 1](./mystery.png)
* [Image 2](./mystery2.png)
* [Image 3](./mystery3.png)

## Solution

1. Run `file mystery` which shows its is a ELF executable: `mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld`...
2. Reverse the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). Open it and in the symbol tree click on main. The decompiled main function will show on the right.

    ```c++
    void main(void)

    {
    FILE *__stream;
    FILE *__stream_00;
    FILE *__stream_01;
    FILE *__stream_02;
    long in_FS_OFFSET;
    char local_6b;
    int local_68;
    int local_64;
    int local_60;
    char local_38 [4];
    char local_34;
    char local_33;
    long local_10;
    
    local_10 = *(long *)(in_FS_OFFSET + 0x28);
    __stream = fopen("flag.txt","r");
    __stream_00 = fopen("mystery.png","a");
    __stream_01 = fopen("mystery2.png","a");
    __stream_02 = fopen("mystery3.png","a");
    if (__stream == (FILE *)0x0) {
        puts("No flag found, please make sure this is run on the server");
    }
    if (__stream_00 == (FILE *)0x0) {
        puts("mystery.png is missing, please run this on the server");
    }
    fread(local_38,0x1a,1,__stream);
    fputc((int)local_38[1],__stream_02);
    fputc((int)(char)(local_38[0] + '\x15'),__stream_01);
    fputc((int)local_38[2],__stream_02);
    local_6b = local_38[3];
    fputc((int)local_33,__stream_02);
    fputc((int)local_34,__stream_00);
    local_68 = 6;
    while (local_68 < 10) {
        local_6b = local_6b + '\x01';
        fputc((int)local_38[local_68],__stream_00);
        local_68 = local_68 + 1;
    }
    fputc((int)local_6b,__stream_01);
    local_64 = 10;
    while (local_64 < 0xf) {
        fputc((int)local_38[local_64],__stream_02);
        local_64 = local_64 + 1;
    }
    local_60 = 0xf;
    while (local_60 < 0x1a) {
        fputc((int)local_38[local_60],__stream_00);
        local_60 = local_60 + 1;
    }
    fclose(__stream_00);
    fclose(__stream);
    if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                        /* WARNING: Subroutine does not return */
        __stack_chk_fail();
    }
    return;
    }
    ```

3. We can see that the program opens the flag file, and scatters an encoded version of it across the three image files.

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
    0001e870: 42 60 82 43 46 7b 41 6e 31 5f 38 35 35 36 31 31  B`.CF{An1_855611
    0001e880: 64 33 7d                                         d3}
    $ xxd -g 1 mystery2.png | tail
    0001e7e0: 21 08 82 20 08 82 20 08 82 20 08 42 f6 21 23 11  !.. .. .. .B.!#.
    0001e7f0: 82 20 08 82 20 08 82 20 08 82 20 64 1f 32 12 21  . .. .. .. d.2.!
    0001e800: 08 82 20 08 82 20 08 82 20 08 42 f6 21 23 11 82  .. .. .. .B.!#..
    0001e810: 20 08 82 20 08 82 20 08 82 20 64 1f 32 12 21 08   .. .. .. d.2.!.
    0001e820: 82 20 08 82 20 08 82 20 08 42 f6 21 23 11 82 20  . .. .. .B.!#.. 
    0001e830: 08 82 20 08 82 20 08 82 20 64 1f 32 12 21 08 82  .. .. .. d.2.!..
    0001e840: 20 08 82 20 08 82 20 08 42 f6 21 23 11 82 20 08   .. .. .B.!#.. .
    0001e850: 82 20 08 82 20 08 82 20 64 17 ff ef ff fd 7f 5e  . .. .. d......^
    0001e860: ed 5a 9d 38 d0 1f 56 00 00 00 00 49 45 4e 44 ae  .Z.8..V....IEND.
    0001e870: 42 60 82 85 73                                   B`..s
    $ xxd -g 1 mystery3.png | tail
    0001e7e0: 21 08 82 20 08 82 20 08 82 20 08 42 f6 21 23 11  !.. .. .. .B.!#.
    0001e7f0: 82 20 08 82 20 08 82 20 08 82 20 64 1f 32 12 21  . .. .. .. d.2.!
    0001e800: 08 82 20 08 82 20 08 82 20 08 42 f6 21 23 11 82  .. .. .. .B.!#..
    0001e810: 20 08 82 20 08 82 20 08 82 20 64 1f 32 12 21 08   .. .. .. d.2.!.
    0001e820: 82 20 08 82 20 08 82 20 08 42 f6 21 23 11 82 20  . .. .. .B.!#.. 
    0001e830: 08 82 20 08 82 20 08 82 20 64 1f 32 12 21 08 82  .. .. .. d.2.!..
    0001e840: 20 08 82 20 08 82 20 08 42 f6 21 23 11 82 20 08   .. .. .B.!#.. .
    0001e850: 82 20 08 82 20 08 82 20 64 17 ff ef ff fd 7f 5e  . .. .. d......^
    0001e860: ed 5a 9d 38 d0 1f 56 00 00 00 00 49 45 4e 44 ae  .Z.8..V....IEND.
    0001e870: 42 60 82 69 63 54 30 74 68 61 5f                 B`.icT0tha_
    ```

4. The encoding works as follows:

    1. Append byte 1 to file 3
    2. Add `0x15` to byte 0 and append to file 2
    3. Append byte 2 to file 3
    4. Append byte 5 to file 3. At the top of the file the variables are listed like so:

        ```c++
        char local_38 [4]; // 4 is length
        char local_34;
        char local_33;
        ```

        This means that `local_34` will contain the 4th character from flag and `local_33` will contain the 5th. So in the below lines the 5th bytes is added then the 4th.

        ```c++
        fputc((int)local_33,__stream_02);
        fputc((int)local_34,__stream_00);
        ```

    5. Append byte 4 to file 1
    6. Append bytes 6 to 9 (inclusive) to file 1
    7. Append byte 3 (which has been increased by 4 during the above loop) to file 2
    8. Append bytes 10 to 14 (inclusive) to file 3
    9. Append bytes 15 to 25 (inclusive) to file 1

5. We need to copy the last 16 bytes from file 1, 2 from file 2, and 8 from file 3 to variable `data_1`, `data_2`, `data_3` in the [script.py](script.py), which reverses the scheme explained above.
6. We can reverse this using the [script.py](script.py) and get the flag.

### Flag

`picoCTF{An0tha_1_855611d3}`
