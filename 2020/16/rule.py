import re


class Rule:
    def __init__(self, rule_str):
        r = re.search('^(.*): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', rule_str)
        if r is None or len(r.groups()) != 5:
            print('Invalid rule line: {0}'.format(rule_str))
        
        self._name = r.group(1)
        self._range1lo = int(r.group(2))
        self._range1hi = int(r.group(3))
        self._range2lo = int(r.group(4))
        self._range2hi = int(r.group(5))

        self._cemented_field = None

    @property
    def name(self):
        return self._name

    @property
    def cemented_field(self):
        return self._cemented_field

    def is_valid(self, value):
        """ Checks if a single integer is valid for this rule """
        return (self._range1lo <= value <= self._range1hi) or \
            (self._range2lo <= value <= self._range2hi)

    def get_valid_fields(self, ticket):
        """
        Returns a list of indices of fields in the given
        ticket that ARE valid for this rule.
        """
        return [i for i in range(len(ticket)) if self.is_valid(ticket[i])]

    def get_invalid_fields(self, ticket):
        """ 
        Returns a list of indices of fields in the given 
        ticket that ARE NOT valid for this rule.
        """
        return [i for i in range(len(ticket)) if not self.is_valid(ticket[i])]

    def cement(self, field):
        if self._cemented_field is None:
            self._cemented_field = field
        else:
            msg_template = 'This rule ({0}) is already associated with field {1}'
            print(msg_template.format(self.name, self._cemented_field))
