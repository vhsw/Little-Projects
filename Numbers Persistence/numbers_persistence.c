#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <sys/sysinfo.h>
#include <limits.h>

#define BASE 10

int n_workers = 0;
size_t found_numbres[] = {0, 0, 0, 0};

int persist(size_t num, size_t steps)
{
    if (num < BASE)
        return (steps);
    size_t result = 1;
    while (num)
    {
        result *= (num % BASE);
        num /= BASE;
    }
    return (persist(result, steps + 1));
}

void *persist_range(void *vargs)
{

    int worker = n_workers++;
    int *args = (int *)vargs;

    for (size_t i = worker; i < __SIZE_MAX__; i += args[1])
    {
        if (found_numbres[worker])
            return NULL;
        int res = persist(i, 1);
        if (res >= args[0])
            found_numbres[worker] = i;
    }
    return NULL;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Usage: %s <target persistence>\nFor example: %s 10\n", argv[0], argv[0]);
        return (1);
    }

    int min_persist = atoi(argv[1]);
    if (min_persist <= 0)
    {
        printf("Target persistence must be positive\n");
        return (1);
    }
    if (min_persist == 1)
    {
        printf("0\n");
        return (0);
    }
    int n_threads = get_nprocs();
    pthread_t threads[n_threads];
    int args[] = {min_persist, n_threads};
    for (int i = 0; i < n_threads; i++)
    {
        pthread_create(&threads[i], NULL, persist_range, (void *)&args);
    }
    for (int i = 0; i < n_threads; i++)
        pthread_join(threads[i], NULL);

    size_t min_num = found_numbres[0];
    for (int i = 0; i < n_threads; i++)
        if (min_num > found_numbres[i])
            min_num = found_numbres[i];

    printf("%lu\n", min_num);
    return (0);
}