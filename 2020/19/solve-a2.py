#!/usr/bin/env python3
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


def expand(all_rules, rule_key):
    rule = all_rules[rule_key]
    for option in rule:



def main(rule_file, msg_file):
    with open(rule_file, 'r') as f:
        all_lines = f.readlines()

    all_rules = [r.strip() for r in all_lines]
    rules = parse_rules(all_rules)

    with open(msg_file, 'r') as f:
        all_lines = f.readlines()

    expand(rules, '0')

#    msgs = [m.strip() for m in all_lines]
#    results = [rule_matches(msg, rules, '0') for msg in msgs]
#    passed = filter(lambda x: x[0], results)

    print('The number of valid messages is {0}'.format(len(list(passed))))


if __name__ == '__main__':
    main('./test-rules1.txt', './test-msgs1.txt')
    #main('./rules.txt', './sample-msgs.txt')
