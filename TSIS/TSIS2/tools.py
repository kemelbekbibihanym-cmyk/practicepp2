import pygame
import math
from collections import deque

def flood_fill(surface, x, y, fill_color):
    """Standard BFS Flood Fill to fill closed areas."""
    target = surface.get_at((x, y))[:3]
    fill = tuple(fill_color[:3])
    if target == fill:
        return
    w, h = surface.get_size()
    queue = deque([(x, y)])
    seen = {(x, y)}
    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), fill)
        for nx, ny in ((cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen:
                if surface.get_at((nx, ny))[:3] == target:
                    seen.add((nx, ny))
                    queue.append((nx, ny))

def get_color(color_mode, index_or_diag):
    """Calculates color based on mode. Supports the gradient effect from original code."""
    val = int(index_or_diag)
    c1 = max(0, min(255, val - 256))
    c2 = max(0, min(255, val))
    
    if color_mode == 'red':   return (c2, c1, c1)
    if color_mode == 'green': return (c1, c2, c1)
    if color_mode == 'blue':  return (c1, c1, c2)
    return (0, 0, 0) # Erase/Black

def draw_fig(screen, start, end, width, color_mode, draw_mode):
    """Handles all geometric shapes and straight lines."""
    x1, y1 = start
    x2, y2 = end
    diag = math.hypot(x2 - x1, y2 - y1)
    # Use diag for shapes, except line where we want it thicker
    color = get_color(color_mode, diag / 2)

    if draw_mode == 2: # Rectangle
        pygame.draw.rect(screen, color, (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)), width)
    elif draw_mode == 3: # Circle
        pygame.draw.circle(screen, color, ((x1+x2)//2, (y1+y2)//2), int(diag/2), width)
    elif draw_mode == 4: # Square
        side = min(abs(x2-x1), abs(y2-y1))
        sx = x1 + (side if x2 >= x1 else -side)
        sy = y1 + (side if y2 >= y1 else -side)
        pygame.draw.rect(screen, color, (min(x1, sx), min(y1, sy), side, side), width)
    elif draw_mode == 5: # Right Triangle
        pygame.draw.polygon(screen, color, [(x1, y2), (x1, y1), (x2, y2)], width)
    elif draw_mode == 6: # Equilateral Triangle
        base = abs(x2 - x1)
        height = (math.sqrt(3)/2) * base
        apex_y = y2 - height if y1 <= y2 else y2 + height
        pygame.draw.polygon(screen, color, [(x1, y2), (x2, y2), ((x1+x2)/2, apex_y)], width)
    elif draw_mode == 7: # Rhombus
        mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
        pygame.draw.polygon(screen, color, [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)], width)
    elif draw_mode == 8: # Straight Line
        pygame.draw.line(screen, color, start, end, max(1, width * 2))

def draw_line_between(screen, index, start, end, width, color_mode):
    """Freehand drawing using circle stamping for smoothness."""
    color = get_color(color_mode, 2 * index)
    dx, dy = end[0] - start[0], end[1] - start[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = i / max(iterations, 1)
        x = int(start[0] + progress * dx)
        y = int(start[1] + progress * dy)
        pygame.draw.circle(screen, color, (x, y), width)