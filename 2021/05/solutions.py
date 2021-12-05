import re


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    line_definitions = []
    for line in all_lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        m = re.match('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)', line)
        if m is None:
            print("A line doesn't match the regex!: ")
            return

        line_definitions.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    
    return line_definitions

def main():
    line_definitions = read_input('./input.txt')
    pass

if __name__ == '__main__':
    main()
