import random


def generate_128_bit_binary_sequence():
    # Generate 128 random bits
    random_bits = random.getrandbits(128)
    py_binary_sequence = format(random_bits, '0128b')
    return py_binary_sequence


binary_sequence = generate_128_bit_binary_sequence()
print("128-bit binary sequence:", binary_sequence)
