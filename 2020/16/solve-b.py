#!/usr/bin/env python3
import re

from rule import Rule


def read_sample_tickets():
    with open('./sample-tickets.txt', 'r') as f:
        all_lines = f.readlines()
        
    sample_tickets = [i.strip() for i in all_lines]
    sample_tickets = [i.split(',') for i in sample_tickets]
    return [list(map(int, i)) for i in sample_tickets]


def read_my_ticket():
    with open('./my-ticket.txt', 'r') as f:
        all_lines = f.readlines()

    return [int(i.strip()) for i in all_lines[0].split(',')]


def read_rules():
    with open('./rules.txt', 'r') as f:
        all_lines = f.readlines()

    rule_strs = [i.strip() for i in all_lines]
    rules = {}
    for rule_str in rule_strs:
        r = Rule(rule_str)
        rules[r.name] = r
    
    return rules


def ticket_errors(ticket, rule_dict):
    inv_field_set = None
    for rule_name in rule_dict:
        rule = rule_dict[rule_name]
        inv_fields_for_this_rule = set(rule.get_invalid_fields(ticket))
        if inv_field_set is None:
            inv_field_set = inv_fields_for_this_rule
        else:
            inv_field_set = inv_field_set.intersection(inv_fields_for_this_rule)

    return list(inv_field_set)


def main():
    sample_tickets = read_sample_tickets()
    my_ticket = read_my_ticket()
    rule_dict = read_rules()

    valid_tickets = []
    for t in sample_tickets:
        if len(ticket_errors(t, rule_dict)) == 0:
            valid_tickets.append(t)

    # We now have a list of valid tickets.

    # Transpose the valid_tickets so that instead of each inner list being a ticket,
    # each inner list is every sample of a single field.
    transposed_fields = list(zip(*valid_tickets))
    field_order = []
    field_lookup = {}

    for samples_of_single_field in transposed_fields:
        print('------------------')
        print('SAMPLES: {0}'.format(samples_of_single_field))
        num_matching_rules = 0
        matching_rules = []
        for rule_name in rule_dict:
            rule = rule_dict[rule_name]
            if all([rule.is_valid(s) for s in samples_of_single_field]):
                num_matching_rules = num_matching_rules + 1
                matching_rules.append(rule_name)
                print(rule_name)

        if num_matching_rules == 1:
            matching_rule_name = matching_rules[0]
            rule = rule_dict[matching_rule_name]
            rule.cement()

        field_lookup[num_matching_rules - 1] = matching_rules
        field_order.append(num_matching_rules)
        
    # This could be more clear, but I want to go to bed, so this
    # is what's happening. Examine the output and you'll see where
    # this comes from.
    ordered_field_names = []
    for idx in range(len(my_ticket)):
        possible_fields = field_lookup[idx]
        for pf in possible_fields:
            if pf not in ordered_field_names:
                ordered_field_names.append(pf)

    print()
    print('MY TICKET:')
    print(my_ticket)
    for idx in range(len(ordered_field_names)):
        print('{0} - {1}'.format(ordered_field_names[idx], my_ticket[idx]))

    # Quick double-check...
    for rule_name in rule_dict:
        rule_name.get_invalid_fields(my_ticket)


if __name__ == '__main__':
    main()
