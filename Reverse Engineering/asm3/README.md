# asm3

## Problem

> What does asm3(0xc4bd37e3,0xf516e15e,0xeea4f333) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. Source located in the directory at /problems/asm3_4_c89016e12b8f3cac92a2e637c03f6139.

* [Source](./test.S)

## Solution

1. Let's look at the source:

    ```assembly
    asm3:
        <+0>:	push   ebp
        <+1>:	mov    ebp,esp
        <+3>:	xor    eax,eax
        <+5>:	mov    ah,BYTE PTR [ebp+0x9]
        <+8>:	shl    ax,0x10
        <+12>:	sub    al,BYTE PTR [ebp+0xd]
        <+15>:	add    ah,BYTE PTR [ebp+0xe]
        <+18>:	xor    ax,WORD PTR [ebp+0x10]
        <+22>:	nop
        <+23>:	pop    ebp
        <+24>:	ret
    ```

2. Since this challenge is more complicated than the previous `asm*` challenges, we will compile and run it.
3. We will modify [test.S](test.S) to [test_modified.S](test_modified.S) like so:

    ```assembly
    .intel_syntax noprefix
    .global asm3

    asm3:
        push   ebp
        mov    ebp,esp
        xor    eax,eax
        mov    ah,BYTE PTR [ebp+0x9]
        shl    ax,0x10
        sub    al,BYTE PTR [ebp+0xd]
        add    ah,BYTE PTR [ebp+0xe]
        xor    ax,WORD PTR [ebp+0x10]
        nop
        pop    ebp
        ret
    ```

4. We also create a [solve.c](solve.c) script:

    ```c++
    #include <stdio.h>

    int asm3(int, int, int);

    int main(int argc, char* argv[])
    {
        printf("0x%x\n", asm3(0xc4bd37e3,0xf516e15e,0xeea4f333));
        return 0;
    }
    ```

5. Compile:

    ```
    $ gcc -masm=intel -m32 -c test_modified.S -o test_modified.o
    $ gcc -m32 -c solve.c -o solve.o
    $ gcc -m32 test_modified.o solve.o -o solve
    ```

6. Run `./solve` to get flag.

### Flag

`0xe52c`
