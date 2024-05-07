# BitMask Sorters in Python

This project explores various sorting algorithms employing a BitMask approach.
One of the algorithms is a Radix Sort utilizing a BitMask to minimize the number of Count Sort iterations required.

The following code demonstrates the calculation of the BitMask:

```
    def calculate_mask_int(array: list[int], start: int, end: int) -> [int]:
        mask: int = 0x00000000
        inv_mask: int = 0x00000000
        for i in range(start, end):
            ei: int = array[i]
            mask = mask | ei
            inv_mask = inv_mask | (~ei)
        return mask & inv_mask
```

For further details, refer to the initial Java implementation
[Java Version and Documentation] (https://github.com/aldo-gutierrez/bitmasksorter)

## RadixBitSorter:
RadixBitSorter is the implementation of a Radix Sort utilizing a BitMask to minimize the number of Count Sort iterations required.

RadixBitSorter is an LSD Radix Sorter. 
The number of bits per iteration has been increased to 11, departing from the standard 8.
For a dual-core machine or lower, it is recommended to use 8 bits.

# Speed
### Comparison for sorting 1 million integer elements ranging from 0 to 1000.
Environment: AMD Ryzen 7 4800H processor

| Algorithm                      | avg. CPU time [ms] |
|--------------------------------|-------------------:|
| Python 3.9.10 sort             |                117 |
| Python 3.9.10 RadixBitSorter   |                369 |
| pypy3.9-v7.3.9 sort            |                103 |
| pypy3.9-v7.3.9 RadixBitSorter  |                 11 |

RadixBitSorter is slower than python standard sort in Python 3.9.10, maybe is because 
Python sort is implemented in C and not in Python which is a disadvantage for RadixBitSorter.

RadixBitSorter is faster in pypy3.0-v7.3.9 because pypy JIT can optimize methods according to runtime parameters
and create different methods for different parameters.

### Comparison for sorting 40 million integer elements ranging from 0 to 1000 million.
Environment: AMD Ryzen 7 4800H processor

| Algorithm                      | avg. CPU time [ms] |
|--------------------------------|-------------------:|
| Python 3.9.10 sort             |              20878 |
| Python 3.9.10 RadixBitSorter   |             100919 |
| pypy3.9-v7.3.9 sort            |               6532 |
| pypy3.9-v7.3.9 RadixBitSorter  |               2628 |


RadixBitSorter is slower than python standard sort in Python 3.9.10, maybe is because 
Python sort is implemented in C and not in Python which is a disadvantage for RadixBitSorter.

RadixBitSorter is faster in pypy3.0-v7.3.9 because pypy JIT can optimize methods according to runtime parameters
and create different methods for different parameters.

# TODO
- Learn python arrays
- Learn numpy
- Learn more about performance optimization in python
- Make a Library
