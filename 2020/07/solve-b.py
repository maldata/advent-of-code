#!/usr/bin/env python3
import re


def parse_rule(rule):
    """
    Given a rule (in text), parse it and return the type of bag and a dictionary of what can
    be placed in that bag
    """
    m = re.match('^([a-z\s]+) bags contain (.*)\.$', rule)

    if m is None or len(m.groups()) != 2:
        return None, None

    bag = m.group(1)
    contents = m.group(2)

    contents = contents.split(',')

    bag_contents = {}
    for sub_bag in contents:
        sub_bag = sub_bag.strip()
        s = re.match('^([0-9]+) (.*) bags*$', sub_bag)

        if s and len(s.groups()) == 2:
            bag_contents[s.group(2)] = int(s.group(1))

    return bag, bag_contents


def get_number_of_inner_bags(rules, target_bag):
    sub_bags = rules[target_bag]

    if len(sub_bags) == 0:
        return 0

    total = 0
    for sub_bag in sub_bags:
        quantity = sub_bags[sub_bag]
        total = total + quantity
        total = total + (quantity * get_number_of_inner_bags(rules, sub_bag))

    return total

def main():
    with open('input.txt', 'r') as f:
        all_input_lines = f.readlines()

    all_rules = [i.strip() for i in all_input_lines]

    # light red bags contain 2 clear indigo bags, 3 light lime bags.
    raw_rules = {}
    for rule in all_rules:
        bag, bag_contents = parse_rule(rule)

        if bag in raw_rules:
            print('Can\'t have another rule for {0} bags!'.format(bag))
            break
        raw_rules[bag] = bag_contents

    target_bag = 'shiny gold'
    num_inner = get_number_of_inner_bags(raw_rules, target_bag)

    print('A {0} bag contains {1} inner bags.'.format(target_bag, num_inner))


if __name__ == '__main__':
    main()
