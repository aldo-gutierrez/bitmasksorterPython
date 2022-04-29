# Mask Bit Sorters Python
This project tests different ideas for sorting algorithms.
We use a bitmask as a way to get statistical information about the numbers to be sorted.
All the algorithms use this bitmask.

See the initial implementation in java for more information.

[Java Version and Documentation] (https://github.com/aldo-gutierrez/bitmasksorter)

Only a test of RadixBitSorter is implemented for now in this project

## RadixBitSorter:
RadixBitSorter is a Radix Sorter that uses the bitmask to make a LSD sorting using bits instead of bytes
upto 11 bits at a time.

# Speed
Comparison for sorting 1 Million int elements with range from 0 to 1000 in an AMD Ryzen 7 4800H processor,

| Algorithm                      | AVG CPU time [ms] |
|--------------------------------|------------------:|
| Python 3.9.10 sort             |               114 |
| Python 3.9.10 RadixBitSorter   |               373 |
| pypy3.9-v7.3.9 sort            |               103 |
| pypy3.9-v7.3.9 RadixBitSorter  |                11 |

RadixBitSorter is slower than python standard sort in Python 3.9.10, maybe is because 
Python sort is implemented in C and not in Python which is a disadvantage for RadixBitSorter.

Comparison for sorting 40 Million int elements with range from 0 to 1000 Million in an AMD Ryzen 7 4800H processor,


| Algorithm                      |    AVG CPU time [ms] |
|--------------------------------|---------------------:|
| Python 3.9.10 sort             |                20878 |
| Python 3.9.10 RadixBitSorter   |               100919 |
| pypy3.9-v7.3.9 sort            |                 6532 |
| pypy3.9-v7.3.9 RadixBitSorter  |                 2628 |


RadixBitSorter is slower than python standard sort in Python 3.9.10, maybe is because 
Python sort is implemented in C and not in Python which is a disadvantage for RadixBitSorter.

RadixBitSorter is faster in pypy3.0-v7.3.9 because pypy JIT can optimize methods according to runtime parameters
and create different methods for different parameters

# TODO
- Learn python arrays
- Learn numpy
- Learn more about performance optimization in python
- Make a Library
