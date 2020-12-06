#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_data = f.read()

    all_groups = all_data.split('\n\n')

    sums = 0
    for group in all_groups:
        people = group.split('\n')
        all_answers = ''.join(people)
        listified = [i for i in all_answers]
        setified = set(listified)
        sums = sums + len(setified)

    print('Sum = {0}'.format(sums))


if __name__ == '__main__':
    main()
