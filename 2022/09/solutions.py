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


def update_follower(updated_leader, current_follower):
    dx = updated_leader[0] - current_follower[0]
    dy = updated_leader[1] - current_follower[1]

    # If it's 1 unit or fewer away in both x and y, then it doesn't move
    if abs(dx) <= 1 and abs(dy) <= 1:
        return current_follower

    # If it's farther than that (i.e., if either dx or dy is >= 2), we need
    # to move one space in any direction, including diagonals, to get closer. 

    # Move one space closer along any axis for which dx or dy is > 0..
    x_move = 0
    y_move = 0

    if dx > 0:
        x_move = 1
    elif dx < 0:
        x_move = -1

    if dy > 0:
        y_move = 1
    elif dy < 0:
        y_move = -1

    return (current_follower[0] + x_move, current_follower[1] + y_move)


def simulate(num_segments):
    with open('input.txt', 'r') as f:
        all_lines = f.readlines()

    starting_pos = (0, 0)
    body_segment_pos = [starting_pos] * num_segments

    visited = set()
    visited.add(body_segment_pos[-1])
    
    for line in all_lines:
        line = line.strip()
        parts = line.split(' ')
        direction = parts[0]
        steps = int(parts[1])

        for _ in range(steps):
            body_segment_pos[0] = update_head(body_segment_pos[0], direction)

            for idx in range(1, num_segments):
                leader = body_segment_pos[idx - 1]
                body_segment_pos[idx] = update_follower(leader, body_segment_pos[idx])

            visited.add(body_segment_pos[-1])

    print(f'The tail visited {len(visited)} places')


if __name__ == '__main__':
    simulate(2)
    simulate(10)
