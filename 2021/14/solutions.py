from os import replace
import re


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    template_line = all_lines[0]
    template_line = template_line.strip()

    rules = []
    for line in all_lines[1:]:
        l = line.strip()
        if l == '':
            continue
        
        r = re.match("([a-zA-Z]+) -> ([a-zA-Z]+)", l)
        pair = r.group(1)
        insert = r.group(2)
        rules.append((pair, insert))

    return template_line, rules


def do_one_step(template, rules):
    replacements = []
    for rule in rules:
        pair = rule[0]
        insert = rule[1]

        # We need some lookahead magic here, because there can be overlapping matches.
        # For example, if the pair is 'BB' and the string is 'BBBB', we need to find
        # THREE matches... but without lookahead, it will only find two!
        lookahead_regex = '(?=({0}))'.format(pair)
        positions = [m.start() for m in re.finditer(lookahead_regex, template)]
        
        for p in positions:
            replacements.append((pair, insert, p))
        
    backward = sorted(replacements, key=lambda x: x[2], reverse=True)
    for b in backward:
        insert = b[1]
        idx = b[2] + 1
        tpre = template[:idx]
        tpost = template[idx:]
        next = tpre + insert + tpost
        # print('{0} - {1} - {2}'.format(template, b, next))
        template = next
    
    return template


def solve_a(template, rules, num_steps):
    current = template
    for idx in range(num_steps):
        # print('--- STEP {0} ---'.format(idx))
        current = do_one_step(current, rules)
    
    all_letters = [i for i in current]
    unique_letters = set(all_letters)
    counts = [(ul, current.count(ul)) for ul in unique_letters]
    counts.sort(key=lambda x: x[1])
    most_freq = counts[-1]
    least_freq = counts[0]
    print('{0} - {1} = {2}'.format(most_freq[1], least_freq[1], most_freq[1] - least_freq[1]))


def main():
    template, rules = read_input('./input.txt')
    solve_a(template, rules, 10)


if __name__ == '__main__':
    main()
