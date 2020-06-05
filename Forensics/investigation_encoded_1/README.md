# investigation_encoded_1

## Problem

> We have recovered a binary and 1 file: image01. See what you can make of it. Its also found in /problems/investigation-encoded-1_4_eb9020306ac9fe150ac9b9ca32ee1cc6 on the shell server. NOTE: The flag is not in the normal picoCTF{XXX} format.

* [Program](./mystery)
* [Output (Image?)](./output)

## Solution

1. Running `file ouput` shows that it is not an image: `output: Non-ISO extended-ASCII text, with no line terminators`. `xxd -g 1 output`:

    ```
    00000000: 8e 8e ba 3b b8 ea 23 a8 a8 ba 3a 8e ee 38 ee a3  ...;..#...:..8..
    00000010: a8 eb 8a a3 ab 80                                ......
    ```

2. Running the `mystery` binary produces: `./flag.txt not found`. Lets create a fake flag: `echo picoCTF{fake_flag} > flag.txt`. Running the binary again produces: `Error, I don't know why I crashed`.
3. Decompile the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)):

    ```c++
    undefined8 main(void)

    {
    long lVar1;
    size_t sVar2;
    undefined4 local_18;
    int local_14;
    FILE *local_10;

    local_10 = fopen("flag.txt","r");
    if (local_10 == (FILE *)0x0) {
        fwrite("./flag.txt not found\n",1,0x15,stderr);
                        /* WARNING: Subroutine does not return */
        exit(1);
    }
    flag_size = 0;
    fseek(local_10,0,2);
    lVar1 = ftell(local_10);
    flag_size = (int)lVar1;
    fseek(local_10,0,0);
    if (0xfffe < flag_size) {
        fwrite("Error, file bigger that 65535\n",1,0x1e,stderr);
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
    fwrite("I\'m Done, check ./output\n",1,0x19,stderr);
    return 0;
    }
    ```

    It reads the flag, sets some global variables and calls `encode()`

4. `encode()` function decompiled:

    ```c++
    void encode(void)

    {
    char cVar1;
    int iVar2;
    int local_10;
    char local_9;

    while( true ) {
        if (flag_size <= *flag_index) {
        while (remain != 7) {
            save(0);
        }
        return;
        }
        cVar1 = isValid((ulong)(uint)(int)*(char *)(*flag_index + flag));
        if (cVar1 != '\x01') break;
        local_9 = lower();
        if (local_9 == ' ') {
        local_9 = '{';
        }
        local_10 = *(int *)(matrix + (long)((int)local_9 + -0x61) * 8 + 4);
        iVar2 = local_10 + *(int *)(matrix + (long)((int)local_9 + -0x61) * 8);
        while (local_10 < iVar2) {
        getValue();
        save();
        local_10 = local_10 + 1;
        }
        *flag_index = *flag_index + 1;
    }
    fwrite("Error, I don\'t know why I crashed\n",1,0x22,stderr);
                        /* WARNING: Subroutine does not return */
    exit(1);
    }
    ```

    `encode()` iterates through the flag character by character, and (assuming the character is valid) converts it to lowercase. Then, it reads two values from a mysterious global matrix variable. The first value looks like a starting index, and the second value looks like a length from the starting index. For `end-start` iterations, it reads a value from `getValue()` and calls `save()` with that value.

    After all the characters in the flag were processed (after `*flag_index`, which is the looping variable, is equal to or greater than `flag_size`), the function calls `save(0)` for a number of times and returns.

    Explanation of the `*`s: The phrase `numbers[1]` can also be expressed as `*(numbers + 1)`, where the `*` operator is said to dereference the pointer address `numbers + 1`. dereference can be thought of in this case as read the value pointed to by. ([source](https://stackoverflow.com/a/36265395))

5. `isValid()` function decompiled:

    ```c++
    undefined8 isValid(char param_1)

    {
    undefined8 uVar1;

    if ((param_1 < 'a') || ('z' < param_1)) {
        if ((param_1 < 'A') || ('Z' < param_1)) {
        if (param_1 == ' ') {
            uVar1 = 1;
        }
        else {
            uVar1 = 0;
        }
        }
        else {
        uVar1 = 1;
        }
    }
    else {
        uVar1 = 1;
    }
    return uVar1;
    }
    ```

    Valid characters are uppercase and lowercase letters, and space. The first run with the fake flag did not work because `echo` creates a newline character, which is not accepted. Lets try without the newline: `echo -n picoCTF{fakeflag} > flag.txt` (also no underscore). The output is shorter than the input and I cannot manually decode the cipher.

6. `getValue()` decompiled:

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

    This function performs some bit-manipulation on the input using the `secret` global variable and returns a `0` or `1` (because of bitwise AND (`& 1`) at the end of the return statement).

7. `save()` decompiled (value from `getValue()` goes to `save()` in `main()`):

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

    This function creates a buffer in the `buffChar` global variable and writes to the `output` file once enough bits have come in to form a byte. The bitwise OR operation and multiplication by `'\x02'` effectively append the incoming bit to the buffer. For example if the bit `1` is the first bit inputted (so `buffChar` is 0) then `buffChar` is set to 1 and multiplied by 2, making it `10` in binary. Next, a `1` is inputted, so the bitwise OR between `10` and `1` is calculated to give `11`, which is then multiplied by 2 (decimal, 10 binary) to get `110`.

    This section of `encode()` now makes sense:

    ```c++
    if (flag_size <= *flag_index) {
    while (remain != 7) {
        save(0);
    }
    return;
    }
    ```

    Since `remain` is global, both `encode()` and `save()` know about it. However many bytes are required to get to the next bit are appended as 0 (hence the `save(0)`). This ensures that the output is padded to the nearest byte and can be flushed correctly.

8. Get `matrix` and `secret` using `radare2`:

    ```
    [0x000007c0]> bf obj.secret
    [0x000007c0]> pc @ obj.secret
    #define _BUFFER_SIZE 37
    const uint8_t buffer[_BUFFER_SIZE] = {
    0xb8, 0xea, 0x8e, 0xba, 0x3a, 0x88, 0xae, 0x8e, 0xe8, 0xaa,
    0x28, 0xbb, 0xb8, 0xeb, 0x8b, 0xa8, 0xee, 0x3a, 0x3b, 0xb8,
    0xbb, 0xa3, 0xba, 0xe2, 0xe8, 0xa8, 0xe2, 0xb8, 0xab, 0x8b,
    0xb8, 0xea, 0xe3, 0xae, 0xe3, 0xba, 0x80
    };
    [0x000007c0]> bf obj.matrix
    [0x000007c0]> pcw @ obj.matrix
    #define _BUFFER_SIZE 54
    const uint32_t buffer[_BUFFER_SIZE] = {
    0x00000008U, 0x00000000U, 0x0000000cU, 0x00000008U, 0x0000000eU,
    0x00000014U, 0x0000000aU, 0x00000022U, 0x00000004U, 0x0000002cU,
    0x0000000cU, 0x00000030U, 0x0000000cU, 0x0000003cU, 0x0000000aU,
    0x00000048U, 0x00000006U, 0x00000052U, 0x00000010U, 0x00000058U,
    0x0000000cU, 0x00000068U, 0x0000000cU, 0x00000074U, 0x0000000aU,
    0x00000080U, 0x00000008U, 0x0000008aU, 0x0000000eU, 0x00000092U,
    0x0000000eU, 0x000000a0U, 0x00000010U, 0x000000aeU, 0x0000000aU,
    0x000000beU, 0x00000008U, 0x000000c8U, 0x00000006U, 0x000000d0U,
    0x0000000aU, 0x000000d6U, 0x0000000cU, 0x000000e0U, 0x0000000cU,
    0x000000ecU, 0x0000000eU, 0x000000f8U, 0x00000010U, 0x00000106U,
    0x0000000eU, 0x00000116U, 0x00000004U, 0x00000124U
    };
    [0x000007c0]> pc @ obj.matrix
    #define _BUFFER_SIZE 216
    const uint8_t buffer[_BUFFER_SIZE] = {
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00,
    0x14, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x22, 0x00,
    0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x2c, 0x00, 0x00, 0x00,
    0x0c, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0x3c, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
    0x48, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x52, 0x00,
    0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x58, 0x00, 0x00, 0x00,
    0x0c, 0x00, 0x00, 0x00, 0x68, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0x74, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
    0x80, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x8a, 0x00,
    0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x92, 0x00, 0x00, 0x00,
    0x0e, 0x00, 0x00, 0x00, 0xa0, 0x00, 0x00, 0x00, 0x10, 0x00,
    0x00, 0x00, 0xae, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
    0xbe, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0xc8, 0x00,
    0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0xd0, 0x00, 0x00, 0x00,
    0x0a, 0x00, 0x00, 0x00, 0xd6, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00,
    0xec, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0xf8, 0x00,
    0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x06, 0x01, 0x00, 0x00,
    0x0e, 0x00, 0x00, 0x00, 0x16, 0x01, 0x00, 0x00, 0x04, 0x00,
    0x00, 0x00, 0x24, 0x01, 0x00, 0x00
    };
    ```

    The [`U` suffix](https://stackoverflow.com/a/4380700) means unsigned (no bit for negative or positive).

9. Find the sequences that correspond with each letter using the [decode.py](decode.py) script:

    ```
    a: 10111000
    b: 111010101000
    c: 11101011101000
    d: 1110101000
    e: 1000
    f: 101011101000
    g: 111011101000
    h: 1010101000
    i: 101000
    j: 1011101110111000
    k: 111010111000
    l: 101110101000
    m: 1110111000
    n: 11101000
    o: 11101110111000
    p: 10111011101000
    q: 1110111010111000
    r: 1011101000
    s: 10101000
    t: 111000
    u: 1010111000
    v: 101010111000
    w: 101110111000
    x: 11101010111000
    y: 1110101110111000
    z: 11101110101000
    Python dictionary: {'10111000': 'a', '111010101000': 'b', '11101011101000': 'c', '1110101000': 'd', '1000': 'e', '101011101000': 'f', '111011101000': 'g', '1010101000': 'h', '101000': 'i', '1011101110111000': 'j', '111010111000': 'k', '101110101000': 'l', '1110111000': 'm', '11101000': 'n', '11101110111000': 'o', '10111011101000': 'p', '1110111010111000': 'q', '1011101000': 'r', '10101000': 's', '111000': 't', '1010111000': 'u', '101010111000': 'v', '101110111000': 'w', '11101010111000': 'x', '1110101110111000': 'y', '11101110101000': 'z'}
    ```

    This script is a python version of the `getValue()` and `encode()` functions. The `encode()` function contains only the necessary components to encode each lower case letter of ascii and then print the calculated encoding.

    Additionally, this script uses a modified version of the `matrix` variable as shown below:

    ```python
    matrix = [
        0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00,
        0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00,
        0x14, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x22, 0x00,
        0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x2c, 0x00, 0x00, 0x00,
        0x0c, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x0c, 0x00,
        0x00, 0x00, 0x3c, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
        0x48, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x52, 0x00,
        0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x58, 0x00, 0x00, 0x00,
        0x0c, 0x00, 0x00, 0x00, 0x68, 0x00, 0x00, 0x00, 0x0c, 0x00,
        0x00, 0x00, 0x74, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
        0x80, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x8a, 0x00,
        0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x92, 0x00, 0x00, 0x00,
        0x0e, 0x00, 0x00, 0x00, 0xa0, 0x00, 0x00, 0x00, 0x10, 0x00,
        0x00, 0x00, 0xae, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
        0xbe, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0xc8, 0x00,
        0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0xd0, 0x00, 0x00, 0x00,
        0x0a, 0x00, 0x00, 0x00, 0xd6, 0x00, 0x00, 0x00, 0x0c, 0x00,
        0x00, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00,
        0xec, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0xf8, 0x00,
        0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x106, 0x00, 0x00, 0x00,
        0x0e, 0x00, 0x00, 0x00, 0x116, 0x00, 0x00, 0x00, 0x04, 0x00,
        0x00, 0x00, 0x124, 0x00, 0x00, 0x00
    ]
    ```

    As you can see, the differences are in the final three lines. In the original 1 byte representation of the original matrix all of the bytes are surrounded by `0x00` except for some in the last 3 rows. Without combining these bytes (bytes that are non-zero right next to each other like `0x06, 0x01`), the the letters "y" and "z" do not produce the correct values. When changing the values it is important to not remove a byte, instead just set it to `0x00`. Additionally, the bytes should be combined from right-to-left. So, for instance, `0x06, 0x01` becomes `0x0106` or just `0x106`.

    I'm not sure why the above is the case, but I believe it has to do with how [primitive data types](https://www.geeksforgeeks.org/c-data-types/) work in C++. I think that the `int` and `long` in the below lines force 4 bytes to be read.

    ```c++
    local_10 = *(int *)(matrix + (long)((int)local_9 + -0x61) * 8 + 4);
    iVar2 = local_10 + *(int *)(matrix + (long)((int)local_9 + -0x61) * 8);
    ```

    These 4 bytes are read in reverse because of little endian. In the `getValue()` function, the data is read using `byte` and `char`, which can both only hold one byte so only one byte is read from `matrix`. Python does not work the same way and will only return the value at a position in an array, nothing more.

10. Run [solve.py](solve.py) to get `Flag: encodedsrdotzdkhx`. This script has a copy of the dictionary converting encoded characters to ascii as produced by [decode.py](decode.py). It loops through the bits of the original `output` file, which contains the encoded flag. The hex representation can be obtained with `xxd -c1 output | cut -d" " -f2 | tr -d "\n"`. For each loop the script adds the current bit to a buffer and checks if that buffer can decode to an ascii character using the dictionary. If not, it adds another bit, if yes, the script adds that letter to the `flag_decoded` variable and clears the buffer.
11. Other write-ups: [AMACB](https://github.com/AMACB/picoCTF-2019-writeups/tree/master/problems/investigation_encoded_1) ([Archive](https://web.archive.org/web/20200604234256/https://github.com/AMACB/picoCTF-2019-writeups/tree/master/problems/investigation_encoded_1)) and [Dvd848](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/investigation_encoded_1.md) ([Archive](https://web.archive.org/web/20200604234305/https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/investigation_encoded_1.md))

### Flag

`encodedsrdotzdkhx`
