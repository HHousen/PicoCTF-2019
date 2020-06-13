# asm1

## Problem

> What does asm1(0x610) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. Source located in the directory at /problems/asm1_1_95494d904d73b330976420bc1cd763ec.

* [Source](./test.S)

## Solution

1. Let's look at the source:

    ```assembly
    asm1:
        <+0>:	push   ebp
        <+1>:	mov    ebp,esp
        <+3>:	cmp    DWORD PTR [ebp+0x8],0x3b9
        <+10>:	jg     0x50f <asm1+34>
        <+12>:	cmp    DWORD PTR [ebp+0x8],0x1
        <+16>:	jne    0x507 <asm1+26>
        <+18>:	mov    eax,DWORD PTR [ebp+0x8]
        <+21>:	add    eax,0x11
        <+24>:	jmp    0x526 <asm1+57>
        <+26>:	mov    eax,DWORD PTR [ebp+0x8]
        <+29>:	sub    eax,0x11
        <+32>:	jmp    0x526 <asm1+57>
        <+34>:	cmp    DWORD PTR [ebp+0x8],0x477
        <+41>:	jne    0x520 <asm1+51>
        <+43>:	mov    eax,DWORD PTR [ebp+0x8]
        <+46>:	sub    eax,0x11
        <+49>:	jmp    0x526 <asm1+57>
        <+51>:	mov    eax,DWORD PTR [ebp+0x8]
        <+54>:	add    eax,0x11
        <+57>:	pop    ebp
        <+58>:	ret
    ```

2. We call `asm1(0x610)` so we are putting `0x610` into the stack. This value gets pushed into ebp and then moved into esp on lines 0 and 1. Normally ebp is used to backup esp, so if esp is changed by the code in a function, all it takes to restore esp is mov esp, ebp. Also since ebp is normally left unchanged by the code in a function, it can be used to access passed parameters or local variables without having to adjust the offsets. More info about esp and ebp: [StackOverflow answer](https://stackoverflow.com/a/21718526).

    ```assembly
    <+0>:	push   ebp
    <+1>:	mov    ebp,esp
    ```

3. First Condition:

    ```assembly
    <+3>:	cmp    DWORD PTR [ebp+0x8],0x3b9
    <+10>:	jg     0x50f <asm1+34>
    ```

    Here, we are comparing (cmp) first value in the stack (which is `0x610`) to 0x3b9. The jg means "jump if greater". Since `0x610` is indeed greater than 0x3b9, we jump to the line given by this condition: line 34.

4. Second Condition:

    ```assembly
    <+34>:	cmp    DWORD PTR [ebp+0x8],0x477
    <+41>:	jne    0x520 <asm1+51>
    ```

    Here, we have another comparison, this time between the first value in the stack and `0x477`. The condition jne means "jump if not equal". Since `0x610` is not equal to `0x477`, this is true and jump to line 51.

5. Addition

    ```assembly
    <+51>:	mov    eax,DWORD PTR [ebp+0x8]
    <+54>:	add    eax,0x11
    ```

    Here, the value in the stack is moved to the variable that will be returned eax. We then add `0x11` to it, so now eax is equal to `0x610+0x11=0x621`.

6. Ending

    ```assembly
    <+57>:	pop    ebp
    <+58>:	ret
    ```

    On line 57, the stack is popped and eax is returned. Since eax is equal to `0x621`, that is our flag.

### Flag

`0x621`
