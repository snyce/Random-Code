#include <stdio.h>

int main(int argc, char **argv, char **envp)
{
    int i = 0;

    while(envp[i] != NULL)
    {
        printf("Environ: %s\n", envp[i++]);
    }
    return(0);
}
