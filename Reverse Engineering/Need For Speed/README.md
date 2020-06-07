# Challenge Name

## Problem

> The name of the game is speed. Are you quick enough to solve this problem and keep it above 50 mph? need-for-speed.

* [Program](./need-for-speed)

## Solution

1. Run the program `chmod +x need-for-speed && ./need-for-speed:

    ```
    Keep this thing over 50 mph!
    ============================

    Creating key...
    Not fast enough. BOOM!
    ```

2. Run the program in GDB and ignore SIGALRM messages:

    ```
    $ gdb ./need-for-speed
    (gdb) handle SIGALRM ignore
    Signal        Stop      Print   Pass to program Description
    SIGALRM       No        No      No              Alarm clock
    (gdb) r
    Starting program: ~/Documents/PicoCTF/Reverse Engineering/Need For Speed/need-for-speed 
    Keep this thing over 50 mph!
    ============================

    Creating key...
    Finished
    Printing flag:
    PICOCTF{Good job keeping bus #3b89d39c speeding along!}
    [Inferior 1 (process 66066) exited normally]
    ```

    More Info: [StackOverflow](https://stackoverflow.com/questions/26145952/gdb-sigalrm-alarm-clock-termination)

3. Alternative Method 1: Run in GDB and skip the `set_timer()` function:

    ```
    (gdb) break set_timer
    Breakpoint 1 at 0x883
    (gdb) r
    Starting program: ~/Documents/PicoCTF/Reverse Engineering/Need For Speed/need-for-speed
    Keep this thing over 50 mph!
    ============================


    Breakpoint 1, 0x0000555555554883 in set_timer ()
    (gdb) return
    Make selected stack frame return now? (y or n) y
    #0  0x0000555555554997 in main ()
    (gdb) step
    Single stepping until exit from function main,
    which has no line number information.
    Creating key...
    Finished
    Printing flag:
    PICOCTF{Good job keeping bus #3b89d39c speeding along!}
    __libc_start_main (main=0x555555554974 <main>, argc=1, argv=0x7fffffffdb58, init=<optimized out>, fini=<optimized out>, 
        rtld_fini=<optimized out>, stack_end=0x7fffffffdb48) at ../csu/libc-start.c:342
    342     ../csu/libc-start.c: No such file or directory.
    ```

    * [GDB Skip Command StackOverflow](https://stackoverflow.com/questions/1133365/preventing-gdb-from-stepping-into-a-function-or-file)
    * [GDB Continuing and Skipping Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb/Continuing-and-Stepping.html)
    * [GDB Skipping Over Functions and Files Documentation](https://sourceware.org/gdb/onlinedocs/gdb/Skipping-Over-Functions-and-Files.html)

4. Alternative Method 2: Only calling the needed functions:

    ```
    (gdb) break main
    Breakpoint 1 at 0x978
    (gdb) r
    Starting program: ~/Documents/PicoCTF/Reverse Engineering/Need For Speed/need-for-speed

    Breakpoint 1, 0x0000555555554978 in main ()
    (gdb) call (int) get_key()
    Creating key...
    Finished
    $1 = 9
    (gdb) call (int) print_flag()
    Printing flag:
    PICOCTF{Good job keeping bus #3b89d39c speeding along!}
    $3 = 56
    ```

    * [GDB Function Calling Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb/Calling.html)
    * [GDB Variables Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb/Variables.html)

5. Alternative Method 3: Bypass the long loop:

    ```
    (gdb) break main
    Breakpoint 1 at 0x978
    (gdb) r
    Starting program: ~/Documents/PicoCTF/Reverse Engineering/Need For Speed/need-for-speed

    Breakpoint 1, 0x0000555555554978 in main ()
    (gdb) call (int) decrypt_flag(0xe99d7887)
    $1 = 55
    (gdb) call (int) print_flag()
    Printing flag:
    PICOBTD{Eold$jkb%kceviig(b}s)#9b29o35c,s}ekdgnh qlnv!o
    $2 = 56
    (gdb) call (int) print_flag()
    Printing flag:
    PICOCTF{Good job keeping bus #3b89d39c speeding along!}
    $3 = 56
    ```

    The `key` value can be found with Ghidra.

6. The significant functions as decompiled by Ghidra can be found in [ghidra.c](ghidra.c)

### Flag

`PICOCTF{Good job keeping bus #3b89d39c speeding along!}`
