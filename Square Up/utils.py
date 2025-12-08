# utils.py
import math
import collections
import config

# ==========================================
# MATH UTILITIES
# ==========================================

def clamp(v, min_v, max_v):
    return max(min_v, min(max_v, v))

def distance(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

def check_grid_collision(wx, wy, grid):
    """Returns True if the point (wx, wy) is inside a wall."""
    ix = int(wx)
    iy = int(wy)
    # Check boundaries
    if ix < 0 or ix >= len(grid[0]) or iy < 0 or iy >= len(grid):
        return True
    # Check wall tile
    if grid[iy][ix] == 1:
        return True
    return False

def has_line_of_sight(x1, y1, x2, y2, grid):
    """Raycast to check if two points can see each other."""
    dist = math.hypot(x2 - x1, y2 - y1)
    # Check every 0.5 world units
    steps = int(dist * 2)
    if steps < 1:
        return True

    for i in range(1, steps + 1):
        t = i / steps
        cx = x1 + (x2 - x1) * t
        cy = y1 + (y2 - y1) * t
        if check_grid_collision(cx, cy, grid):
            return False
    return True

# ==========================================
# PATHFINDING (BFS)
# ==========================================
def get_path_bfs(start, end, grid):
    w = len(grid[0])
    h = len(grid)

    if start == end:
        return []

    queue = collections.deque([start])
    came_from = {start: None}
    found = False

    # Directions: Up, Down, Left, Right
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    iterations = 0
    max_iter = 400

    while queue:
        current = queue.popleft()
        iterations += 1
        if iterations > max_iter:
            break

        if current == end:
            found = True
            break

        for dx, dy in neighbors:
            nx, ny = current[0] + dx, current[1] + dy

            if 0 <= nx < w and 0 <= ny < h:
                if grid[ny][nx] == 0: # 0 is walkable
                    next_node = (nx, ny)
                    if next_node not in came_from:
                        queue.append(next_node)
                        came_from[next_node] = current

    if found:
        path = []
        curr = end
        while curr != start:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path
    return []