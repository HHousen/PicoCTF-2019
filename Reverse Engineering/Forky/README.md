# Forky

## Problem

> In this program, identify the last integer value that is passed as parameter to the function doNothing(). The binary is also found in /problems/forky_5_4f100885e708548a54f8c5668f9821c1 on the shell server.

* [Program](./vuln)

## Solution

1. Reverse the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). `main()` function:

    ```c++
    /* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

    undefined4 main(void)

    {
    int *piVar1;

    piVar1 = (int *)mmap((void *)0x0,4,3,0x21,-1,0);
    *piVar1 = 1000000000;
    fork();
    fork();
    fork();
    fork();
    *piVar1 = *piVar1 + 0x499602d2;
    doNothing(*piVar1);
    return 0;
    }
    ```

    `doNothing()` function:

    ```c++
    void doNothing(void)

    {
    __x86.get_pc_thunk.ax();
    return;
    }

    ```

2. So this program recursively forks itself and calls `doNothing()`. We need to identify last integer value that is passed as parameter to `doNothing()`.
3. The first process forks itself, creating 2 child processes. Those two children fork, creating 4 child processes. We have now executed 2 of the 4 calls to `fork()`. We fork the 4 children, doubling again to create 8 child processes. Now we only have 1 call to `fork()` left. We fork the 8 children, resulting in 16 child processes. More info about `fork()` on [GeeksforGeeks](https://www.geeksforgeeks.org/fork-system-call/). The diagram below shows this happening (each `0` is a process):

    ```
    +
    |
    +-----------------------------------+
    |                                   |
    +-----------------+                 +-----------------+
    |                 |                 |                 |
    +--------+        +--------+        +--------+        +--------+
    |        |        |        |        |        |        |        |
    +---+    +---+    +---+    +---+    +---+    +---+    +---+    +---+  
    |   |    |   |    |   |    |   |    |   |    |   |    |   |    |   |  
    O   O    O   O    O   O    O   O    O   O    O   O    O   O    O   O  
    ```

4. Therefore, all we need to do is calculate `1000000000 + (16 * 0x499602d2)`. The program creates 16 processes, each of which adds `0x499602d2` to the initial value `1000000000`.
5. Run the calculation using python: `python -c "from numpy import int32;print(int32(1000000000) + int32(16)*int32(0x499602d2))"` to get `-721750240`. Here, we use the numpy.int32 datatype (generic unsigned integer) since it overflows just like in C. More info on [this blog post from Loïc Pefferkorn](https://loicpefferkorn.net/2013/09/python-force-c-integer-overflow-behavior/) ([Archive](https://web.archive.org/web/20200612220223/https://loicpefferkorn.net/2013/09/python-force-c-integer-overflow-behavior/)) and [this StackOverflow answer](https://stackoverflow.com/a/16745427) ([Archive](https://web.archive.org/web/20200612220238/https://stackoverflow.com/questions/16745387/python-32-bit-and-64-bit-integer-math-with-intentional-overflow/16745427)).
6. Another way to use python to compute the answer is to use `ctypes`:

    ```python
    import ctypes
    ctypes.c_int32(0x3B9ACA00 + 16*0x499602D2)
    c_int(-721750240)
    ```

### Flag

`picoCTF{-721750240}`
