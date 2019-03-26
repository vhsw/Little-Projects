#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s maxN\n", argv[0]);
        return (1);
    }
    unsigned long n = atol(argv[1]);
    unsigned long *arr = calloc(n + 1, sizeof(unsigned long));
    unsigned long upper_lim = (long)sqrt((double)n) +1;
    for (unsigned long k1 = 1; k1 < upper_lim; ++k1)
    {
        for (unsigned long k2 = k1; k2 < (n / k1 + 1); ++k2)
        {
            unsigned long val = k1 != k2 ? k1 + k2 : k1;
            arr[k1 * k2] += val;
        }
    }

    printf("%ld\n", arr[n]);
    free(arr);
}
