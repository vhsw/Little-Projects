#!/usr/bin/env python3

import argparse
import math

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('maxN', type=int, nargs=1)

args = parser.parse_args()
n = int(args.maxN[0])

arr = [0] * (n + 1)
for k1 in range(1, int(math.sqrt(n) + 1)):
    for k2 in range(k1, n // k1 + 1):
        val = k1 + k2 if k1 != k2 else k1
        arr[k1 * k2] += val

print(arr[-1])
