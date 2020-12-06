#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_data = f.read()

    all_groups = all_data.split('\n\n')

    sums = 0
    for group in all_groups:
        people = group.split('\n')
        people = [set(i) for i in people]

        # If there's only one person in a group, just total up the number
        # of questions they answered yes to. If there are more, get
        # the intersection of all people in the group.
        if len(people) == 1:
            sums = sums + len(people[0])
        else:
            isct = people[0].intersection(*people[1:])
            sums = sums + len(isct)

    print('Sum = {0}'.format(sums))


if __name__ == '__main__':
    main()
