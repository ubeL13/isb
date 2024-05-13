import json
import constants
from scipy.stats import norm, chi2

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
    p_value = norm.sf(abs(s_obs)) * 2  # two-sided p-value for frequency test
    return p_value


def runs_test(bit_string: str) -> float:
    """
    Perform the Runs Test on a given bit string and calculate the p-value.
    Parameters:
    bit_string (str): The bit string to be tested.
    Returns:
    float: The p-value, or 0.0 if non-random.
    """
    runs = 1
    for i in range(1, len(bit_string)):
        if bit_string[i] != bit_string[i - 1]:
            runs += 1
    n1 = bit_string.count('0')
    n2 = bit_string.count('1')
    prop = n2 / len(bit_string)
    tau = 2 / (len(bit_string) ** 0.5)
    if abs(prop - 0.5) > tau:
        return 0.0
    else:
        expected_runs = 2 * n1 * n2 / len(bit_string)
        var_runs = (2 * n1 * n2 * (2 * n1 * n2 - len(bit_string)) /
                    (len(bit_string) ** 2 * (len(bit_string) - 1)))
        test_statistic = abs(runs - expected_runs) / var_runs ** 0.5
        p_value = chi2.sf(test_statistic ** 2, 1)  # Chi-squared test is a square of Z
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
    max_run_lengths = []
    num_blocks = len(bit_string) // block_size
    for i in range(0, len(bit_string), block_size):
        block = bit_string[i:i + block_size]
        max_run = max(len(run) for run in block.split('0'))
        max_run_lengths.append(max_run)
    v_values = [max_run_lengths.count(i) for i in range(1, 7)]
    pi_values = constants.PI_VALUES
    chi_squared_stat = sum(
        [(v_values[i] - num_blocks * pi_values[i]) ** 2 / (num_blocks * pi_values[i]) for i in
         range(len(pi_values))])
    p_value = chi2.sf(chi_squared_stat,
                      len(pi_values) - 1)
    return chi_squared_stat, p_value

try:
    with open(constants.PATH, 'r') as file:
        sequences = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {constants.PATH} was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: The file {constants.PATH} contains invalid JSON.")
    exit()

results = {}
for name, bit_string in sequences.items():
    if not all(bit in ('0', '1') for bit in bit_string):
        print(f"Error: The sequence {name} contains invalid characters.")
        continue
    if len(bit_string) % constants.BLOCK_SIZE != 0:
        print(f"Error: The sequence {name} is not a multiple of the block size {constants.BLOCK_SIZE}.")
        continue

    freq_p_value = frequency_test(bit_string)
    runs_p_value = runs_test(bit_string)
    longest_runs_p_value = longest_run_ones_test(bit_string, constants.BLOCK_SIZE)[
        1]  # Assuming this function returns a tuple with p-value as the second element

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
