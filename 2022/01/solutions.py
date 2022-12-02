
def part1():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    this_elfs_calories = 0
    calories_per_elf = []
    for line in all_lines:
        if line.strip() == "":
            calories_per_elf.append(this_elfs_calories)
            this_elfs_calories = 0
        else:
            this_elfs_calories = this_elfs_calories + int(line.strip())

    # If we end on a blank line, we're fine. If it's not blank, though,
    # we'll have a non-zero value that we've accumulated for the last elf.
    if this_elfs_calories != 0:
        calories_per_elf.append(this_elfs_calories)

    most_calories = max(calories_per_elf)
    print(f'The elf with the most has {most_calories} calories')
    return calories_per_elf


def part2(calories_per_elf):
    calories_per_elf.sort()
    top3 = sum(calories_per_elf[-3:])
    print(f'The 3 elves with the most calories have {top3} all together')

if __name__ == '__main__':
    calories_per_elf = part1()
    part2(calories_per_elf)
