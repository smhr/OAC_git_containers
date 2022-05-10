#!/usr/bin/env python3

from sys import argv

assert len(argv) == 2
accuracy = int(argv[1])

assert len(argv) == 2
accuracy = int(argv[1])
assert accuracy <= 9999999

pi = 0


for i in range(0, accuracy):
    pi += ((4.0 * (-1)**i) / (2*i + 1))

print("Estimated Pi = {0:16.13f}".format(pi))
