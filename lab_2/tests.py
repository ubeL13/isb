import json
import math

from scipy.stats import norm
from scipy.special import erfc
from mpmath import gammainc

from constants import PATH, BLOCK_SIZE, PI_VALUES


def load_sequences(path):
    """
    Load and return the sequences from the specified JSON file.
    Parameters: path (str): The path to the JSON file.
    Returns: dict: The loaded sequences.
    """
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {path} was not found.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: The file {path} contains invalid JSON.")
        exit()


def frequency_test(bit_string: str) -> float:
    """
    Perform the Frequency Test on a given bit string and calculate the p-value.
    Parameters: bit_string (str): The bit string to be tested.
    float: The p-value.
    """
    if not bit_string:
        raise ValueError("The bit string provided is empty.")

    count = sum(1 if bit == '1' else -1 for bit in bit_string)
    n = len(bit_string)

    try:
        s_obs = abs(count) / (n ** 0.5)
        p_value = norm.sf(abs(s_obs)) * 2
        return p_value
    except ZeroDivisionError:
        raise ValueError("Bit string length must be greater than zero.")


def runs_test(bit_string: str) -> float:
    """
    Perform the Runs Test on a given bit string and calculate the p-value.
    Parameters:
    bit_string (str): The bit string to be tested.
    Returns:
    float: The p-value.
    """
    try:
        sum_of_ones = bit_string.count('1')
        proportion = sum_of_ones / len(bit_string)

        if abs(proportion - 0.5) >= 2 / math.sqrt(len(bit_string)):
            p_value = 0
        else:
            count = 0
            for i in range(0, len(bit_string) - 1):
                if bit_string[i] != bit_string[i + 1]:
                    count += 1
            numerator = abs(count - 2 * len(bit_string) * proportion * (1 - proportion))
            denominator = 2 * math.sqrt(2 * len(bit_string)) * proportion * (1 - proportion)
            p_value = erfc(numerator / denominator)

        return p_value

    except ValueError as e:
        print(f"A ValueError occurred: {e}")
    except ZeroDivisionError as e:
        print(f"Division by zero error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def longest_run_ones_test(bit_string: str, block_size: int) -> tuple[float, float]:
    """
    Perform the Longest Run of Ones in a Block Test on a given bit string and calculate the p-value.
    Parameters:
    bit_string (str): The bit string to be tested.
    block_size (int): The size of the block.
    Returns: tuple[float, float]: A tuple containing the chi-squared statistic and the p-value.
    """
    try:
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
            match max_length:
                case int(0) | int(1):
                    v_counts[0] += 1
                case int(2):
                    v_counts[1] += 1
                case int(3):
                    v_counts[2] += 1
                case _:
                    v_counts[3] += 1

        chi_squared = sum(
            ((v_counts[i] - len(max_len) * PI_VALUES[i]) ** 2) / (len(max_len) * PI_VALUES[i]) for i in range(4)
        )
        p_value = gammainc(1.5, chi_squared / 2)
        return p_value

    except NameError as e:
        print(f"An undefined variable was used: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main() -> None:
    """
   Loads binary sequences from a file, performs statistical tests on each sequence, and prints the results.
   Args: PATH (str)
    """
    try:
        sequences = load_sequences(PATH)
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
                'longest_run_ones_p_value': longest_runs_p_value}
        for name, result in results.items():
            print(f"Results for {name}:")
            print(f"Frequency Test p-value: {result['frequency_test_p_value']}")
            print(f"Runs Test p-value: {result['runs_test_p_value']}")
            print(f"Longest Run of Ones p-value: {result['longest_run_ones_p_value']}")

    except Exception as e:
        print('Error', str(e))


if __name__ == "__main__":
    main()
