# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import time


# import numpy


def arrayCopy(src: list[int], srcPos: int, dest, destPos: int, length: int):
    dest[destPos:destPos + length] = src[srcPos:srcPos + length]
    # for i in range(length):
    #     dest[i + destPos] = src[i + srcPos]


def newArray(length: int):
    # numpy.empty(length, dtype=int)
    # return numpy.zeros((length,), numpy.int32)
    return [0] * length



def getMaskBit(array: list[int], start: int, end: int) -> list[int]:
    mask: int = 0x00000000
    inv_mask: int = 0x00000000
    for i in range(start, end):
        ei: int = array[i]
        mask = mask | ei
        inv_mask = inv_mask | (~ei)
    return [mask, inv_mask]


def getMaskAsArray(mask: int) -> list[int]:
    res: list[int] = []
    for i in reversed(range(0, 32)):
        if ((mask >> i) & 1) == 1:
            res.append(i)
    return res


# def getMaskBit(k):
#    return 1 << k


def twoPowerX(k) -> int:
    return 1 << k


def swap(array: list[int], left: int, right: int):
    aux: int = array[left]
    array[left] = array[right]
    array[right] = aux


def partitionNotStable(array: list[int], start: int, end: int, mask: int) -> int:
    left: int = start
    right: int = end - 1

    while left <= right:
        element: int = array[left]
        if (element & mask) == 0:
            left += 1
        else:
            while left <= right:
                element = array[right]
                if (element & mask) == 0:
                    swap(array, left, right)
                    left += 1
                    right -= 1
                    break
                else:
                    right -= 1
    return left


def partitionReverseNotStable(array: list[int], start: int, end: int, mask: int) -> int:
    left: int = start
    right: int = end - 1

    while left <= right:
        element: int = array[left]
        if (element & mask) == 0:
            while left <= right:
                element = array[right]
                if (element & mask) == 0:
                    right -= 1
                else:
                    swap(array, left, right)
                    left += 1
                    right -= 1
                    break
        else:
            left += 1
    return left


def partitionStable(array: list[int], start: int, end: int, mask: int, aux: list[int]) -> int:
    left: int = start
    right: int = 0
    for i in range(start, end):
        element: int = array[i]
        if (element & mask) == 0:
            array[left] = element
            left += 1
        else:
            aux[right] = element
            right += 1

    arrayCopy(aux, 0, array, left, right)
    return left


def partitionStableLastBits(array: list[int], start: int, end: int, mask: int, twoPowerK: int, aux: list[int]):
    leftX: list[int] = newArray(twoPowerK)
    count: list[int] = newArray(twoPowerK)
    for i in range(start, end):
        count[array[i] & mask] += 1

    for i in range(1, twoPowerK):
        leftX[i] = leftX[i - 1] + count[i - 1]

    for i in range(start, end):
        element: int = array[i]
        elementShiftMasked: int = element & mask
        aux[leftX[elementShiftMasked]] = element
        leftX[elementShiftMasked] += 1

    arrayCopy(aux, 0, array, start, end - start)


def partitionStableGroupBits(array: list[int], start: int, end: int, mask: int, shiftRight: int, twoPowerK: int, aux):
    leftX: list[int] = newArray(twoPowerK)
    count: list[int] = newArray(twoPowerK)

    for i in range(start, end):
        count[(array[i] & mask) >> shiftRight] += 1

    for i in range(1, twoPowerK):
        leftX[i] = leftX[i - 1] + count[i - 1]

    for i in range(start, end):
        element: int = array[i]
        elementShiftMasked: int = (element & mask) >> shiftRight
        aux[leftX[elementShiftMasked]] = element
        leftX[elementShiftMasked] += 1

    arrayCopy(aux, 0, array, start, end - start)


def sort(array: list[int]):
    if len(array) < 2:
        return

    start: int = 0
    end: int = len(array)

    maskParts = getMaskBit(array, start, end)
    mask: int = maskParts[0] & maskParts[1]
    kList = getMaskAsArray(mask)
    if len(kList) == 0:
        return

    if kList[0] == 31:
        sortMask: int = twoPowerX(kList[0])
        finalLeft: int = partitionNotStable(array, start, end, sortMask)
        if finalLeft - start > 1:
            aux = newArray(finalLeft - start)
            maskParts = getMaskBit(array, start, finalLeft)
            mask = maskParts[0] & maskParts[1]
            kList = getMaskAsArray(mask)
            radixSort(array, start, finalLeft, kList, len(kList) - 1, 0, aux)

        if end - finalLeft > 1:
            aux = newArray(end - finalLeft)
            maskParts = getMaskBit(array, finalLeft, end)
            mask = maskParts[0] & maskParts[1]
            kList = getMaskAsArray(mask)
            radixSort(array, finalLeft, end, kList, len(kList) - 1, 0, aux)

    else:
        aux = newArray(end - start)
        radixSort(array, start, end, kList, len(kList) - 1, 0, aux)


def radixSort(array, start: int, end: int, kList, kIndexStart: int, kIndexEnd: int, aux):
    #        for (int i = kIndexStart; i >= kIndexEnd; i--) {
    i: int = kIndexStart
    while i >= kIndexEnd:
        kListI = kList[i]
        maskI: int = twoPowerX(kListI)
        bits: int = 1
        imm: int = 0
        for j in reversed(range(1, 12)):
            if i - j >= kIndexEnd:
                kListIm1 = kList[i - j]
                if kListIm1 == kListI + j:
                    maskIm1 = twoPowerX(kListIm1)
                    maskI = maskI | maskIm1
                    bits += 1
                    imm += 1
                else:
                    break
        i -= imm
        if bits == 1:
            partitionStable(array, start, end, maskI, aux)
        else:
            twoPowerBits: int = twoPowerX(bits)
            if kListI == 0:
                partitionStableLastBits(array, start, end, maskI, twoPowerBits, aux)
            else:
                partitionStableGroupBits(array, start, end, maskI, kListI, twoPowerBits, aux)
        i -= 1


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
    start = time.time()
    vet.sort()
    end = time.time()
    elapsedP = end - start
    totalElapsedP += elapsedP

    vet = [random.randint(0, RANGE) for _ in range(SIZE)]
    start = time.time()
    sort(vet)
    end = time.time()
    elapsedK = end - start
    totalElapsedK += elapsedK

    print("elapsed python " + str(elapsedP) + " s.")
    print("elapsed radixb " + str(elapsedK) + " s.")
    print("\n")

print("elapsed AVG python " + str(totalElapsedP/ITERATIONS) + " s.")
print("elapsed AVG radixb " + str(totalElapsedK/ITERATIONS) + " s.")
print("\n")
