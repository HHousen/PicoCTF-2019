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

