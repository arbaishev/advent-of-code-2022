# coding=utf-8
from typing import List


def read_input() -> List[str]:
    input_file_name = "input.txt"

    try:
        with open(input_file_name) as input_file:
            input_lines = input_file.read()
            if not input_lines:
                raise Exception(f"File {input_file_name} is empty")
            return [line.strip() for line in input_lines.split("\n\n")]
    except EnvironmentError as e:
        raise Exception(f"File {input_file} is missing or invalid") from e


class Elf:
    def __init__(self, inventory: List[int]):
        self.carried_food = inventory

    def carried_calories(self) -> int:
        return sum(self.carried_food)


class Expedition:
    def __init__(self):
        self.members = []
        self.calculated_members = {}

    def create(self, provided_calories_list: List[str]) -> None:
        self.members = [
            Elf(list(map(int, provision_calories.split("\n"))))
            for provision_calories in provided_calories_list
        ]
        self.calculated_members = {elf: elf.carried_calories() for elf in self.members}

    def find_elf_carried_most_calories(self) -> int:
        return self.calculated_members[max(self.calculated_members, key=self.calculated_members.get)]


if __name__ == "__main__":
    input_lines = read_input()

    expedition = Expedition()
    expedition.create(input_lines)
    print(expedition.find_elf_carried_most_calories())
