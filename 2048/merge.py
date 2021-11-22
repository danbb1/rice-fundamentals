"""
Merge function for 2048 game.
"""


def shift_line(line):
    """
    Function that shifts non zero values to left most indices
    """
    new_line = [0] * len(line)
    non_zero_values = 0

    for value in line:
        if value > 0:
            new_line[non_zero_values] = value
            non_zero_values += 1

    return new_line


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """

    new_line = shift_line(line)

    for index, value in enumerate(new_line):
        next_value = new_line[index + 1] if index + 1 < len(new_line) else None

        if value == next_value:
            new_line[index] *= 2
            new_line[index + 1] = 0

    return shift_line(new_line)


print ("Testing merge, computed:", merge([0, 2, 4, 8, 16]), "Expected: [2, 4, 8, 16, 0]")
print ("Testing merge, computed:", merge([2, 2, 2, 2, 2]), "Expected: [4, 4, 2, 0, 0]")
print ("Testing merge, computed:", merge([0, 2, 0, 2, 0]), "Expected: [4, 0, 0, 0, 0]")
print ("Testing merge, computed:", merge([0, 0, 0, 0, 2]), "Expected: [2, 0, 0, 0, 0]")
print ("Testing merge, computed:", merge([2, 0, 0, 0, 2]), "Expected: [4, 0, 0, 0, 0]")
print ("Testing merge, computed:", merge([32, 32, 16, 16, 0]), "Expected: [64, 32, 0, 0, 0]")
print ("Testing merge, computed:", merge([2, 0, 2, 4]), "Expected: [4, 4, 0, 0]")

