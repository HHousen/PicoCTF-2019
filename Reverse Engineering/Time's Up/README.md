# Time's Up

## Problem

> Time waits for no one. Can you solve this before time runs out? times-up, located in the directory at /problems/time-s-up_1_7d4f79c3df3e1b044801573eea5722be.

* [Program](./times-up)

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
    ualarm(5000,0);
    printf("Solution? ");
    __isoc99_scanf(&DAT_00100e68,&guess);
    if (guess == result) {
        puts("Congrats! Here is the flag!");
        system("/bin/cat flag.txt");
    }
    else {
        puts("Nope!");
    }
    return 0;
    }
    ```

    Using the debugger, like we did for `Need For Speed` will not work because we will lose the SETUID permissions required for the system call: `system("/bin/cat flag.txt");`.

    This code also shows us that there is an alarm which ends the program if we don't provide a valid answer within 5000 uSeconds, which is not a lot of time.

2. Let's try running the program: `chmod +x times-up && ./times-up`

    ```
    Challenge: (((((2033553839) + (-1699577110)) + (((-545013997) - (67704704)) + ((-1918353553) + (-1516567616)))) + (((-210308874) + (1475601456)) + ((1775129956) + (-2055247704)))) + ((((1330215250) - (-1021292908)) + ((-1623051128) + (-1560439740))) + ((((-748207565) + (215421591)) + (1002169210)) + ((-1314247138) + (1641760225)))))
    Setting alarm...
    Solution? Alarm clock
    ```

3. Running the [script.py](script.py) will not work since it communicates over SSH, which is not fast enough to solve this challenge.
4. Instead, run the following (which is commented at the end of [script.py](script.py)) on the shell server in `/problems/time-s-up_1_7d4f79c3df3e1b044801573eea5722be`:

    ```python
    from pwn import *
    io = process("./times-up")
    io.recvuntil("Challenge: ")
    challenge = io.recvline()
    answer = eval(challenge)
    io.sendline(str(answer))
    io.interactive()
    ```

    ```
    Solution? Congrats! Here is the flag!
    picoCTF{Gotta go fast. Gotta go FAST. #3daa579a}
    ```

### Flag

`picoCTF{Gotta go fast. Gotta go FAST. #3daa579a}`
