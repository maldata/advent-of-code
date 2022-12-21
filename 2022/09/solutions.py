def update_head(head, direction):
    dx = 0
    dy = 0
    
    if direction == 'L':
        dx = -1
    elif direction == 'R':
        dx = 1
    elif direction == 'U':
        dy = 1
    elif direction == 'D':
        dy = -1
    else:
        print('Bad direction!')

    return (head[0] + dx, head[1] + dy)


def update_tail(new_head, current_tail):
    dx = new_head[0] - current_tail[0]
    dy = new_head[1] - current_tail[1]

    if abs(dx) <= 1 and abs(dy) <= 1:
        return current_tail

    if dx > 1:
        dx = 1
        dy = 0
    elif dx < -1:
        dx = -1
        dy = 0
    elif dy > 1:
        dx = 0
        dy = 1
    elif dy < 1:
        dx = 0
        dy = -1
    else:
        print('Oof. Something weird.')

    return (new_head[0] - dx, new_head[1] - dy)
    

def part1():
    with open('input.txt', 'r') as f:
        all_lines = f.readlines()

    head_pos = (0, 0)
    tail_pos = (0, 0)
    visited = set()
    visited.add(tail_pos)
    
    for line in all_lines:
        line = line.strip()
        parts = line.split(' ')
        direction = parts[0]
        steps = int(parts[1])

        for step in range(steps):
            new_head = update_head(head_pos, direction)
            new_tail = update_tail(new_head, tail_pos)

            visited.add(new_tail)

            head_pos = new_head
            tail_pos = new_tail

    print(f'The tail visited {len(visited)} places')


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
