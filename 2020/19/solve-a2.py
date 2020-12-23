#!/usr/bin/env python3
def chars_matched_by_sequence(msg, all_rules, sequence):
    accum_offsets = [0]
    offsets_from_previous = list(accum_offsets)
    for seq_idx in range(len(sequence)):
        subrule = sequence[seq_idx]

        offsets_for_next = []
        for offset in offsets_from_previous:
            chars_matched = chars_matched_by_rule(msg[offset:], all_rules, subrule)
            accum_offsets = [i + offset for i in chars_matched]
            offsets_for_next = offsets_for_next + accum_offsets

        offsets_from_previous = offsets_for_next

    return offsets_from_previous


def chars_matched_by_rule(msg, all_rules, rule_key):
    """
    Return a list of integers. This is a list of the number of characters that can be matched
    by various paths of the rule.
    """
    rule = all_rules[rule_key]

    if len(rule) == 1 and len(rule[0]) == 1 and (rule[0][0] == '"a"' or rule[0][0] == '"b"'):
        letter = rule[0][0].strip('"')
        if msg[0] == letter:
            return [1]
        else:
            return [0]

    total_chars_matched = []
    for option in rule:
        ch_matched = chars_matched_by_sequence(msg, all_rules, option)
        total_chars_matched = total_chars_matched + ch_matched

    return total_chars_matched


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
    num_valid = 0
    for msg in msgs:
        chars_matched = chars_matched_by_rule(msg, rules, '0')
        if len(msg) in chars_matched:
            num_valid = num_valid + 1

    print('The number of valid messages is {0}'.format(num_valid))


if __name__ == '__main__':
    #main('./test-rules2.txt', './test-msgs2.txt')
    #main('./test-rules1.txt', './test-msgs1.txt')
    main('./rules.txt', './sample-msgs.txt')
