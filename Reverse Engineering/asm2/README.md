# asm2

## Problem

> What does asm2(0x9,0x1e) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. Source located in the directory at /problems/asm2_2_5667a5cd5764b4356121f1d6232ac78c.

* [Source](./test.S)

## Solution

1. Let's look at the source:

    ```assembly
    asm2:
        <+0>:	push   ebp
        <+1>:	mov    ebp,esp
        <+3>:	sub    esp,0x10
        <+6>:	mov    eax,DWORD PTR [ebp+0xc]
        <+9>:	mov    DWORD PTR [ebp-0x4],eax
        <+12>:	mov    eax,DWORD PTR [ebp+0x8]
        <+15>:	mov    DWORD PTR [ebp-0x8],eax
        <+18>:	jmp    0x50c <asm2+31>
        <+20>:	add    DWORD PTR [ebp-0x4],0x1
        <+24>:	add    DWORD PTR [ebp-0x8],0xa9
        <+31>:	cmp    DWORD PTR [ebp-0x8],0x47a6
        <+38>:	jle    0x501 <asm2+20>
        <+40>:	mov    eax,DWORD PTR [ebp-0x4]
        <+43>:	leave  
        <+44>:	ret
    ```

2. We call `asm2(0x9,0x1e)` so we are putting `0x9` and `0x1e` into the stack. After running `mov ebp,esp` the stack looks like this:

    ```
    +---------+
    | old ebp | <-- ebp
    +---------+
    | ret     | <-- ebp + 0x4
    +---------+
    | 0x9     | <-- ebp + 0x8
    +---------+
    | 0x1e    | <-- ebp + 0xc
    +---------+
    ```

3. Then we run `sub esp,0x10` which creates the below layout:

    ```
    +---------+
    |         | <-- ebp - 0x10 (local3)
    +---------+
    |         | <-- ebp - 0xc (local2)
    +---------+
    |         | <-- ebp - 0x8 (local1)
    +---------+
    |         | <-- ebp - 0x4 (local0)
    +---------+
    | old ebp | <-- ebp
    +---------+
    | ret     | <-- ebp + 0x4
    +---------+
    | 0x9     | <-- ebp + 0x8
    +---------+
    | 0x1e    | <-- ebp + 0xc
    +---------+
    ```

4. Next, we put our two parameters in at `ebp-0x4` and `ebp-0x8`:

    ```assembly
    <+6>:	mov    eax,DWORD PTR [ebp+0xc]
    <+9>:	mov    DWORD PTR [ebp-0x4],eax
    <+12>:	mov    eax,DWORD PTR [ebp+0x8]
    <+15>:	mov    DWORD PTR [ebp-0x8],eax
    <+18>:	jmp    0x50c <asm2+31>
    ```

    Two new positions at `ebp-0x4` and `ebp-0x8` are created and store the values from `ebp+0xc` and `ebp+0x8`.

    This makes the stack look as follows:

    ```
    +---------+
    |         | <-- ebp - 0x10 (local3)
    +---------+
    |         | <-- ebp - 0xc (local2)
    +---------+
    | 0x9     | <-- ebp - 0x8 (local1)
    +---------+
    | 0x1e    | <-- ebp - 0x4 (local0)
    +---------+
    | old ebp | <-- ebp
    +---------+
    | ret     | <-- ebp + 0x4
    +---------+
    | 0x9     | <-- ebp + 0x8
    +---------+
    | 0x1e    | <-- ebp + 0xc
    +---------+
    ```

5. At this point, we know that `ebp-0x4` is storing `0x1e` and `ebp-0x8` is storing `0x9`. We then take an unconditional jump to line 31.
6. We see here that we are comparing the value stored at `ebp-0x8`, which is `0x9`, to `0x47a6`. Since the comparison is less or equal to and the condition is jle (jump less/equal), we make the jump back up to line 20.

    ```assembly
    <+31>:	cmp    DWORD PTR [ebp-0x8],0x47a6
    <+38>:	jle    0x501 <asm2+20>
    ```

7. At this point we can start to see a for loop type of logic occurring. After jumping to line 20, the value stored at `ebp-0x4` increases by `0x1` and the value at `ebp-0x8` increases by `0xa9`. This continues to loop because of the jle condition until `ebp-0x8` is not less or equal to `0x47a6`. Finally, once the loop ends, we move the value stored at `ebp-0x4` to the returned value eax. Therefore, the value at `ebp-0x4` is all that matters in determining the flag, but we do need to worry about `ebp-0x8` since it determines how many times to loop. So we take `0x1e` and add `0x1` x times, where x can be found by solving `0x9+0xa9*x>0x47a6` to get 109. `0x1e+0x1*109` is `0x8b`, which is the flag.

    ```assembly
    <+20>:	add    DWORD PTR [ebp-0x4],0x1
    <+24>:	add    DWORD PTR [ebp-0x8],0xa9
    <+31>:	cmp    DWORD PTR [ebp-0x8],0x47a6
    <+38>:	jle    0x501 <asm2+20>
    <+40>:	mov    eax,DWORD PTR [ebp-0x4]
    <+43>:	leave  
    <+44>:	ret
    ```

### Flag

`0x8b`
