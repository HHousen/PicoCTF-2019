#include <stdio.h>

int asm3(int, int, int);

int main(int argc, char* argv[])
{
    printf("0x%x\n", asm3(0xc4bd37e3,0xf516e15e,0xeea4f333));
    return 0;
}