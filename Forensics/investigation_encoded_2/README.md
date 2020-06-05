# investigation_encoded_2

## Problem

> We have recovered a binary and 1 file: image01. See what you can make of it. Its also found in /problems/investigation-encoded-2_6_74ebdbfd3962c221df51c8ce5141b275 on the shell server. NOTE: The flag is not in the normal picoCTF{XXX} format.

* [Program](./mystery)
* [Output (Image?)](./output)

## Solution

1. Running the binary produces: `Error: file ./flag.txt not found`
2. Lets create a flag with `echo picoctf > flag.txt` and try running again which just causes a `Segmentation fault`
3. Decompile the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)):

    ```c++
    undefined8 main(void)

    {
    long lVar1;
    size_t sVar2;
    undefined4 local_18;
    int local_14;
    FILE *local_10;

    badChars = '\0';
    local_10 = fopen("flag.txt","r");
    if (local_10 == (FILE *)0x0) {
        fwrite("Error: file ./flag.txt not found\n",1,0x21,stderr);
                        /* WARNING: Subroutine does not return */
        exit(1);
    }
    flag_size = 0;
    fseek(local_10,0,2);
    lVar1 = ftell(local_10);
    flag_size = (int)lVar1;
    fseek(local_10,0,0);
    login();
    if (0xfffe < flag_size) {
        fwrite("Error, file bigger than 65535\n",1,0x1e,stderr);
                        /* WARNING: Subroutine does not return */
        exit(1);
    }
    flag = malloc((long)flag_size);
    sVar2 = fread(flag,1,(long)flag_size,local_10);
    local_14 = (int)sVar2;
    if (local_14 < 1) {
                        /* WARNING: Subroutine does not return */
        exit(0);
    }
    local_18 = 0;
    flag_index = &local_18;
    output = fopen("output","w");
    buffChar = 0;
    remain = 7;
    fclose(local_10);
    encode();
    fclose(output);
    if (badChars == '\x01') {
        fwrite("Invalid Characters in flag.txt\n./output is corrupted\n",1,0x35,stderr);
    }
    else {
        fwrite("I\'m Done, check file ./output\n",1,0x1e,stderr);
    }
    return 0;
    }
    ```

4. `encode()` function decompiled:

    ```c++
    void encode(void)

    {
    byte bVar1;
    int iVar2;
    int local_10;
    char local_9;

    while (*flag_index < flag_size) {
        local_9 = lower((ulong)(uint)(int)*(char *)(*flag_index + flag));
        if (local_9 == ' ') {
        local_9 = -0x7b;
        }
        else {
        if (('/' < local_9) && (local_9 < ':')) {
            local_9 = local_9 + 'K';
        }
        }
        local_9 = local_9 + -0x61;
        if ((local_9 < '\0') || ('$' < local_9)) {
        badChars = 1;
        }
        if (local_9 != '$') {
        iVar2 = ((int)local_9 + 0x12) % 0x24;
        bVar1 = (byte)(iVar2 >> 0x1f);
        local_9 = ((byte)iVar2 ^ bVar1) - bVar1;
        }
        local_10 = *(int *)(indexTable + (long)(int)local_9 * 4);
        iVar2 = *(int *)(indexTable + (long)((int)local_9 + 1) * 4);
        while (local_10 < iVar2) {
        getValue();
        save();
        local_10 = local_10 + 1;
        }
        *flag_index = *flag_index + 1;
    }
    while (remain != 7) {
        save(0);
    }
    return;
    }
    ```

5. `getValue()` function decompiled:

    ```c++
    ulong getValue(int param_1)

    {
    byte bVar1;
    int iVar2;

    iVar2 = param_1;
    if (param_1 < 0) {
        iVar2 = param_1 + 7;
    }
    bVar1 = (byte)(param_1 >> 0x37);
    return (ulong)((int)(uint)(byte)secret[iVar2 >> 3] >>
                    (7 - (((char)param_1 + (bVar1 >> 5) & 7) - (bVar1 >> 5)) & 0x1f) & 1);
    }
    ```

6. `save()` function decompiled:

    ```c++
    void save(byte param_1)

    {
    buffChar = buffChar | param_1;
    if (remain == 0) {
        remain = 7;
        fputc((int)(char)buffChar,output);
        buffChar = '\0';
    }
    else {
        buffChar = buffChar * '\x02';
        remain = remain + -1;
    }
    return;
    }
    ```

7. Differences from previous challenge, `investigation_encoded_1`:
    * The `matrix` array was replaced with `indexTable`
    * The digits 0-9 (inclusive) are valid for input (the flag can include numbers now). The while loop through the flag adds `K` (75) if the current character is between '\' and '$', which are the ascii values for the digits 0-9. Adding `K` is important because `a` (97) is subtracted from each character, regardless whether its a number or not. 48 is the ascii value for 0. Adding 75 yields 123 and subtracting the 97 gives 26. This means that from 0-25 are the letters a-z and then starting at 26 are the numbers 0-9. Since 97 is always subtracted, only a-z, `{`, `|`, `}`, `~`, and any exceptions (0-9 and space) are accepted. However, the characters `{`, `|`, `}`, `~` would get the same encoding as `0`, `1`, `2`, and `3`, so they can be ignored.
    * The program performs some kind of manipulation on the characters before using them as array indices:

        ```c++
        iVar2 = ((int)local_9 + 0x12) % 0x24;
        bVar1 = (byte)(iVar2 >> 0x1f);
        local_9 = ((byte)iVar2 ^ bVar1) - bVar1;
        ```

    * There is a `login` function which will crash the program (This was the cause of the `Segmentation fault` earlier). It can be skipped over during debugging.

8. Get `indexTable` and `secret` using `radare2`:

    ```
    [0x00000ae0]> bf obj.secret
    [0x00000ae0]> pc @ obj.secret
    #define _BUFFER_SIZE 71
    const uint8_t buffer[_BUFFER_SIZE] = {
    0x8b, 0xaa, 0x2e, 0xee, 0xe8, 0xbb, 0xae, 0x8e, 0xbb, 0xae,
    0x3a, 0xee, 0x8e, 0xee, 0xa8, 0xee, 0xae, 0xe3, 0xaa, 0xe3,
    0xae, 0xbb, 0x8b, 0xae, 0xb8, 0xea, 0xae, 0x2e, 0xba, 0x2e,
    0xae, 0x8a, 0xee, 0xa3, 0xab, 0xa3, 0xbb, 0xbb, 0x8b, 0xbb,
    0xb8, 0xae, 0xee, 0x2a, 0xee, 0x2e, 0x2a, 0xb8, 0xaa, 0x8e,
    0xaa, 0x3b, 0xaa, 0x3b, 0xba, 0x8e, 0xa8, 0xeb, 0xa3, 0xa8,
    0xaa, 0x28, 0xbb, 0xb8, 0xae, 0x2a, 0xe2, 0xee, 0x3a, 0xb8,
    0x00
    };
    [0x00000ae0]> bf obj.indexTable
    [0x00000ae0]> pcw @ obj.indexTable
    #define _BUFFER_SIZE 38
    const uint32_t buffer[_BUFFER_SIZE] = {
    0x00000000U, 0x00000004U, 0x00000012U, 0x00000028U, 0x0000003cU,
    0x00000052U, 0x00000064U, 0x00000078U, 0x0000008eU, 0x0000009eU,
    0x000000b4U, 0x000000c8U, 0x000000daU, 0x000000eaU, 0x000000fcU,
    0x0000010eU, 0x0000011eU, 0x00000134U, 0x00000148U, 0x0000015aU,
    0x0000016aU, 0x00000172U, 0x00000180U, 0x0000018cU, 0x0000019aU,
    0x000001aaU, 0x000001bcU, 0x000001c8U, 0x000001d6U, 0x000001e0U,
    0x000001eaU, 0x000001f0U, 0x00000200U, 0x0000020aU, 0x00000216U,
    0x00000222U, 0x00000230U, 0x00000234U
    };
    [0x00000ae0]> pc @ obj.indexTable
    #define _BUFFER_SIZE 152
    const uint8_t buffer[_BUFFER_SIZE] = {
    0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x12, 0x00,
    0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x3c, 0x00, 0x00, 0x00,
    0x52, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x78, 0x00,
    0x00, 0x00, 0x8e, 0x00, 0x00, 0x00, 0x9e, 0x00, 0x00, 0x00,
    0xb4, 0x00, 0x00, 0x00, 0xc8, 0x00, 0x00, 0x00, 0xda, 0x00,
    0x00, 0x00, 0xea, 0x00, 0x00, 0x00, 0xfc, 0x00, 0x00, 0x00,
    0x0e, 0x01, 0x00, 0x00, 0x1e, 0x01, 0x00, 0x00, 0x34, 0x01,
    0x00, 0x00, 0x48, 0x01, 0x00, 0x00, 0x5a, 0x01, 0x00, 0x00,
    0x6a, 0x01, 0x00, 0x00, 0x72, 0x01, 0x00, 0x00, 0x80, 0x01,
    0x00, 0x00, 0x8c, 0x01, 0x00, 0x00, 0x9a, 0x01, 0x00, 0x00,
    0xaa, 0x01, 0x00, 0x00, 0xbc, 0x01, 0x00, 0x00, 0xc8, 0x01,
    0x00, 0x00, 0xd6, 0x01, 0x00, 0x00, 0xe0, 0x01, 0x00, 0x00,
    0xea, 0x01, 0x00, 0x00, 0xf0, 0x01, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x0a, 0x02, 0x00, 0x00, 0x16, 0x02, 0x00, 0x00,
    0x22, 0x02, 0x00, 0x00, 0x30, 0x02, 0x00, 0x00, 0x34, 0x02,
    0x00, 0x00
    };
    ```

9. Find the sequences that correspond with each letter using the [decode.py](decode.py) script:

    ```
    a: 101011101110111000
    b: 1010101110111000
    c: 10111000
    d: 10101010111000
    e: 101010101000
    f: 11101010101000
    g: 1110111010101000
    h: 111011101110101000
    i: 111010101000
    j: 11101011101000
    k: 1110101000
    l: 1010101000
    m: 101000
    n: 1011101110111000
    o: 1010111000
    p: 101010111000
    q: 101110111000
    r: 11101010111000
    s: 1000
    t: 10111010101000
    u: 1011101110111011101000
    v: 10111011101011101000
    w: 1110101110111010111000
    x: 111010111011101000
    y: 11101110111010101000
    z: 1110111010101110111000
    0: 1110101010111000
    1: 1110101110101110111000
    2: 10111010111010111000
    3: 111010101010111000
    4: 1011101011101000
    5: 101110101011101000
    6: 101011101110101000
    7: 1110101011101000
    8: 1110111011101110111000
    9: 10111011101110111000
    Python dictionary: {'101011101110111000': 'a', '1010101110111000': 'b', '10111000': 'c', '10101010111000': 'd', '101010101000': 'e', '11101010101000': 'f', '1110111010101000': 'g', '111011101110101000': 'h', '111010101000': 'i', '11101011101000': 'j', '1110101000': 'k', '1010101000': 'l', '101000': 'm', '1011101110111000': 'n', '1010111000': 'o', '101010111000': 'p', '101110111000': 'q', '11101010111000': 'r', '1000': 's', '10111010101000': 't', '1011101110111011101000': 'u', '10111011101011101000': 'v', '1110101110111010111000': 'w', '111010111011101000': 'x', '11101110111010101000': 'y', '1110111010101110111000': 'z', '1110101010111000': '0', '1110101110101110111000': '1', '10111010111010111000': '2', '111010101010111000': '3', '1011101011101000': '4', '101110101011101000': '5', '101011101110101000': '6', '1110101011101000': '7', '1110111011101110111000': '8', '10111011101110111000': '9'}
    ```

    Unlike the previous script in `investigation_encoded_1`, this script makes use of the C word (4 byte) representation of the `matrix`/`indexTable` variable instead of the 1 byte representation. To handle this, the `* 4` was removed from `index` and `end`. The `* 4` effectively selected every 4th value, so removing that and only keeping every 4th value is an alternative way to solve this challenge instead of manually updating the 1 byte representation of `indexTable` as was done in the previous challenge.

10. Run [solve.py](solve.py) to get `Flag: t1m3f1i3500000000000098a9a51`. The [solve.py](solve.py) script is the exact same as in `investigation_encoded_1`, except the `decoded_dict` and `flag_encoded` were replaced.

### Flag

`t1m3f1i3500000000000098a9a51`
