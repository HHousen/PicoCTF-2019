# Investigative Reversing 3

## Problem

> We have recovered a binary and an image See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-3_1_8670aba71322d7b19d278027f10f2935 on the shell server.

* [Binary](./mystery)
* [Image](./encoded.bmp)

## Solution

1. Reverse the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). Open it and in the symbol tree click on main. The decompiled main function will show on the right.

    ```c++
    undefined8 main(void)

    {
    size_t sVar1;
    long in_FS_OFFSET;
    char local_7e;
    char local_7d;
    int local_7c;
    int local_78;
    uint local_74;
    uint local_70;
    undefined4 local_6c;
    int local_68;
    int local_64;
    FILE *local_60;
    FILE *local_58;
    FILE *local_50;
    char local_48 [56];
    long local_10;

    local_10 = *(long *)(in_FS_OFFSET + 0x28);
    local_6c = 0;
    local_60 = fopen("flag.txt","r");
    local_58 = fopen("original.bmp","r");
    local_50 = fopen("encoded.bmp","a");
    if (local_60 == (FILE *)0x0) {
        puts("No flag found, please make sure this is run on the server");
    }
    if (local_58 == (FILE *)0x0) {
        puts("No output found, please run this on the server");
    }
    sVar1 = fread(&local_7e,1,1,local_58);
    local_7c = (int)sVar1;
    local_68 = 0x2d3;
    local_78 = 0;
    while (local_78 < local_68) {
        fputc((int)local_7e,local_50);
        sVar1 = fread(&local_7e,1,1,local_58);
        local_7c = (int)sVar1;
        local_78 = local_78 + 1;
    }
    sVar1 = fread(local_48,0x32,1,local_60);
    local_64 = (int)sVar1;
    if (local_64 < 1) {
        puts("Invalid Flag");
                        /* WARNING: Subroutine does not return */
        exit(0);
    }
    local_74 = 0;
    while ((int)local_74 < 100) {
        if ((local_74 & 1) == 0) {
        local_70 = 0;
        while ((int)local_70 < 8) {
            local_7d = codedChar((ulong)local_70,(ulong)(uint)(int)local_48[(int)local_74 / 2],
                                (ulong)(uint)(int)local_7e,
                                (ulong)(uint)(int)local_48[(int)local_74 / 2]);
            fputc((int)local_7d,local_50);
            fread(&local_7e,1,1,local_58);
            local_70 = local_70 + 1;
        }
        }
        else {
        fputc((int)local_7e,local_50);
        fread(&local_7e,1,1,local_58);
        }
        local_74 = local_74 + 1;
    }
    while (local_7c == 1) {
        fputc((int)local_7e,local_50);
        sVar1 = fread(&local_7e,1,1,local_58);
        local_7c = (int)sVar1;
    }
    fclose(local_50);
    fclose(local_58);
    fclose(local_60);
    if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
        return 0;
    }
                        /* WARNING: Subroutine does not return */
    __stack_chk_fail();
    }
    ```

2. The flag is encoded using LSB encoding, similarly to the previous challenge. However, this time the encoding starts from offset `0x2d3` and every 9 bytes the image is left as-is. In essence, 8 bits of payload are encoded in the LSB of 8 bytes of the image, and then one byte of the original image is placed as-is.
3. The encoding script accomplishes the above by looping the following 100 times:

    * If `(local_74 & 1) == 0` (if the last bit of the current iteration index is 0; this effectively switches back and forth between the if and else clauses for each iteration):
        * Loop 8 times (write 8 bites (1 byte) of the flag to 9 bytes of the image):
            * Write a bit of the flag to the current byte in the image. The divided by 2 in `local_48[(int)local_74 / 2]` is necessary because every other iteration of the outer 100 times loop leaves a bit of the regular image alone. Since, the looping variable is twice the required value, it is divided by 
    * Else (every other loop):
        * Write a bit of the original image

4. The above is reflected in the reversal [script.py](script.py).
5. Run the [script.py](script.py) and get the flag.

### Flag

`picoCTF{4n0th3r_L5b_pr0bl3m_0000000000000dbd98691}`
