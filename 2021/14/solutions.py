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


def do_one_step_b(counts, rules):
    new_counts = {}
    for r in rules:
        pair = r[0]
        insert = r[1]
        first_char = pair[0]
        second_char = pair[1]
        new_pair1 = first_char + insert
        new_pair2 = insert + second_char

        # If this pair isn't in the dictionary at all, just move on
        if pair not in counts or counts[pair] == 0:
            continue

        # Otherwise, we add that many counts of the two new pairs
        num_old_pair = counts[pair]
        if new_pair1 in new_counts:
            new_counts[new_pair1] = new_counts[new_pair1] + num_old_pair
        else:
            new_counts[new_pair1] = num_old_pair
        
        if new_pair2 in new_counts:
            new_counts[new_pair2] = new_counts[new_pair2] + num_old_pair
        else:
            new_counts[new_pair2] = num_old_pair

    return new_counts

def solve_b(template, rules, num_steps):
    exploded = [t for t in template]
    pairs = zip(exploded[:-1], exploded[1:])

    counts = {}
    for p in pairs:
        string_pair = p[0] + p[1]
        if string_pair in counts:
            counts[string_pair] = counts[string_pair] + 1
        else:
            counts[string_pair] = 1
    
    for step_idx in range(num_steps):
        counts = do_one_step_b(counts, rules)

    letter_counts = {}
    for letter_pair in counts:
        num_counts = counts[letter_pair]
        for letter in letter_pair:
            if letter in letter_counts:
                letter_counts[letter] = letter_counts[letter] + num_counts
            else:
                letter_counts[letter] = num_counts
    
    # The first and last letters in the template don't get double-counted
    # in the pairs, so we'll add one to each, then divide all of them by two.
    for end in [exploded[0], exploded[-1]]:
        letter_counts[end] = letter_counts[end] + 1
    
    min_letter = None
    max_letter = None
    for k in letter_counts:
        letter_counts[k] = letter_counts[k] // 2
        if min_letter is None or letter_counts[k] < min_letter:
            min_letter = letter_counts[k]
        if max_letter is None or letter_counts[k] > max_letter:
            max_letter = letter_counts[k]

    print('{0} - {1} = {2}'.format(max_letter, min_letter, max_letter - min_letter))


def main():
    template, rules = read_input('./input.txt')
    solve_a(template, rules, 10)
    solve_b(template, rules, 40)


if __name__ == '__main__':
    main()
