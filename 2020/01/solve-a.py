#!/usr/bin/env python3

def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_values = [int(i.strip()) for i in all_lines]

    found = False
    for v in all_values:
        complement = 2020 - v
        if complement in all_values:
            found = True
            break

    if not found:
        print('Something went horribly wrong.')
    else:
        print('{0} * {1} = {2}'.format(v, complement, v * complement))
    

if __name__ == '__main__':
    main()
    
