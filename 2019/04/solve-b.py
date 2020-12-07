#!/usr/bin/env python3
def pwd_is_valid(pwd):
    pwd_str = str(pwd)
    chars = [ch for ch in pwd_str]

    # Check that the numbers in the sequence never DECREASE,
    # and that there is a sequence of EXACTLY two duplicates.
    found_adjacent_dup = False
    found_adjacent_dec = False
    run_length = 1
    for i in range(1, len(chars)):
        if chars[i] < chars[i-1]:
            found_adjacent_dec = True
        
        if chars[i-1] == chars[i]:
            run_length = run_length + 1
        else:
            if run_length == 2:
                found_adjacent_dup = True
            run_length = 1

    # catch the case where the final two digits match
    if run_length == 2:
        found_adjacent_dup = True

    return found_adjacent_dup and not found_adjacent_dec


def main():
    first = 387638
    last = 919123

    valid_pwds = filter(pwd_is_valid, range(first, last+1))
    
    print(len(list(valid_pwds)))


if __name__ == '__main__':
    main()
