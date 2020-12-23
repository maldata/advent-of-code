#!/usr/bin/env python3
import re


def build_rules_regex_core(all_rules, rule_key, depth):
    """
    Build a gigantic regex string based on the rules provided as a dictionary
    There are loops now, so we need to cap the recursion depth. If we hit the
    limit (which I have set arbitrarily), just return a bogus regex that won't
    hurt anything at higher levels.
    """
    if depth >= 100:
        return ''

    rule = all_rules[rule_key]

    # If the rule is just the a or b (no options, no subrules), then the regex string is just a or b.
    if len(rule) == 1 and len(rule[0]) == 1 and rule[0][0] in ('a', 'b'):
        return rule[0][0]

    # If there are subrules, then we build them recursively. Loop over all options.
    # Build a regex string for each one and collect them in option_strs
    option_strs = []
    for option in rule:
        option_str = ''
        for subrule in option:
            sub_regex = build_rules_regex_core(all_rules, subrule, depth + 1)
            option_str = option_str + sub_regex
        option_strs.append(option_str)

    # Join the option strings with a pipe so the regex will match either one of them
    option_strs_as_regex = '|'.join(option_strs)

    # Group it all together with parentheses
    final_regex = '(' + option_strs_as_regex + ')'
    return final_regex


def build_rules_regex(all_rules, rule_key):
    return build_rules_regex_core(all_rules, rule_key, 0)


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

    # Completely replace rules 8 and 11 with:
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]

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
