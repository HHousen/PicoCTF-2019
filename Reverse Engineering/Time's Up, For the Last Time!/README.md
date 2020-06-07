# Time's Up, For the Last Time!

## Problem

> You've solved things fast. You've solved things faster! Now do the impossible. times-up-one-last-time, located in the directory at /problems/time-s-up--for-the-last-time-_5_b2df97b433878873b16cff47337769d6.

* [Program](./times-up-one-last-time)

## Solution

1. Running the program and inputting a newline character (`\n`) with bash is not fast enough.

    Running previous challenges in this way produced `Solution? Nope!`:

    ```
    $ ./times-up <<< '\n'
    Challenge: (((((657265146) + (-1923909696)) + ((1986179264) + (-812103564))) + (((-1027939860) + (1392242872)) + ((-110733888) + (-310598076)))) + ((((((720637104) + (-2047273348)) - (708133016)) - (-890325910)) - ((443949727) - (1909030317))) + (((-301107515) - (551799480)) - ((1489532366) + (1475102980)))))
    Setting alarm...
    Solution? Nope!
    ```

    However, this challenge does not even register the input since the alarm triggers so fast:

    ```
    $ ./times-up-one-last-time <<< '\n'
    Challenge: (((((-1012045115) - (1810430134)) % ((2010494120) + (-1086432160))) - (((-403630830) % (596322993)) ^ ((-1348370583) * (2088348720)))) | ((((1271304372) + (1954174030)) x ((-376311670) o (-407368940))) & (((-1044627813) - (1022249799)) | ((-1080733304) | (1758513321)))))
    Setting alarm...
    Alarm clock
    ```

2. The time for the alarm to trigger is now 10 microseconds (10 uSections). It is unlikely that any script will solve this if we can't even get any input into the program. Decompile the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). `main()` function (Ghidra was not able to determine names):

    ```c++
    undefined8 FUN_00100eae(void)

    {
    FUN_00100ad0();
    printf("Challenge: ");
    FUN_00100e96();
    putchar(10);
    fflush(stdout);
    puts("Setting alarm...");
    fflush(stdout);
    ualarm(10,0);
    printf("Solution? ");
    __isoc99_scanf(&DAT_001011b8,&DAT_00304770);
    if (DAT_00304770 == DAT_00304778) {
        puts("Congrats! Here is the flag!");
        system("/bin/cat flag.txt");
    }
    else {
        puts("Nope!");
    }
    return 0;
    }
    ```

3. There are also weird new operators. Going into the source code we find the function that appears to solve the expression generated (comments are ascii conversions added by me):

    ```c++
    ulong FUN_00100ca2(undefined param_1,ulong param_2,ulong param_3)

    {
    switch(param_1) {
    case 0x25: // %
        if (param_3 != 0) {
        param_2 = (long)param_2 % param_3;
        }
        break;
    case 0x26: // &
        param_2 = param_2 & param_3;
        break;
    default:
                        /* WARNING: Subroutine does not return */
        exit(1);
    case 0x2a: // *
        param_2 = param_2 * param_3;
        break;
    case 0x2b: // +
        param_2 = param_3 + param_2;
        break;
    case 0x2d: // -
        param_2 = param_2 - param_3;
        break;
    case 0x2f: // /
        if (param_3 != 0) {
        param_2 = (long)param_2 / (long)param_3;
        }
        break;
    case 0x5e: // ^
        param_2 = param_2 ^ param_3;
        break;
    case 0x66: // f
        break;
    case 0x6f: // o
        param_2 = param_3;
        break;
    case 0x72: // r
        param_2 = param_3;
        break;
    case 0x74: // t
        break;
    case 0x78: // x
        param_2 = param_3;
        break;
    case 0x7c: // |
        param_2 = param_2 | param_3;
    }
    return param_2;
    }
    ```

    We can reverse this functionality and implement it into our script later.

4. We should try blocking the `SIGALRM`. However, this cannot be done using a debugger (`GDB`) like was possible in "Need For Speed" since we need the elevated permissions from SETUID to be able to `cat` the `flag.txt` file. The [zardus/preeny](https://github.com/zardus/preeny) project will not work here for the same reason, but it could be useful for future projects.
5. We can open a session with the challenge file in which the `SIGALRM` is ignored with the following C program:

    ```c++
    #include <stdio.h>
    #include <stdlib.h>
    #include <signal.h>

    int main() {
        signal(SIGALRM, SIG_IGN);
        system("/problems/time-s-up--for-the-last-time-_5_b2df97b433878873b16cff47337769d6/times-up-one-last-time");
    }
    ```

    The above file runs the challenge using the absolute path on the shell server. Create a file called `no_sigalrm.c` in your home directory. Compile it with: `gcc -g no_sigalrm.c -o no_sigalrm` (output name is important since the [script.py](script.py) is hardcoded to use that name). Make sure to mark it as executable with `chmod +x no_sigalrm`.

    Above script as a file (calls the `times-up-one-last-time` in the present directory): [no_sigalrm.c](no_sigalrm.c) (compiled version: [no_sigalrm](no_sigalrm))

6. Let's write a script to solve the equation, now that we have bypassed the time restriction. Searching for "custom python operators" yields [this hack for infix operators](https://code.activestate.com/recipes/384122/) linked to from [this blog](http://tomerfiliba.com/blog/Infix-Operators/) and [this StackOverflow answer](https://stackoverflow.com/a/932580).
7. We actually only have two custom operators: return the left value and return the right value, there are just many names for these operators in the produced equation.

    ```
    L = Infix(lambda x,y: x)
    R = Infix(lambda x,y: y)
    ```

    We replace the operators in the program output with our new operators:

    ```
    challenge = challenge.replace("f", "|L|")
    challenge = challenge.replace("o", "|R|")
    challenge = challenge.replace("r", "|R|")
    challenge = challenge.replace("t", "|L|")
    challenge = challenge.replace("x", "|R|")
    ```

8. The [script.py](script.py) only works in `python2` since the infix operator hack only works properly in that version. Make sure to change the script location directory to your home folder. You should compile the `no_sigalrm` file on the shell server and place it in your home folder. Then, in [script.py](script.py) change the text `<username>` to your username.
9. Run exploit: `python2 script.py USER=<username> PASSWORD=<password>`:

    ```
    [+] Connecting to 2019shell1.picoctf.com on port 22: Done
    [*] <username>@2019shell1.picoctf.com:
        Distro    Ubuntu 18.04
        OS:       linux
        Arch:     amd64
        Version:  4.15.0
        ASLR:     Enabled
    [+] Opening new channel: 'pwd': Done
    [+] Receiving all data: Done (14B)
    [*] Closed SSH channel with 2019shell1.picoctf.com
    [*] Working directory: '/tmp/tmp.Ss2j8QPOBM'
    [+] Opening new channel: 'ln -s /home/<username>/* .': Done
    [+] Receiving all data: Done (0B)
    [*] Closed SSH channel with 2019shell1.picoctf.com
    [+] Starting remote process '/home/<username>/no_sigalrm' on 2019shell1.picoctf.com: pid 1091939
    Answer: -2606491616
    [+] picoCTF{And now you can hack time! #0e9c1f05}
    ```

    Warning: The script might fail, but it has approximately a 3/4 success rate.

### Flag

`picoCTF{And now you can hack time! #0e9c1f05}`
