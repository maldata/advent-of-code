import re

def read_input(file_path):
    with open(file_path, 'r') as f:
        all_data = f.read()
    
    all_data = all_data.strip()
    m = re.search('x=(-*[0-9]+)..(-*[0-9]+), y=(-*[0-9]+)..(-*[0-9]+)', all_data)
    if m:
        xmin = m.group(1)
        xmax = m.group(2)
        ymin = m.group(3)
        ymax = m.group(4)
    
    return (int(xmin), int(xmax), int(ymin), int(ymax))


def single_step(x0, y0, vx0, vy0):
    xf = x0 + vx0
    yf = y0 + vy0
    if vx0 == 0:
        vxf = 0
    elif vx0 > 0:
        vxf = vx0 - 1
    else:
        vxf = vx0 + 1
    vyf = vy0 - 1

    return xf, yf, vxf, vyf


def simulate(v0, limits):
    xmin = limits[0]
    xmax = limits[1]
    ymin = limits[2]
    ymax = limits[3]

    x = 0
    y = 0
    vx = v0[0]
    vy = v0[1]

    peak_y = y
    while True:
        x, y, vx, vy = single_step(x, y, vx, vy)
        peak_y = max([y, peak_y])

        # If we're inside the limits, return the peak y value
        if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
            print('{0} -> {1}'.format(v0, peak_y))
            return peak_y
        
        # If we fall under the minimum y value or we blow past the maximum x value
        # and we're still not in the target limits, then there's no hope of us ever
        # getting in there, so just bail out and return None.
        if y < ymin or x > xmax:
            return None


def solve_a(limits):
    biggest_peak_y = 0
    velocities = [(x, y) for x in range(0, 50) for y in range(0, 300)]
    for v in velocities:
        result = simulate(v, limits)
        if result:
            biggest_peak_y = max([result, biggest_peak_y])
    
    print('Largest y peak is {0}'.format(biggest_peak_y))


def solve_b(limits):
    num_hits = 0
    velocities = [(x, y) for x in range(0, 70) for y in range(-250, 1750)]
    for v in velocities:
        result = simulate(v, limits)
        if result:
            num_hits = num_hits + 1
    
    print('Found {0} hits'.format(num_hits))


def main():
    limits = read_input('./input.txt')
    solve_a(limits)
    solve_b(limits)


if __name__ == '__main__':
    main()
