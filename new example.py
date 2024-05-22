import numpy as np
from functools import reduce
import operator as op

bits = np.array([0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0])
print (bits)

pos_with_bit_on = [i for i, bit in enumerate(bits) if bit]
print(pos_with_bit_on)

# XOR these positions 

xor_of_bits_on = reduce(op.xor, pos_with_bit_on)
print(xor_of_bits_on)

print(bin(xor_of_bits_on))


bits_with_error = np.array([0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0])

pos_with_bit_on2 = [i for i, bit in enumerate(bits_with_error) if bit]

xor_of_bits_on2 = reduce(op.xor, pos_with_bit_on2)
print(xor_of_bits_on2)

print(bin(xor_of_bits_on2))

# Error in pos 10


