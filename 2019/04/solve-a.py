#!/usr/bin/env python3
def pwd_is_valid(pwd):
    pwd_str = str(pwd)
    chars = [ch for ch in pwd_str]

    # Check if two adjacent digits are the same and that the
    # numbers never DECREASE
    found_adjacent_dup = False
    found_adjacent_dec = False
    for i in range(1, len(chars)):
        if chars[i] == chars[i-1]:
            found_adjacent_dup = True
        if chars[i] < chars[i-1]:
            found_adjacent_dec = True

    return found_adjacent_dup and not found_adjacent_dec


def main():
    first = 387638
    last = 919123

    valid_pwds = filter(pwd_is_valid, range(first, last+1))
    
    print(len(list(valid_pwds)))


if __name__ == '__main__':
    main()
