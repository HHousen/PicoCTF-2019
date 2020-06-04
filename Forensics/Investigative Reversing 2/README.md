# Investigative Reversing 2

## Problem

> We have recovered a binary and an image See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-2_6_2ea0f420e29d29b575882f681dc272d5 on the shell server.

* [Binary](./mystery)
* [Image](./encoded.bmp)

## Solution

1. Run `file mystery` which shows its is a ELF executable: `mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld`...
2. Reverse the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). Open it and in the symbol tree click on main. The decompiled main function will show on the right.

    ```c++
    undefined8 main(void)

    {
    size_t sVar1;
    long in_FS_OFFSET;
    char local_7e;
    char local_7d;
    int local_7c;
    int local_78;
    int local_74;
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
        puts("original.bmp is missing, please run this on the server");
    }
    sVar1 = fread(&local_7e,1,1,local_58);
    local_7c = (int)sVar1;
    local_68 = 2000;
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
        puts("flag is not 50 chars");
                        /* WARNING: Subroutine does not return */
        exit(0);
    }
    local_74 = 0;
    while (local_74 < 0x32) {
        local_70 = 0;
        while ((int)local_70 < 8) {
        local_7d = codedChar((ulong)local_70,(ulong)(uint)(int)(char)(local_48[local_74] + -5),
                            (ulong)(uint)(int)local_7e,
                            (ulong)(uint)(int)(char)(local_48[local_74] + -5));
        fputc((int)local_7d,local_50);
        fread(&local_7e,1,1,local_58);
        local_70 = local_70 + 1;
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


    ulong codedChar(int param_1,byte param_2,byte param_3)

    {
    byte local_20;

    local_20 = param_2;
    if (param_1 != 0) {
        local_20 = (byte)((int)(char)param_2 >> ((byte)param_1 & 0x1f));
    }
    return (ulong)(param_3 & 0xfe | local_20 & 1);
    }
    ```

3. This time the program jumps to offset 2000, and hides a 50 character flag using [LSB](https://en.wikipedia.org/wiki/Bit_numbering#Least_significant_bit) encoding. More info on [BoiteAKlou's Infosec Blog](https://www.boiteaklou.fr/Steganography-Least-Significant-Bit.html) ([Archive](https://web.archive.org/web/20200603202609/https://www.boiteaklou.fr/Steganography-Least-Significant-Bit.html)). The error string `"flag is not 50 chars"` reveals that the flag is 50 characters long.

4. We can see that up to offset 2000 (`0x7d0`) we have a constant value of `0xe8`. Then, for `50 * 8` bytes we have different values (switching between `0xe9` and `0xe8`), and finally, at offset `0x960` we're back to `0xe8`. `0xe8` in binary is `0b11101000` and `0xe9` is `0b11101001`. In binary you can easily see the "least significant bit" modification that was made. Output of `xxd -g 1 -s $((2000 - 32)) -l $((50*8 + 64)) encoded.bmp`:

    ```bash
    000007b0: e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8  ................
    000007c0: e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8  ................
    000007d0: e9 e9 e8 e9 e8 e9 e9 e8 e8 e8 e9 e8 e8 e9 e9 e8  ................
    000007e0: e8 e9 e9 e9 e9 e8 e9 e8 e8 e9 e8 e9 e8 e9 e9 e8  ................
    000007f0: e8 e9 e9 e9 e9 e9 e8 e8 e9 e9 e9 e9 e8 e8 e9 e8  ................
    00000800: e9 e8 4e 4e 4e 4e 4f e8 e8 e9 e9 e8 e9 e9 e9 e8  ..NNNNO.........
    00000810: e9 e8 e8 e9 e8 e9 e9 e8 e8 e9 e9 e9 e8 e9 e8 e8  ................
    00000820: e9 e9 e8 e8 e9 e9 e9 e8 e9 e9 e9 e9 e8 e9 e9 e8  ................
    00000830: e8 e9 e8 e9 e9 e8 e9 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    00000840: e9 e8 e8 e9 e8 e9 e9 e8 e8 e9 e9 e9 e8 e9 e8 e8  ................
    00000850: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    00000860: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    00000870: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    00000880: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    00000890: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    000008a0: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    000008b0: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    000008c0: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    000008d0: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    000008e0: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    000008f0: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    00000900: e9 e9 e8 e9 e8 e9 e8 e8 e9 e9 e8 e9 e8 e9 e8 e8  ................
    00000910: e9 e9 e8 e9 e8 e9 e8 e8 e9 e8 e8 e8 e9 e9 e8 e8  ................
    00000920: e8 e9 e9 e9 e9 e8 e9 e8 e8 e9 e8 e8 e9 e9 e8 e8  ................
    00000930: e8 e9 e9 e9 e8 e9 e8 e8 e9 e8 e9 e9 e8 e9 e8 e8  ................
    00000940: e8 e9 e9 e9 e9 e8 e9 e8 e8 e8 e8 e8 e8 e9 e9 e8  ................
    00000950: e8 e8 e8 e8 e8 e9 e9 e8 e8 e8 e8 e9 e9 e9 e9 e8  ................
    00000960: e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8  ................
    00000970: e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8  ................
    ```

5. Run the [script.py](script.py) to select the last bits from offset 2000 bytes to 2000+50*8 bytes and then convert them to ascii. View the code for the low-levels details about how the code works (60% of the file is purely comments).

### Flag

`picoCTF{n3xt_0n300000000000000000000000006c732cee}`
