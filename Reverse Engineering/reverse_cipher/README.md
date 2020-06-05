# reverse_cipher

## Problem

> We have recovered a binary and a text file. Can you reverse the flag. Its also found in /problems/reverse-cipher_0_b784b7d0e499d532eba7269bfdf6a21d on the shell server.

* [Binary](./vuln)
* [Text file](./vuln.c)

## Solution

1. `cat rev_this` shows `picoCTF{w1{1wq87g_9654g}`.
2. Decompile the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)):

    ```c++
    void main(void)

    {
    size_t sVar1;
    char local_58 [23];
    char local_41;
    int local_2c;
    FILE *local_28;
    FILE *local_20;
    uint local_14;
    int local_10;
    char local_9;

    local_20 = fopen("flag.txt","r");
    local_28 = fopen("rev_this","a");
    if (local_20 == (FILE *)0x0) {
        puts("No flag found, please make sure this is run on the server");
    }
    if (local_28 == (FILE *)0x0) {
        puts("please run this on the server");
    }
    sVar1 = fread(local_58,0x18,1,local_20);
    local_2c = (int)sVar1;
    if ((int)sVar1 < 1) {
                        /* WARNING: Subroutine does not return */
        exit(0);
    }
    local_10 = 0;
    while (local_10 < 8) {
        local_9 = local_58[local_10];
        fputc((int)local_9,local_28);
        local_10 = local_10 + 1;
    }
    local_14 = 8;
    while ((int)local_14 < 0x17) {
        if ((local_14 & 1) == 0) {
        local_9 = local_58[(int)local_14] + '\x05';
        }
        else {
        local_9 = local_58[(int)local_14] + -2;
        }
        fputc((int)local_9,local_28);
        local_14 = local_14 + 1;
    }
    local_9 = local_41;
    fputc((int)local_41,local_28);
    fclose(local_28);
    fclose(local_20);
    return;
    }
    ```

    This is just a simple script that performs a few shifts on the characters of the flag. Characters 0-7 are left as is. Characters 8-22 alternate between adding 5 and subtracting 2, starting with adding 5. `local_14 & 1` does a bitwise AND between the current iteration number and 1. The if statement checks if this equals `0`. It will equal `0` every other iteration because `& 1` checks if the last bit is 0 or 1 and returns 1 if the last bit is 1, and otherwise returns 0. Finally, the last character (the 23rd one) is added on to the file as is.

3. Run the [script.py](script.py) to reverse this logic and get the flag.

### Flag

`picoCTF{r3v3rs39ba4806b}`
