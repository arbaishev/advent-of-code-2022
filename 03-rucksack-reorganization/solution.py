# coding=utf-8
from typing import List


def read_input() -> List[str]:
    input_file_name = "input.txt"

    try:
        with open(input_file_name) as input_file:
            input_lines = input_file.read()
            if not input_lines:
                raise Exception(f"File {input_file_name} is empty")
            return [line.strip() for line in input_lines.split("\n")]
    except EnvironmentError as e:
        raise Exception(f"File {input_file} is missing or invalid") from e


def calculate_items_priority(items):
    ascii_offset_lower = 97  # ord("a")
    ascii_offset_upper = 65  # ord("A")
    offset_upper = 27
    offset_lower = 1

    priority = 0
    for item in items:
        if item.islower():
            priority += ord(item) - ascii_offset_lower + offset_lower
        if item.isupper():
            priority += ord(item) - ascii_offset_upper + offset_upper
    return priority


class PriorityCalculator:
    def __init__(self, rucksacks):
        self.rucksacks = rucksacks

    def calculate_total_priority(self):
        total_priority = 0
        for rucksack in self.rucksacks:
            assert len(rucksack) % 2 == 0
            middle = int(len(rucksack) // 2)
            left_compartment, right_compartment = rucksack[:middle], rucksack[middle:]
            assert len(left_compartment) == len(right_compartment)

            intersection_compartments = set(left_compartment).intersection(set(right_compartment))
            total_priority += calculate_items_priority(intersection_compartments)
        return total_priority

    def calculate_total_priority_into_group(self):
        total_priority = 0
        assert len(self.rucksacks) % 3 == 0
        groups = [self.rucksacks[i : i + 3] for i in range(0, len(self.rucksacks), 3)]
        for group in groups:
            assert len(group) == 3
            unique_rucksack_items_of_each_elf = list(
                map(lambda rucksack: set(rucksack), group)
            )
            common_items_in_group = unique_rucksack_items_of_each_elf[0].intersection(
                unique_rucksack_items_of_each_elf[1].intersection(
                    unique_rucksack_items_of_each_elf[2]
                )
            )
            total_priority += calculate_items_priority(common_items_in_group)
        return total_priority


if __name__ == "__main__":
    input_lines = read_input()
    print(PriorityCalculator(input_lines).calculate_total_priority())
    print(PriorityCalculator(input_lines).calculate_total_priority_into_group())
