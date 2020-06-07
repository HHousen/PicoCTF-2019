#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main() {
    signal(SIGALRM, SIG_IGN);
    system("./times-up-one-last-time");
}