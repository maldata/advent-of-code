#!/usr/bin/env python3
def evaluate_subrules(msg, all_rules, sub_rules):
    if len(sub_rules) == 1:
        letter = sub_rules[0]
        letter = letter.strip('"')
        return msg[0] == letter, 1

    matched = False
    unmatched_portion = msg
    matched_portion = ''
    for sub_rule in sub_rules:
        matched, index = rule_matches(unmatched_portion, all_rules, sub_rule)
        if not matched:
            break
        part1 = unmatched_portion[0:index]
        part2 = unmatched_portion[index:]
        matched_portion = matched_portion + part1
        unmatched_portion = part2

    return matched, len(matched_portion)


def rule_matches(msg, all_rules, rule_key):
    """
    Return a boolean indicating if the rule matches, along with the index of the split
    """
    rule = all_rules[rule_key]

    for option in rule:
        result, index = evaluate_subrules(msg, all_rules, option)
        if result:
            return True, index

    return False, 0


def parse_rules(rule_list):
    rule_dict = {}
    for rule in rule_list:
        s = rule.split(':')
        k = s[0]

        v = s[1]
        v = v.strip()
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

    with open(msg_file, 'r') as f:
        all_lines = f.readlines()

    msgs = [m.strip() for m in all_lines]
    results = [rule_matches(msg, rules, '0') for msg in msgs]
    passed = filter(lambda x: x[0], results)

    print('The number of valid messages is {0}'.format(len(list(passed))))


if __name__ == '__main__':
    #main('./test-rules1.txt', './test-msgs1.txt')
    main('./rules.txt', './sample-msgs.txt')
