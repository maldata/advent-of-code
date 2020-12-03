#!/usr/bin/env python3

def find_pair(available, target_sum):
    listified = list(available)
    if len(listified) == 0:
        return (None, None, False)

    found = False
    for v in listified:
        complement = target_sum - v
        if complement in listified:
            found = True
            break
    return (v, complement, found)

def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_values = [int(i.strip()) for i in all_lines]

    triplet_found = False
    for v in all_values:
        remainder = 2020 - v
        smaller_values = filter(lambda x: x < remainder, all_values)
        a, b, pair_found = find_pair(smaller_values, remainder)

        if pair_found:
            print('{0} + {1} + {2} = {3}'.format(a, b, v, a + b + v))
            print('{0} * {1} * {2} = {3}'.format(a, b, v, a * b * v))
            triplet_found = True
            break

    if not triplet_found:
        print('Something went horribly wrong.')
    

if __name__ == '__main__':
    main()
    
