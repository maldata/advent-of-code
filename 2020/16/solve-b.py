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

    print('We now have a list of valid tickets.')

    # Transpose the valid_tickets so that instead of each inner list being a
    # ticket, each inner list is every sample of a single field.
    transposed_fields = list(zip(*valid_tickets))
    transposed_fields_removed = [False for t in transposed_fields]

    # We want to pick a rule and test it on every set of samples in the list.
    # If only one sample set works, we lock it in and associate it with that rule.
    rule_key_list = list(rule_dict)
    num_rules = len(rule_dict)
    cemented_rules = 0
    index = 0
    while cemented_rules < num_rules:
        # Get a rule
        current_rule_key = rule_key_list[index]
        current_rule = rule_dict[current_rule_key]
        
        # If that rule isn't cemented, figure out how many of the field sets are valid
        if not current_rule.is_cemented:
            print('current_rule: {0}'.format(current_rule.name))
            num_all_valid = 0
            cached_index = 0
            for sample_list_idx in range(len(transposed_fields)):
                # Skip it if this field has already been cemented
                if transposed_fields_removed[sample_list_idx]:
                    continue
                
                samples = transposed_fields[sample_list_idx]
                if current_rule.all_samples_valid(samples):
                    num_all_valid = num_all_valid + 1
                    cached_index = sample_list_idx

            print('For rule {0}, there are {1} valid fields'.format(current_rule.name, num_all_valid))
            if num_all_valid == 1:
                transposed_fields_removed[cached_index] = True
                current_rule.cement(cached_index)
                cemented_rules = cemented_rules + 1
                print('got one... {0} is {1}'.format(current_rule.name, cached_index))

        # Cycle to the next rule. Keep going until they're all set.
        index = index + 1
        index = index % num_rules
    
    print()
    print('MY TICKET:')
    print(my_ticket)

    for rule_key in rule_dict:
        current_rule = rule_dict[rule_key]
        print('{0} - {1}'.format(current_rule.cemented_field, current_rule.name))

    departure_keys = ['departure location',
                      'departure station',
                      'departure platform',
                      'departure track',
                      'departure date',
                      'departure time']

    product = 1
    for k in departure_keys:
        r = rule_dict[k]
        field = r.cemented_field
        product = product * my_ticket[field]

    print('Final answer: {0}'.format(product))
    

if __name__ == '__main__':
    main()
