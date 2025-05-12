import sys
from collections import deque

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    return [list(line.strip()) for line in sys.stdin if line.strip()]


def solve(data):
    if not data:
        return -1

    rows, cols = len(data), len(data[0])
    robots = []
    key_positions = {}
    all_keys = 0

    # Находим роботов и ключи (сохраняем оригинальную логику)
    for i in range(rows):
        for j in range(cols):
            c = data[i][j]
            if c == '@':
                robots.append((i, j))
            elif c in keys_char:
                key_positions[c] = (i, j)
                all_keys |= 1 << (ord(c) - ord('a'))

    if not key_positions:
        return 0

    while len(robots) < 4:
        robots.append((-1, -1))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = {}
    queue = deque([(tuple(robots), 0, 0)])

    while queue:
        positions, mask, steps = queue.popleft()

        if mask == all_keys:
            return steps

        for robot_idx in range(4):
            r, c = positions[robot_idx]
            if r == -1:  # Неактивный робот
                continue

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    cell = data[nr][nc]

                    if cell == '#':
                        continue

                    if cell in doors_char:
                        key_needed = 1 << (ord(cell.lower()) - ord('a'))
                        if not (mask & key_needed):
                            continue

                    new_positions = list(positions)
                    new_positions[robot_idx] = (nr, nc)
                    new_positions_tuple = tuple(new_positions)

                    new_mask = mask
                    if cell in keys_char:
                        new_mask |= 1 << (ord(cell) - ord('a'))

                    if (new_positions_tuple, new_mask) not in visited:
                        visited[(new_positions_tuple, new_mask)] = True
                        queue.append((new_positions_tuple, new_mask, steps + 1))

    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()