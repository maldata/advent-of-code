#!/usr/bin/env python3
def passport_valid(pp):
    return 'byr' in pp and 'iyr' in pp and 'eyr' in pp and 'hgt' in pp \
        and 'hcl' in pp and 'ecl' in pp and 'pid' in pp


def main():
    with open('./input.txt', 'r') as f:
        all_data = f.read()

    valid_passports = 0
    raw_passports = all_data.split('\n\n')
    for raw_passport in raw_passports:
        raw_passport = raw_passport.replace(' ', '\n')
        exploded = raw_passport.split()

        d = {}
        for element in exploded:
            kv = element.split(':')
            d[kv[0]] = kv[1]

        if passport_valid(d):
            valid_passports = valid_passports + 1

    print('There are {0} valid passports.'.format(valid_passports))
    

if __name__ == '__main__':
    main()
