import json
import math

from scipy.stats import norm, chi2
from scipy.special import erfc, gammainc

from constants import PATH, BLOCK_SIZE, PI_VALUES


def frequency_test(bit_string: str) -> float:
    """
    Perform the Frequency Test on a given bit string and calculate the p-value.
    Parameters:
    bit_string (str): The bit string to be tested.
    Returns:
    float: The p-value.
    """
    count = sum(1 if bit == '1' else -1 for bit in bit_string)
    s_obs = abs(count) / (len(bit_string) ** 0.5)
    p_value = norm.sf(abs(s_obs)) * 2
    return p_value


def runs_test(bit_string: str) -> float:
    """
    Perform the Runs Test on a given bit string and calculate the p-value.
    Parameters:
    bit_string (str): The bit string to be tested.
    Returns:
    float: The p-value.
    """
    sum_of_ones = bit_string.count('1')
    proportion = sum_of_ones / len(bit_string)
    if abs(proportion - 0.5) >= 2 / math.sqrt(len(bit_string)):
        p_value = 0
    else:
        count = 0
        for i in range(0, len(bit_string)-1):
            if bit_string[i] != bit_string[i + 1]:
                count += 1

        numerator = abs(count - 2 * len(bit_string) * proportion * (1 - proportion))
        denominator = 2 * math.sqrt(2 * len(bit_string)) * proportion * (1 - proportion)

        p_value = erfc(numerator / denominator)

    return p_value



def longest_run_ones_test(bit_string: str, block_size: int) -> tuple[float, float]:
    """
    Perform the Longest Run of Ones in a Block Test on a given bit string and calculate the p-value.
    Parameters:
    bit_string (str): The bit string to be tested.
    block_size (int): The size of the block.
    Returns:
    tuple[float, float]: A tuple containing the chi-squared statistic and the p-value.
    """
    max_len = [bit_string[i * block_size: (i + 1) * block_size] for i in range(0, len(bit_string) // block_size)]
    v_counts = [0, 0, 0, 0]
    for block in max_len:
        count = 0
        max_length = 0
        for bit in block:
            if bit == '1':
                count += 1
                max_length = max(max_length, count)
            else:
                count = 0
        if max_length <= 1:
            v_counts[0] += 1
        elif max_length == 2:
            v_counts[1] += 1
        elif max_length == 3:
            v_counts[2] += 1
        elif max_length >= 4:
            v_counts[3] += 1
    chi_squared = sum(((v_counts[i] - len(max_len) * PI_VALUES[i]) ** 2) / (len(max_len) * PI_VALUES[i]) for i in range(4))
    p_value = gammainc(1.5, chi_squared / 2)
    return p_value

    # blocks = [bit_string[i * block_size: (i + 1) * block_size] for i in range(0, len(bit_string) // block_size)]
    # for block in range(0, len(name), 8):
    #         block = name[step: step + 8]
    #         maxline = 0
    #         count = 0
    #         for i in block:
    #             if i == '1':
    #                 count += 1
    #                 maxline = max(maxline, count)
    #             else:
    #                 count = 0
    #         max_len[maxline] = max_len.get(maxline, 0) + 1
    #     for maxline, count in max_len.items():
    #         if maxline == 1:
    #             v[1] += count
    #         elif maxline == 2:
    #             v[2] += count
    #         elif maxline == 3:
    #             v[3] += count
    #         else:
    #             v[4] += count
    #     xi_squared = sum(((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i]) for i in range(1, 5))
    #     p = mpmath.gammainc(3 / 2, xi_squared / 2)
    #     return p


try:
    with open(PATH, 'r') as file:
        sequences = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {PATH} was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: The file {PATH} contains invalid JSON.")
    exit()

results = {}
for name, bit_string in sequences.items():
    if not all(bit in ('0', '1') for bit in bit_string):
        print(f"Error: The sequence {name} contains invalid characters.")
        continue
    if len(bit_string) % BLOCK_SIZE != 0:
        print(f"Error: The sequence {name} is not a multiple of the block size {BLOCK_SIZE}.")
        continue

    freq_p_value = frequency_test(bit_string)
    runs_p_value = runs_test(bit_string)
    longest_runs_p_value = longest_run_ones_test(bit_string, BLOCK_SIZE)

    results[name] = {
        'frequency_test_p_value': freq_p_value,
        'runs_test_p_value': runs_p_value,
        'longest_run_ones_p_value': longest_runs_p_value
    }

for name, result in results.items():
    print(f"Results for {name}:")
    print(f"Frequency Test p-value: {result['frequency_test_p_value']}")
    print(f"Runs Test p-value: {result['runs_test_p_value']}")
    print(f"Longest Run of Ones p-value: {result['longest_run_ones_p_value']}")
