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


def can_contain(rules, bag_type, target_bag):
    """
    Returns True if the given bag_type can contain the target bag (recursively)
    """
    # get a list of bags that CAN go in this bag_type
    valid_bags = list(rules[bag_type])

    if len(valid_bags) == 0:
        return False

    if target_bag in valid_bags:
        return True
    else:
        target_in_sub_bag = [can_contain(rules, b, target_bag) for b in valid_bags]
        return any(target_in_sub_bag)


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

    # We're looking to see how many bag types can contain (at some level) the target bag
    target_bag = 'shiny gold'
    num_valid_containers = 0
    for bag_type in raw_rules:
        if bag_type == target_bag:
            continue
        else:
            if can_contain(raw_rules, bag_type, target_bag):
                num_valid_containers = num_valid_containers + 1

    print('There are {0} valid containing bags for a {1} bag.'.format(num_valid_containers, target_bag))


if __name__ == '__main__':
    main()
