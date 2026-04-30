import pygame
import datetime
import tools # Imports the tools.py file created above

def main():
    pygame.init()
    WIDTH, HEIGHT = 1200, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Professional Paint Tool")
    
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((0, 0, 0))
    clock = pygame.time.Clock()

    # --- State Variables ---
    mode = 'blue'        # Current color mode
    drawing_mode = 1     # 1=Pencil, 2=Rect, etc.
    brush_idx = 1
    BRUSH_SIZES = [2, 5, 10]
    
    points = []          # For freehand
    figures = []         # For shape preview
    fig_start = (0, 0)
    
    text_active = False
    text_buf = ""
    text_cursor = (0, 0)
    
    FIGURE_MODES = (2, 3, 4, 5, 6, 7, 8)
    color_map = {'red': (255,0,0), 'green': (0,255,0), 'blue': (0,0,255), 'erase': (0,0,0)}
    
    # UI Buttons
    r_btn = pygame.Rect(30, 350, 30, 30)
    g_btn = pygame.Rect(70, 350, 30, 30)
    b_btn = pygame.Rect(110, 350, 30, 30)

    instructions = [
        "Z: Rect | X: Circle | Q: Square",
        "W: R-Tri | E: E-Tri | R: Rhombus",
        "L: Pencil | N: Line | F: Fill",
        "T: Text | C: Eraser | A: Clear",
        "1/2/3: Brush Size | Ctrl+S: Save"
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        radius = BRUSH_SIZES[brush_idx]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if text_active:
                    if event.key == pygame.K_RETURN:
                        tf = pygame.font.SysFont(None, 36)
                        canvas.blit(tf.render(text_buf, True, color_map.get(mode)), text_cursor)
                        text_active = False
                    elif event.key == pygame.K_BACKSPACE: text_buf = text_buf[:-1]
                    else: text_buf += event.unicode
                    continue

                # Tool & Size Selection
                if event.key == pygame.K_1: brush_idx = 0
                elif event.key == pygame.K_2: brush_idx = 1
                elif event.key == pygame.K_3: brush_idx = 2
                elif event.key == pygame.K_z: drawing_mode = 2
                elif event.key == pygame.K_x: drawing_mode = 3
                elif event.key == pygame.K_q: drawing_mode = 4
                elif event.key == pygame.K_w: drawing_mode = 5
                elif event.key == pygame.K_e: drawing_mode = 6
                elif event.key == pygame.K_r: drawing_mode = 7
                elif event.key == pygame.K_n: drawing_mode = 8
                elif event.key == pygame.K_f: drawing_mode = 9
                elif event.key == pygame.K_t: drawing_mode = 10
                elif event.key == pygame.K_c: mode = 'erase'
                elif event.key == pygame.K_l: drawing_mode = 1
                elif event.key == pygame.K_a: canvas.fill((0,0,0))
                
                # Save Function
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    fname = f"paint_{datetime.datetime.now().strftime('%H%M%S')}.png"
                    pygame.image.save(canvas, fname)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check Color Buttons First
                    if r_btn.collidepoint(mouse_pos): mode = 'red'
                    elif g_btn.collidepoint(mouse_pos): mode = 'green'
                    elif b_btn.collidepoint(mouse_pos): mode = 'blue'
                    # Then Check Tools
                    elif drawing_mode == 9:
                        tools.flood_fill(canvas, mouse_pos[0], mouse_pos[1], color_map.get(mode))
                    elif drawing_mode == 10:
                        text_active, text_cursor, text_buf = True, mouse_pos, ""
                    elif drawing_mode in FIGURE_MODES:
                        fig_start = mouse_pos
                        figures = [(fig_start, mouse_pos)]
                    elif drawing_mode == 1:
                        points = [mouse_pos]

            if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if drawing_mode == 1 and points:
                    tools.draw_line_between(canvas, len(points), points[-1], mouse_pos, radius, mode)
                    points.append(mouse_pos)
                elif drawing_mode in FIGURE_MODES:
                    figures = [(fig_start, mouse_pos)]

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing_mode in FIGURE_MODES and figures:
                    s, e = figures[0]
                    tools.draw_fig(canvas, s, e, radius, mode, drawing_mode)
                    figures = []

        # --- Rendering ---
        screen.blit(canvas, (0, 0)) # Draw permanent canvas
        
        # Draw dynamic previews
        if drawing_mode in FIGURE_MODES and figures:
            s, e = figures[0]
            tools.draw_fig(screen, s, e, radius, mode, drawing_mode)
        
        if text_active:
            tf = pygame.font.SysFont(None, 36)
            screen.blit(tf.render(text_buf + "|", True, (255,255,255)), text_cursor)

        # Draw UI Overlay
        ui_font = pygame.font.SysFont(None, 24)
        for i, line in enumerate(instructions):
            surf = ui_font.render(line, True, (200, 200, 200))
            screen.blit(surf, (10, 10 + i * 20))
            
        status = ui_font.render(f"Mode: {mode.upper()} | Tool: {drawing_mode} | Size: {radius}px", True, (255, 255, 0))
        screen.blit(status, (10, 10 + len(instructions) * 20 + 5))

        # Color Buttons
        pygame.draw.rect(screen, (255,0,0), r_btn)
        pygame.draw.rect(screen, (0,255,0), g_btn)
        pygame.draw.rect(screen, (0,0,255), b_btn)
        # Outline active color
        active_rect = r_btn if mode == 'red' else g_btn if mode == 'green' else b_btn
        pygame.draw.rect(screen, (255,255,255), active_rect, 2)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()