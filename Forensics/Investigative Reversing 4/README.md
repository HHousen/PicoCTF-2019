# Investigative Reversing 4

## Problem

> We have recovered a binary and 5 images: image01, image02, image03, image04, image05. See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-4_6_f5c1435d5f45ad042614888d32091beb on the shell server.

* [Binary](./mystery)
* [Image 1](./Item01_cp.bmp)
* [Image 2](./Item02_cp.bmp)
* [Image 3](./Item03_cp.bmp)
* [Image 4](./Item04_cp.bmp)
* [Image 5](./Item05_cp.bmp)

## Solution

1. Reverse the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). Open it and in the symbol tree click on main. The decompiled main function will show on the right.

    ```c++
    undefined8 main(void)

    {
    size_t sVar1;
    undefined4 local_4c;
    undefined local_48 [52];
    int local_14;
    FILE *local_10;
    
    flag = local_48;
    local_4c = 0;
    flag_index = &local_4c;
    local_10 = fopen("flag.txt","r");
    if (local_10 == (FILE *)0x0) {
        puts("No flag found, please make sure this is run on the server");
    }
    sVar1 = fread(flag,0x32,1,local_10);
    local_14 = (int)sVar1;
    if (local_14 < 1) {
        puts("Invalid Flag");
                        /* WARNING: Subroutine does not return */
        exit(0);
    }
    fclose(local_10);
    encodeAll();
    return 0;
    }


    /* WARNING: Could not reconcile some variable overlaps */

    void encodeAll(void)

    {
    ulong local_48;
    undefined8 local_40;
    undefined4 local_38;
    ulong local_28;
    undefined8 local_20;
    undefined4 local_18;
    char local_9;
    
    local_28 = 0x635f31306d657449;
    local_20 = 0x706d622e70;
    local_18 = 0;
    local_48 = 0x622e31306d657449;
    local_40 = 0x706d;
    local_38 = 0;
    local_9 = '5';
    while ('0' < local_9) {
        local_48._0_6_ = CONCAT15(local_9,(undefined5)local_48);
        local_48 = local_48 & 0xffff000000000000 | (ulong)(uint6)local_48;
        local_28._0_6_ = CONCAT15(local_9,(undefined5)local_28);
        local_28 = local_28 & 0xffff000000000000 | (ulong)(uint6)local_28;
        encodeDataInFile(&local_48,&local_28,&local_28);
        local_9 = local_9 + -1;
    }
    return;
    }


    void encodeDataInFile(char *param_1,char *param_2)

    {
    size_t sVar1;
    char local_2e;
    char local_2d;
    int local_2c;
    FILE *local_28;
    FILE *local_20;
    uint local_18;
    int local_14;
    int local_10;
    int local_c;
    
    local_20 = fopen(param_1,"r");
    local_28 = fopen(param_2,"a");
    if (local_20 != (FILE *)0x0) {
        sVar1 = fread(&local_2e,1,1,local_20);
        local_c = (int)sVar1;
        local_2c = 0x7e3;
        local_10 = 0;
        while (local_10 < local_2c) {
        fputc((int)local_2e,local_28);
        sVar1 = fread(&local_2e,1,1,local_20);
        local_c = (int)sVar1;
        local_10 = local_10 + 1;
        }
        local_14 = 0;
        while (local_14 < 0x32) {
        if (local_14 % 5 == 0) {
            local_18 = 0;
            while ((int)local_18 < 8) {
            local_2d = codedChar((ulong)local_18,(ulong)(uint)(int)*(char *)(*flag_index + flag),
                                (ulong)(uint)(int)local_2e,
                                (ulong)(uint)(int)*(char *)(*flag_index + flag));
            fputc((int)local_2d,local_28);
            fread(&local_2e,1,1,local_20);
            local_18 = local_18 + 1;
            }
            *flag_index = *flag_index + 1;
        }
        else {
            fputc((int)local_2e,local_28);
            fread(&local_2e,1,1,local_20);
        }
        local_14 = local_14 + 1;
        }
        while (local_c == 1) {
        fputc((int)local_2e,local_28);
        sVar1 = fread(&local_2e,1,1,local_20);
        local_c = (int)sVar1;
        }
        fclose(local_28);
        fclose(local_20);
        return;
    }
    puts("No output found, please run this on the server");
                        /* WARNING: Subroutine does not return */
    exit(0);
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

2. This script spreads the flag amongst the five ".bmp" image files provided in the challenge. For each image the program:

    1. Jumps to offset 2019 bytes and encodes a byte of the flag using LSB in 8 bytes of the original image file.
    2. Skips 4 bytes by copying 4 bytes from the original image file

3. However, the above steps are made slightly more complicated in the actual encoding program. It performs a loop 50 times. If the interval tracking variable is divisible by 5, then it will loop through and write 8 bits of the flag. If the interval tracking variable is not divisible by 5, then the program writes writes a value from the original image. This effectively does the above steps.
4. Run the decoding [script.py](script.py) to get the flag.

### Flag

`picoCTF{N1c3_R3ver51ng_5k1115_000000000002eea28cd}`
