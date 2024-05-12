import json
import constants

def frequency_test(bit_string):
    count = 0
    for bit in bit_string:
        count += 1 if bit == '1' else -1
    s_obs = abs(count) / len(bit_string) ** 0.5
    return s_obs

def runs_test(bit_string):
    runs = 1
    for i in range(1, len(bit_string)):
        if bit_string[i] != bit_string[i-1]:
            runs += 1
    prop = bit_string.count('1') / len(bit_string)
    tau = 2 / (len(bit_string) ** 0.5)
    if abs(prop - 0.5) > tau:
        return 0.0
    else:
        return runs

def longest_run_ones_test(bit_string, block_size):
    max_run_lengths = []
    for i in range(0, len(bit_string), block_size):
        block = bit_string[i:i+block_size]
        max_run = max(len(run) for run in block.split('0'))
        max_run_lengths.append(max_run)
    return max_run_lengths

with open(constants.PATH, 'r') as file:
    sequences = json.load(file)

results = {}
for name, bit_string in sequences.items():
    results[name] = {
        'frequency_test_statistic': frequency_test(bit_string),
        'runs_test_statistic': runs_test(bit_string),
        'longest_run_ones': longest_run_ones_test(bit_string, constants.BLOCK_SIZE)
    }

for name, result in results.items():
    print(f"Results for {name}:")
    print(f"Frequency Test Statistic: {result['frequency_test_statistic']}")
    print(f"Runs Test Statistic: {result['runs_test_statistic']}")
    print(f"Longest Run of Ones: {result['longest_run_ones']}n")
