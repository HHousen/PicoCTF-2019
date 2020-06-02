# Glory of the Garden

## Problem

> This garden contains more than it seems. You can also find the file in /problems/glory-of-the-garden_3_346e50df4a37bcc4aa5f6e5831604e2a on the shell server.

* [Image](garden.jpg)

## Solution

1. Use `strings` and `grep`:

    ```bash
    $ strings garden.jpg | grep pico
    Here is a flag "picoCTF{more_than_m33ts_the_3y35a97d3bB}"
    ```

2. [Katana](https://github.com/JohnHammond/katana) can solve this challenge:

    ```bash
    Target completed in 2.29 seconds after 3844 unit cases
    strings(/data/targets/garden.jpg) ➜ 
    picoCTF{more_than_m33ts_the_3y35a97d3bB} - (copied)
    ```

### Flag

`picoCTF{more_than_m33ts_the_3y35a97d3bB}`
