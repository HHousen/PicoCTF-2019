# Time's Up, Again!

## Problem

> Previously you solved things fast. Now you've got to go faster. Much faster. Can you solve *this one* before time runs out? times-up-again, located in the directory at /problems/time-s-up--again-_1_014490a2cb518921928db099702cbfd9.

* [Program](./times-up-again)

## Solution

1. Decompile the binary file using [Ghidra](https://ghidra-sre.org/) ([cheat sheet](https://ghidra-sre.org/CheatSheet.html)). `main()` function:

    ```c++
    undefined8 main(void)

    {
    init_randomness();
    printf("Challenge: ");
    generate_challenge();
    putchar(10);
    fflush(stdout);
    puts("Setting alarm...");
    fflush(stdout);
    ualarm(200,0);
    printf("Solution? ");
    __isoc99_scanf(&DAT_00100efb,&guess);
    if (guess == result) {
        puts("Congrats! Here is the flag.txt!");
        system("/bin/cat flag.txt");
    }
    else {
        puts("Nope!");
    }
    return 0;
    }
    ```

    We cannot use the same script as in the previous challenge, `Time's Up`, because we only have 200 uSeconds. `pwntools` is too slow.

2. We will use `SIGSTOP` and `SIGCONT` to pause to resume the program before the timer can expire. Wikipedia description of `SIGSTOP` and `SIGCONT`: "When SIGSTOP is sent to a process, the usual behaviour is to pause that process in its current state. The process will only resume execution if it is sent the SIGCONT signal. SIGSTOP and SIGCONT are used for job control in the Unix shell, among other purposes. SIGSTOP cannot be caught or ignored."
3. The [script.py](script.py) works by:

    1. Running [times-up-again](times-up-again)
    2. Waiting for...
        * the moment right before the alarm is about to go off (which would trigger the `SIGALRM` signal and end the program)
        * the moment after the problem has been printed
    3. Pausing the program with the `SIGSTOP` signal
    4. Solving the mathematical equation given by the program using `eval()`
    5. Sending the answer and a newline
    6. Flushing the `stdin` and resuming the program by sending the `SIGCONT` signal
    7. Waiting 0.2 seconds for the program to output success or failure.
    8. Checking 4 lines of output for the word "pico". If it is found, the line is printed and the program ends. If "pico" does not appear, restart from step 1.

4. I tweaked the sleep amount and settled on `0.000175` seconds since it works well most of the time. 
5. I attempted to use the threading.Timer class, as discussed in this [StackOverflow answer](https://stackoverflow.com/a/10012262), in order to handle the rare cases that make the [script.py](script.py) appear to hang. However, using it caused delays and messed with the exact timing needed to run this script.
6. The original program was likely written in a language that does not implicitly support arbitrary-percision integers (`python` does). Also, the binary is only 64-bit: `times-up-again: ELF 64-bit LSB shared object` (output from `file times-up-again`). Thus, any integer we want to pass into the program we should turn back into 64-bit. This can be done with `%pow(2,64)` or `%(1 << 64)`. Other write-ups used `ctypes.c_longlong` instead of these techniques, but I could not get this to work.
7. `SIGSTOP` cannot be caught, which means the process doesn't even know it ever received the signal.
8. Run the [script.py](script.py). If it hangs for more than a second, kill it with `^C` and rerun. It will work eventually. Example output below (only two tries!):

    ```
    $ python script.py 
    Iteration #0
    Challenge:  (((((-1886135413) * (-687120364)) + ((294269581) * (1582871241))) - ((((-17798219) * (1585379416)) * (1261009084)) * ((-43416399) + (1227394943)))) - ((((-1868099744) * (388792763)) + ((-761322635) * (-1904639340))) + (((423915198) + (938350835)) + ((898339908) + (-1468634992)))))

    Answer: 42128093804841937203064357319295560
    Iteration #1
    Challenge:  (((((-1198557986) * (-1647142996)) + ((-1134528065) * (-441174539))) - ((((-1094944300) * (-239912724)) * (-770189614)) * ((230930317) + (638786821)))) - ((((910186477) * (-660748696)) + ((-1457806516) * (-2113165691))) + (((-894967377) + (1288049451)) + ((-1413128335) + (-1784259912)))))

    Answer: 175962852982823941714121282654933100
    picoCTF{Hasten. Hurry. Ferrociously Speedy. #3b0e50c7}

    It took 2 tries to get the flag.
    ```

9. Other Write-ups: [C program by Dvd848](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/Times_Up_Again.md) ([Archive](https://web.archive.org/web/20200606231624/https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/Times_Up_Again.md)) and [Python script that runs fast enough by AMACB](https://github.com/AMACB/picoCTF-2019-writeups/tree/master/problems/times-up-again) ([Archive](https://web.archive.org/web/20200606231633/https://github.com/AMACB/picoCTF-2019-writeups/tree/master/problems/times-up-again))

### Flag

`picoCTF{Hasten. Hurry. Ferrociously Speedy. #3b0e50c7}`
