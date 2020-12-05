#!/usr/bin/env python3
import re


def all_fields_present(pp):
    # Note that country ID is NOT required
    return 'byr' in pp and 'iyr' in pp and 'eyr' in pp and 'hgt' in pp \
        and 'hcl' in pp and 'ecl' in pp and 'pid' in pp


def year_ok(pp, string, low, high):
    if string not in pp:
        return False

    value = pp[string]

    try:
        year = int(value)
    except ValueError:
        return False

    return year >= low and year <= high


def birth_year_ok(pp):
    return year_ok(pp, 'byr', 1920, 2002)


def issue_year_ok(pp):
    return year_ok(pp, 'iyr', 2010, 2020)


def expiration_year_ok(pp):
    return year_ok(pp, 'eyr', 2020, 2030)


def height_ok(pp):
    if 'hgt' not in pp:
        return False
    
    hgt = pp['hgt']

    # Needs units, either 'cm' or 'in'. If there are fewer than 3 characters,
    # then we can't have both a number and a unit, so fail.
    if len(hgt) < 3:
        return False

    unit = hgt[-2:]
    if unit == 'cm':
        low = 150
        high = 193
    elif unit == 'in':
        low = 59
        high = 76
    else:
        # Not a valid unit
        return False

    meas_str = hgt[:-2]
    try:
        meas = int(meas_str)
    except ValueError:
        return False
    
    return meas >= low and meas <= high


def hair_color(pp):
    if 'hcl' not in pp:
        return False

    hcl = pp['hcl']
    if len(hcl) != 7:
        return False

    result = re.match('', hcl)
    return result is not None


def country_id_ok(pp):
    return True


def passport_valid(pp):
    return birth_year_ok(pp) \
        and issue_year_ok(pp) \
        and expiration_year_ok(pp) \
        and height_ok(pp) \
        and hair_color_ok(pp) \
        and eye_color_ok(pp) \
        and passport_id_ok(pp) \
        and country_id_ok(pp)


def main():
    with open('./input.txt', 'r') as f:
        all_data = f.read()

    parsed_passports = []
    valid_passports = 0
    raw_passports = all_data.split('\n\n')
    for raw_passport in raw_passports:
        raw_passport = raw_passport.replace(' ', '\n')
        exploded = raw_passport.split()

        d = {}
        for element in exploded:
            kv = element.split(':')
            d[kv[0]] = kv[1]

        parsed_passports.append(d)

        if passport_valid(d):
            valid_passports = valid_passports + 1

    print('There are {0} valid passports.'.format(valid_passports))
    

if __name__ == '__main__':
    main()
