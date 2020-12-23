#!/usr/bin/env python3
import re


def build_rules_regex(all_rules, rule_key):
    """
    Build a gigantic regex string based on the rules provided as a dictionary
    """
    rule = all_rules[rule_key]

    # If the rule is just the a or b, then the regex string is just a or b.
    if len(rule) == 1 and len(rule[0]) == 1 and rule[0][0] in ('a', 'b'):
        return rule[0][0]

    # If there are subrules, then we build them recursively.
    option_strs = []

    # Loop over options. Build a regex string for each one and collect them in option_strs
    for option in rule:
        option_str = ''
        for subrule in option:
            sub_regex = build_rules_regex(all_rules, subrule)
            option_str = option_str + sub_regex
        option_strs.append(option_str)

    # If there are multiple options, separate them with a pipe
    option_strs_as_regex = '|'.join(option_strs)

    # Anything more complicated than an a or b are grouped with parentheses
    final_regex = '(' + option_strs_as_regex + ')'
    return final_regex


def parse_rules(rule_list):
    rule_dict = {}
    for rule in rule_list:
        s = rule.split(':')
        k = s[0]

        v = s[1]
        v = v.strip()
        v = v.strip('"')
        v = v.split('|')
        v = [i.strip() for i in v]
        v = [i.split(' ') for i in v]

        rule_dict[k] = v

    return rule_dict


def main(rule_file, msg_file):
    with open(rule_file, 'r') as f:
        all_lines = f.readlines()

    all_rules = [r.strip() for r in all_lines]
    rules = parse_rules(all_rules)
    rules_regex_str = build_rules_regex(rules, '0')

    with open(msg_file, 'r') as f:
        all_lines = f.readlines()

    msgs = [m.strip() for m in all_lines]
    valid_msgs = filter(lambda msg: re.fullmatch(rules_regex_str, msg) is not None, msgs)
    num_valid = len(list(valid_msgs))

    print('The number of valid messages is {0}'.format(num_valid))


if __name__ == '__main__':
    #main('./test-rules2.txt', './test-msgs2.txt')
    #main('./test-rules1.txt', './test-msgs1.txt')
    main('./rules.txt', './sample-msgs.txt')
