# WhitePages

## Problem

> I stopped using YellowPages and moved onto WhitePages... but the page they gave me is all blank!

* [TXT File](./whitepages.txt)

## Solution

1. If we inspect the file using a HEX editor, we can see that there are two types of whitespaces:

    ```bash
    $ xxd whitepages.txt | head
    00000000: e280 83e2 8083 e280 83e2 8083 20e2 8083  ............ ...
    00000010: 20e2 8083 e280 83e2 8083 e280 83e2 8083   ...............
    00000020: 20e2 8083 e280 8320 e280 83e2 8083 e280   ...... ........
    00000030: 83e2 8083 20e2 8083 e280 8320 e280 8320  .... ...... ... 
    00000040: 2020 e280 83e2 8083 e280 83e2 8083 e280    ..............
    00000050: 8320 20e2 8083 20e2 8083 e280 8320 e280  .  ... ...... ..
    00000060: 8320 20e2 8083 e280 83e2 8083 2020 e280  .  .........  ..
    00000070: 8320 20e2 8083 2020 2020 e280 8320 e280  .  ...    ... ..
    00000080: 83e2 8083 e280 83e2 8083 2020 e280 8320  ..........  ... 
    00000090: e280 8320 e280 8320 e280 83e2 8083 e280  ... ... ........
    ```

2. We have the standard space (`0x20`), and the Unicode EM SPACE (`0xE2 0x80 0x83`). Since we have only two options, let's try to treat them as binary.
3. Run the [script.py](script.py) (which is commented) and get the flag.

### Flag

`picoCTF{not_all_spaces_are_created_equal_f71be4d2457dc2d068e8b1e7a51ed39a}`
