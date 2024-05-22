import json
import math

from scipy.stats import norm
from scipy.special import erfc
from mpmath import gammainc

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
    bits = [bit_string[i:i + block_size] for i in range(0, len(bit_string), block_size)]

    v_counts = [0] * 4

    for block in bits:
        longest = 0
        for bit in block:
            if bit == '1':
                longest += 1
            else:
                longest = 0

        if longest <= 1:
            v_counts[0] += 1
        elif longest == 2:
            v_counts[1] += 1
        elif longest == 3:
            v_counts[2] += 1
        else:
            v_counts[3] += 1

    chi_squared = sum(
        ((v_counts[i] - len(bits) * PI_VALUES[i]) ** 2) / (len(bits) * PI_VALUES[i]) for i in range(4))
    p_value = gammainc(1.5, chi_squared / 2)

    return p_value

import json

# Предполагаем, что функции frequency_test, runs_test и longest_run_ones_test уже определены
# Предполагаем, что переменная BLOCK_SIZE также определена

def main():
    PATH = 'path/to/your/file.json'  # Замените на фактический путь к вашему файлу

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

if __name__ == "__main__":
    main()
