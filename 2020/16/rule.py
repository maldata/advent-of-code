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

    @property
    def name(self):
        return self._name

    def is_valid(self, value):
        return (self._range1lo <= value <= self._range1hi) or \
            (self._range2lo <= value <= self._range2hi)
