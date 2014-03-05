#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int main (int argc, char **argv, char **envp) {
    int hex = 16, deci, quot, ctr;

    printf("Enter Decimal num: ");
    scanf("%d", &deci);

    for (ctr = 1; ctr<=deci; ctr++)
        quot = deci / hex;

    printf("Quotient is %d\n", quot);
    printf("Hex is %X\n", deci);

    getchar();
    return(0);
}

