# coding=utf-8

if __name__ == "__main__":
    elves_calories = []

    input_calories = [line.strip() for line in open('input.txt').read().split("\n\n")]

    for elf_calories in input_calories:
        current_elf_calories = sum(int(calories) for calories in elf_calories.split('\n'))
        elves_calories.append(current_elf_calories)

    elves_calories.sort(reverse=True)

    print(elves_calories[0], sum(elves_calories[:3]))
