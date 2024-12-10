import pygame
import random
import time
import sys
import os
import subprocess
pygame.init()

# Configuración de pantalla en modo pantalla completa
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Sopa de Letras - Juego de Palabras")

# Cargar la imagen de fondo
background = pygame.image.load("fondos.jpg")
background = pygame.transform.scale(background, (width, height))  
# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # Color amarillo para "Mind"
TIMER_COLOR = (255, 0, 0)  # Color del temporizador en rojo

# Fuente
font = pygame.font.SysFont('Arial', 28)
font_small = pygame.font.SysFont('Arial', 24)

# Configuración de la sopa de letras
words = ["MONITOR", "TECLADO", "RATON", "PROCESADOR", "MEMORIA", "PLACA", "FUENTE", 
         "DISCO", "HARDWARE", "SOFTWARE", "INTERNET", "INFORMATICA", "INFORMACION"]
grid_size = 15
cell_size = 37
grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
found_words = []
found_word_positions = []

# Centrado de la cuadrícula en la pantalla
grid_x_offset = (width - grid_size * cell_size) // 2
grid_y_offset = (height - grid_size * cell_size) // 2

# Variables de tiempo
time_limit = 180  # Límite de tiempo en segundos
start_time = None
game_started = False
game_over = False
elapsed_time = 0

# Variables de selección de palabras
start_pos = None
end_pos = None

# Funciones para el juego
def place_words():
    global grid
    for word in words:
        placed = False
        while not placed:
            direction = random.choice(['H', 'V', 'D'])  # H=Horizontal, V=Vertical, D=Diagonal
            if direction == 'H':
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - len(word))
                if all(grid[row][col + i] == ' ' for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row][col + i] = word[i]
                    placed = True
            elif direction == 'V':
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - 1)
                if all(grid[row + i][col] == ' ' for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row + i][col] = word[i]
                    placed = True
            elif direction == 'D':  # Diagonal
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - len(word))
                if all(grid[row + i][col + i] == ' ' for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row + i][col + i] = word[i]
                    placed = True

# Relleno de letras aleatorias
def fill_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == ' ':
                grid[row][col] = chr(random.randint(65, 90))

# Dibujar la cuadrícula de la sopa de letras
def draw_grid():
    global grid_y_offset  # Usamos la variable grid_y_offset para ajustar la posición de la cuadrícula
    grid_y_offset = 185  # Ajusta este valor para mover la cuadrícula aún más abajo

    for row in range(grid_size):
        for col in range(grid_size):
            letter = font.render(grid[row][col], True, BLACK)
            rect = pygame.Rect(col * cell_size + grid_x_offset, row * cell_size + grid_y_offset, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            # Resalta las palabras encontradas
            if (row, col) in found_word_positions:
                pygame.draw.rect(screen, GREEN, rect)
            screen.blit(letter, (col * cell_size + grid_x_offset + 10, row * cell_size + grid_y_offset + 5))

# Dibujar la lista de palabras a encontrar
def draw_word_list():
    y_offset = 155  # Incrementa este valor para bajar la posición de la lista
    for idx, word in enumerate(words):
        color = RED if word in found_words else BLACK
        word_text = font_small.render(f"{idx + 1}. {word}", True, color)
        screen.blit(word_text, (width - 200, y_offset))
        y_offset += 30


# Función para el temporizador
def draw_timer():
    global elapsed_time
    elapsed_time = time.time() - start_time if game_started else 0
    
    # Usar la fuente Martian
    timer_font = pygame.font.Font("martian.ttf", 30)
    
    # Crear el texto "Tiempo: " en negro
    time_label = timer_font.render("Tiempo: ", True, (0, 0, 0))  # Color negro
    
    # Crear el texto de los minutos y segundos en rojo
    remaining_time = int(time_limit - elapsed_time)
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    time_value = timer_font.render(f"{minutes:02}:{seconds:02}", True, (255, 0, 0))  # Color rojo
    
    # Posicionar el texto en la pantalla
    timer_x = 50
    timer_y = height - 100  # Moverlo 20 píxeles más arriba
    
    # Dibujar el texto "Tiempo: " en negro
    screen.blit(time_label, (timer_x, timer_y))
    
    # Dibujar el tiempo restante en rojo, a la derecha del texto "Tiempo: "
    screen.blit(time_value, (timer_x + time_label.get_width(), timer_y))
    
    # Verificar si el tiempo se ha agotado
    if elapsed_time >= time_limit:
        end_game(False)


# Función de selección de palabras
def check_selection(start, end):
    selected_word = ""
    selected_positions = []

    # Validación para asegurar que la selección está dentro de los límites de la cuadrícula
    if start[0] < 0 or start[0] >= grid_size or start[1] < 0 or start[1] >= grid_size:
        return  # Ignorar si la selección está fuera de los límites

    # Horizontal
    if start[0] == end[0]:
        if start[1] < 0 or start[1] >= grid_size or end[1] < 0 or end[1] >= grid_size:
            return  # Ignorar si la selección está fuera de los límites

        for c in range(start[1], end[1] + 1) if start[1] < end[1] else range(start[1], end[1] - 1, -1):
            if c < 0 or c >= grid_size:  # Asegurarse de que c no esté fuera de los límites
                return
            selected_word += grid[start[0]][c]
            selected_positions.append((start[0], c))

    # Vertical
    elif start[1] == end[1]:
        if start[0] < 0 or start[0] >= grid_size or end[0] < 0 or end[0] >= grid_size:
            return  # Ignorar si la selección está fuera de los límites

        for r in range(start[0], end[0] + 1) if start[0] < end[0] else range(start[0], end[0] - 1, -1):
            if r < 0 or r >= grid_size:  # Asegurarse de que r no esté fuera de los límites
                return
            selected_word += grid[r][start[1]]
            selected_positions.append((r, start[1]))

    # Diagonal
    elif abs(start[0] - end[0]) == abs(start[1] - end[1]):
        row, col = start
        while (row != end[0] + (1 if start[0] < end[0] else -1)) and (col != end[1] + (1 if start[1] < end[1] else -1)):
            if row < 0 or row >= grid_size or col < 0 or col >= grid_size:  # Validación adicional para la diagonal
                return
            selected_word += grid[row][col]
            selected_positions.append((row, col))
            row += 1 if start[0] < end[0] else -1
            col += 1 if start[1] < end[1] else -1

    if selected_word in words and selected_word not in found_words:
        found_words.append(selected_word)
        found_word_positions.extend(selected_positions)

# Verificar si el juego ha terminado
def end_game(won):
    global game_started, game_over
    game_started = False
    game_over = True

    # Determinar el mensaje
    if won:
        message = "¡Has completado la sopa de letras! 🎉"
    else:
        message = "¡Tiempo agotado! 😞"

    # Crear el texto
    text = font.render(message, True, BLACK)
    
    # Establecer el tamaño del cuadro de texto
    text_width, text_height = text.get_width(), text.get_height()
    padding = 20  # Espacio adicional alrededor del texto
    box_width = text_width + padding * 2
    box_height = text_height + padding * 2
    
    # Definir el rectángulo para el cuadro de texto
    box_rect = pygame.Rect((width // 2 - box_width // 2, height // 2 - box_height // 2), (box_width, box_height))
    
    # Dibujar el fondo del cuadro de texto (cuadro con color de fondo)
    pygame.draw.rect(screen, WHITE, box_rect)
    pygame.draw.rect(screen, BLACK, box_rect, 3)  # Un borde alrededor del cuadro

    # Dibujar el texto dentro del cuadro
    screen.blit(text, (width // 2 - text_width // 2, height // 2 - text_height // 2))
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Mostrar el botón "Continuar" o "Reiniciar"
    if won:
        continue_button = draw_continue_button()  # Asume que esta función devuelve un rectángulo de botón.
    else:
        restart_button = draw_buttons()  # Similar a la de continuar, asume que devuelve un rectángulo.

    # Bucle de espera hasta que se haga clic en un botón
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verificar si el clic está dentro del área del botón
                if won and continue_button.collidepoint(mouse_pos):
                    waiting_for_click = False  # Salir del bucle
                elif not won and restart_button.collidepoint(mouse_pos):
                    waiting_for_click = False  # Salir del bucle

        # Actualizar la pantalla mientras esperamos
        pygame.display.update()




# Reiniciar el juego
def restart_game():
    global grid, found_words, found_word_positions, game_started, game_over, start_time
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    found_words.clear()
    found_word_positions.clear()
    place_words()
    fill_grid()
    game_started = True
    game_over = False
    start_time = time.time()

# Función para dibujar los botones
def draw_buttons():
    margin = 30  # Margen de 30 píxeles desde el borde izquierdo
    spacing = 10  # Espacio entre botones

    # Obtener la posición del ratón
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Definir los botones
    restart_button = pygame.Rect(margin, height // 2 - 50, 200, 50)
    quit_button = pygame.Rect(margin, height // 2 + 60, 200, 50)

    # Comprobar si el ratón está sobre el botón
    restart_hover = restart_button.collidepoint(mouse_x, mouse_y)
    quit_hover = quit_button.collidepoint(mouse_x, mouse_y)

    # Botón Reiniciar - Gris con hover gris y borde redondeado
    restart_color = (169, 169, 169) if not restart_hover else (169, 169, 169)  # Gris en hover también
    pygame.draw.rect(screen, restart_color, restart_button, border_radius=17)
    restart_text = pygame.font.Font("martian.ttf", 35).render("Reiniciar", True, BLACK if not restart_hover else WHITE)
    
    # Centrar el texto en el botón
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

    # Botón Salir - Rojo con hover gris y borde redondeado
    quit_color = (255, 0, 0) if not quit_hover else (169, 169, 169)  # Gris en hover
    pygame.draw.rect(screen, quit_color, quit_button, border_radius=17)
    quit_text = pygame.font.Font("martian.ttf", 35).render("Salir", True, WHITE if quit_hover else BLACK)
    
    # Centrar el texto en el botón
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)

    return restart_button, quit_button

def draw_continue_button():
    # Dimensiones del botón
    button_width = 200
    button_height = 50
    button_margin = 30  # Margen desde los bordes

    # Definir la posición del botón en la esquina inferior derecha
    button_x = width - button_width - button_margin
    button_y = height - button_height - button_margin

    # Rectángulo del botón
    continue_button = pygame.Rect(button_x, button_y, button_width, button_height)

    # Obtener la posición del ratón
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Cambiar color del botón al pasar el mouse
    base_color = (173, 216, 230)  # Color celeste
    hover_color = (135, 206, 250)  # Celeste más claro al pasar el ratón
    continue_color = base_color if not continue_button.collidepoint(mouse_x, mouse_y) else hover_color

    # Dibujar el botón
    pygame.draw.rect(screen, continue_color, continue_button, border_radius=17)
    continue_text = pygame.font.Font("martian.ttf", 35).render("Continuar", True, BLACK)

    # Centrar el texto en el botón
    continue_text_rect = continue_text.get_rect(center=continue_button.center)
    screen.blit(continue_text, continue_text_rect)

    return continue_button

# Cargar la fuente personalizada
RED = (255, 0, 0)
GRAY = (169, 169, 169)  # Gris
YELLOW = (255, 255, 0)
# Dibujar título y descripción con la fuente personalizada
def draw_title_description():
    font_title = pygame.font.Font("martian.ttf", 60)  # Título
    font_small = pygame.font.Font("comic.ttf", 20)  # Texto pequeño con fuente más pequeña
    
    # Título con partes de diferente color
    title_text_1 = font_title.render("SOPA DE LETRAS  ", True, BLACK)  # "SO" en negro
    title_text_2 = font_title.render("MI", True, RED)    # "MI" en rojo
    title_text_3 = font_title.render("ND", True, GRAY)   # "ND" en gris
    title_text_4 = font_title.render("CODE", True, (255, 194, 0))  # "CODE" en amarillo

    # Posicionar cada parte del título
    x_offset = width // 2 - (title_text_1.get_width() + title_text_2.get_width() + title_text_3.get_width() + title_text_4.get_width()) // 2
    screen.blit(title_text_1, (x_offset, 20))
    x_offset += title_text_1.get_width()
    screen.blit(title_text_2, (x_offset, 20))
    x_offset += title_text_2.get_width()
    screen.blit(title_text_3, (x_offset, 20))
    x_offset += title_text_3.get_width()
    screen.blit(title_text_4, (x_offset, 20))

    # Descripción con tamaño de fuente reducido
    description_text = font_small.render("Encuentra todas las palabras ocultas en la cuadrícula. Presiona el \n"
                                        "botón izquierdo sobre la palabra correcta y arrástralo sin soltar \n"
                                        "hasta el final de la palabra para validar y remarcar tu logro.", 
                                        True, BLACK)
    
    # Ajustar la posición de la descripción para que esté justo debajo del título, sin espacio
    screen.blit(description_text, (width // 2 - description_text.get_width() // 2, 85))  # Sin espacio entre título y descripción

def continue_game():
    print("Continuando el juego... ejecutando el Sudoku")
    # Ejecuta el script del sudoku como un proceso separado
    subprocess.run(["python", "sudokulisto.py"])
    restart_game()
    
# Loop principal
place_words()
fill_grid()
game_started = True
start_time = time.time()

while True:
    screen.blit(background, (0, 0))

    # Dibujar título, cuadrícula, lista de palabras, temporizador
    draw_title_description()
    draw_grid()
    draw_word_list()
    draw_timer()

    # Dibujar botones
    restart_button, quit_button = draw_buttons()

    # Mostrar botón "Continuar" si todas las palabras han sido encontradas
    if game_over and set(found_words) == set(words):
        continue_button = draw_continue_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                start_pos = (event.pos[1] - grid_y_offset) // cell_size, (event.pos[0] - grid_x_offset) // cell_size
            if restart_button.collidepoint(event.pos):
                restart_game()
            if quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

            if game_over and set(found_words) == set(words):
                if continue_button.collidepoint(event.pos):
                    continue_game()

        if event.type == pygame.MOUSEBUTTONUP and not game_over:
            end_pos = (event.pos[1] - grid_y_offset) // cell_size, (event.pos[0] - grid_x_offset) // cell_size
            check_selection(start_pos, end_pos)

    # Verificar si todas las palabras han sido encontradas
    if not game_over and set(found_words) == set(words):
        end_game(True)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
