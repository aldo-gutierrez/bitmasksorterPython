import random
import time


def array_copy(src: list[int], src_pos: int, dest: list[int], dest_pos: int, length: int):
    dest[dest_pos:dest_pos + length] = src[src_pos:src_pos + length]
    # this is faster in pypy
    # for i in range(length):
    #     dest[i + dest_pos] = src[i + src_pos]


def new_array(length: int):
    return [0] * length


def calculate_mask_int(array: list[int], start: int, end: int) -> list[int]:
    mask: int = 0x00000000
    inv_mask: int = 0x00000000
    for i in range(start, end):
        ei: int = array[i]
        mask = mask | ei
        inv_mask = inv_mask | (~ei)
    return [mask, inv_mask]


def get_mask_as_array(mask: int) -> list[int]:
    res: list[int] = []
    for i in reversed(range(0, 32)):
        if ((mask >> i) & 1) == 1:
            res.append(i)
    return res


def partition_not_stable(array: list[int], start: int, end_p1: int, mask: int) -> int:
    left: int = start
    right: int = end_p1 - 1

    while left <= right:
        element: int = array[left]
        if (element & mask) == 0:
            left += 1
        else:
            while left <= right:
                element = array[right]
                if (element & mask) == 0:
                    (array[left], array[right]) = (array[right], array[left])
                    left += 1
                    right -= 1
                    break
                else:
                    right -= 1
    return left


def partition_reverse_not_stable(array: list[int], start: int, end_p1: int, mask: int) -> int:
    left: int = start
    right: int = end_p1 - 1

    while left <= right:
        element: int = array[left]
        if (element & mask) == 0:
            while left <= right:
                element = array[right]
                if (element & mask) == 0:
                    right -= 1
                else:
                    (array[left], array[right]) = (array[right], array[left])
                    left += 1
                    right -= 1
                    break
        else:
            left += 1
    return left


def partition_stable(array: list[int], start: int, end_p1: int, mask: int, aux: list[int]) -> int:
    left: int = start
    right: int = 0
    for i in range(start, end_p1):
        element: int = array[i]
        if (element & mask) == 0:
            array[left] = element
            left += 1
        else:
            aux[right] = element
            right += 1

    array_copy(aux, 0, array, left, right)
    return left


def partition_stable_last_bits(array: list[int], start: int, end_p1: int, mask: int, d_range: int, aux: list[int]):
    count: list[int] = new_array(d_range)
    for i in range(start, end_p1):
        count[array[i] & mask] += 1

    sum: int = 0
    for i in range(0, d_range):
        count_i: int = count[i]
        count[i] = sum
        sum += count_i

    for i in range(start, end_p1):
        element: int = array[i]
        element_shift_masked: int = element & mask
        aux[count[element_shift_masked]] = element
        count[element_shift_masked] += 1

    array_copy(aux, 0, array, start, end_p1 - start)


def partition_stable_one_group_bits(array: list[int], start: int, end: int, mask: int, shift_right: int,
                                    d_range: int, aux):
    count: list[int] = new_array(d_range)

    for i in range(start, end):
        count[(array[i] & mask) >> shift_right] += 1

    sum: int = 0
    for i in range(0, d_range):
        count_i: int = count[i]
        count[i] = sum
        sum += count_i

    for i in range(start, end):
        element: int = array[i]
        element_shift_masked: int = (element & mask) >> shift_right
        aux[count[element_shift_masked]] = element
        count[element_shift_masked] += 1

    array_copy(aux, 0, array, start, end - start)


def sort(array: list[int]):
    if len(array) < 2:
        return

    start: int = 0
    end_p1: int = len(array)

    mask_parts = calculate_mask_int(array, start, end_p1)
    mask: int = mask_parts[0] & mask_parts[1]
    b_list = get_mask_as_array(mask)
    if len(b_list) == 0:
        return

    if b_list[0] == 31:
        k = b_list[0]
        final_left: int = partition_not_stable(array, start, end_p1, 1 << k)
        n1 = final_left - start
        n2 = end_p1 - final_left
        mask1 = 0
        mask2 = 0
        if n1 > 1:
            mask_parts = calculate_mask_int(array, start, final_left)
            mask1 = mask_parts[0] & mask_parts[1]
            if mask1 == 0:
                n1 = 0
        if n2 > 1:
            mask_parts = calculate_mask_int(array, final_left, end_p1)
            mask2 = mask_parts[0] & mask_parts[1]
            if mask2 == 0:
                n2 = 0

        aux = new_array(max(n1, n2))

        if n1 > 1:
            b_list = get_mask_as_array(mask1)
            radix_bit_sort(array, start, final_left, b_list, aux)

        if n2 > 1:
            b_list = get_mask_as_array(mask2)
            radix_bit_sort(array, final_left, end_p1, b_list, aux)

    else:
        aux = new_array(end_p1 - start)
        radix_bit_sort(array, start, end_p1, b_list, aux)
    return


def reverse_list_get(b_list, index):
    return b_list[len(b_list) - 1 - index]


def getSections(bList):
    if len(bList) == 0:
        return ()

    max_bits_digit = 11
    sections = []
    b = 0
    shift = reverse_list_get(bList, b)
    bits = 1
    b = b + 1
    while b < len(bList):
        bitIndex = reverse_list_get(bList, b)
        if bitIndex <= shift + max_bits_digit - 1:
            bits = (bitIndex - shift + 1)
        else:
            sections.append((bits, shift, shift + bits - 1))
            shift = bitIndex
            bits = 1
        b = b + 1

    sections.append((bits, shift, shift + bits - 1))
    return sections


def get_mask_range_bits(b_start: int, b_end: int):
    return ((1 << b_start + 1 - b_end) - 1) << b_end


def radix_bit_sort(array, start: int, end_p1: int, b_list, aux: list[int]):
    sections = getSections(b_list)
    index = 0
    while index < len(sections):
        res = sections[index]
        bits = res[0]
        shift = res[1]
        b_start = res[2]
        mask = get_mask_range_bits(b_start, shift)
        if bits == 1:
            partition_stable(array, start, end_p1, mask, aux)
        else:
            d_range = 1 << bits
            if shift == 0:
                partition_stable_last_bits(array, start, end_p1, mask, d_range, aux)
            else:
                partition_stable_one_group_bits(array, start, end_p1, mask, shift, d_range, aux)
        index = index + 1
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Comparing Sorters')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

ITERATIONS = 20
RANGE = 1000
SIZE = 1000000
# RANGE = 1000000000
# SIZE = 40000000

totalElapsedP = 0
totalElapsedK = 0

for j in range(0, ITERATIONS):
    vet = [random.randint(0, RANGE) for _ in range(SIZE)]
    start_t = time.time()
    vet.sort()
    end_t = time.time()
    elapsedP = end_t - start_t
    totalElapsedP += elapsedP

    vet = [random.randint(0, RANGE) for _ in range(SIZE)]
    start_t = time.time()
    sort(vet)
    end_t = time.time()
    elapsedK = end_t - start_t
    totalElapsedK += elapsedK

    print("elapsed python " + str(elapsedP) + " s.")
    print("elapsed radixb " + str(elapsedK) + " s.")
    print("\n")

print("elapsed AVG python " + str(totalElapsedP / ITERATIONS) + " s.")
print("elapsed AVG radixb " + str(totalElapsedK / ITERATIONS) + " s.")
print("\n")
