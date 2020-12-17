#!/usr/bin/env python3
import re

class Rule:
    def __init__(self, name, range1_lo, range1_hi, range2_lo, range2_hi):
        self.name = name
        self.range1_lo = int(range1_lo)
        self.range1_hi = int(range1_hi)
        self.range2_lo = int(range2_lo)
        self.range2_hi = int(range2_hi)

    def get_invalid_fields(self, ticket):
        invalid_fields = []
        for field in ticket:
            if self.range1_lo <= field <= self.range1_hi or \
               self.range2_lo <= field <= self.range2_hi:
                continue
            else:
                invalid_fields.append(field)

        return invalid_fields

    def all_values_pass(self, field_samples):
        results = [self.range1_lo <= field <= self.range1_hi or self.range2_lo <= field <= self.range2_hi for field in field_samples]
        return all(results)
    

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

    rules = [i.strip() for i in all_lines]
    output = []
    for rule in rules:
        r = re.search('^(.*): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', rule)
        if r is None or len(r.groups()) != 5:
            print('Invalid rule line: {0}'.format(rule))

        name = r.group(1)
        range1lo = r.group(2)
        range1hi = r.group(3)
        range2lo = r.group(4)
        range2hi = r.group(5)
        output.append(Rule(name, range1lo, range1hi, range2lo, range2hi))

    return output


def ticket_errors(ticket, rule_set):
    inv_field_set = None
    for rule in rule_set:
        inv_fields_for_this_rule = set(rule.get_invalid_fields(ticket))
        if inv_field_set is None:
            inv_field_set = inv_fields_for_this_rule
        else:
            inv_field_set = inv_field_set.intersection(inv_fields_for_this_rule)

    return list(inv_field_set)


def main():
    sample_tickets = read_sample_tickets()
    my_ticket = read_my_ticket()
    rule_set = read_rules()

    valid_tickets = []
    for t in sample_tickets:
        if len(ticket_errors(t, rule_set)) == 0:
            valid_tickets.append(t)

    print('Order of fields:')
    transposed_fields = list(zip(*valid_tickets))
    field_order = []
    field_lookup = {}
    for field_list in transposed_fields:
        print('------------------')
        num_matching_fields = 0
        matching_fields = []
        for rule in rule_set:
            if rule.all_values_pass(field_list):
                num_matching_fields = num_matching_fields + 1
                matching_fields.append(rule.name)
                print(rule.name)
        field_lookup[num_matching_fields - 1] = matching_fields
        field_order.append(num_matching_fields)
        
    # This could be more clear, but I want to go to bed, so this
    # is what's happening. Examine the output and you'll see where
    # this comes from.
    ordered_field_names = []
    for idx in range(len(my_ticket)):
        possible_fields = field_lookup[idx]
        for pf in possible_fields:
            if pf not in ordered_field_names:
                ordered_field_names.append(pf)

    for idx in range(len(ordered_field_names)):
        print('{0} - {1}'.format(ordered_field_names[idx], my_ticket[idx]))
                    
    
if __name__ == '__main__':
    main()
