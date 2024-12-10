import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla (modo Full Screen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Ajustar la pantalla al tamaño completo
width, height = screen.get_size()  # Obtener las dimensiones de la pantalla
# Cargar imagen de fondo
background_image = pygame.image.load("fondos.jpg")  # Cambia "background.jpg" por el nombre de tu imagen
background_image = pygame.transform.scale(background_image, (width, height))  # Escala la imagen al tamaño de la pantalla

pygame.display.set_caption("Sudoku 4x4")

fuente_boton = pygame.font.Font('martian.ttf', 35)  # Aumento del tamaño de la fuente
button_pista = (12,183,242)
button_reinciar = (157,192,157)
button_salir = (245,4,0)
hover_color = (255, 255, 255)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
CELBLUE = (173, 216, 230)
GREEN = (100, 255, 100)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)

# Fuentes
font = pygame.font.SysFont("Arial", 60, bold=True)  # Números en negrita más grandes
small_font = pygame.font.SysFont("Arial", 25)  # Tamaño más pequeño para otros textos
title_font = pygame.font.SysFont("Arial", 80, bold=True)  # Título en negrita más grande
description_font = pygame.font.SysFont("Arial", 35, bold=True)  # Descripción en negrita y tamaño 35

# Fondo
background_color = (240, 240, 255)

# Sudoku 4x4
solution = [
    [4, 1, 3, 2],
    [2, 3, 1, 4],
    [1, 4, 2, 3],
    [3, 2, 4, 1]
]
puzzle = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
    [3, 0, 4, 0]
]

# Números arrastrables (1 a 4) con espacio adicional antes de cada número
draggable_numbers = [
    {"number": i, "rect": pygame.Rect(width // 2 - 200 + (i - 1) * 80 + 20, height // 2 + 250, 50, 50), "selected": False}
    for i in range(1, 5)
]

comic_font = pygame.font.Font("comic.ttf", 30)
# Variables globales
selected_number = None
hint_count = 0  # Contador de pistas
max_hints = 3  # Número máximo de pistas

NUMBERS_COLORS = [
    (0, 0, 255),  # Azul para el número 1
    (0, 255, 0),  # Verde para el número 2
    (255, 0, 0),  # Rojo para el número 3
    (255, 165, 0)  # Naranja para el número 4
]

# Función para dar una pista
def give_hint():
    global hint_count
    if hint_count < max_hints:
        # Buscar una celda vacía y poner el número correcto de la solución
        for row in range(4):
            for col in range(4):
                if puzzle[row][col] == 0:  # Si la celda está vacía
                    puzzle[row][col] = solution[row][col]  # Coloca el número correcto
                    hint_count += 1  # Incrementa el contador de pistas
                    print(f"Pista dada. Total de pistas: {hint_count}")  # Imprimir para debug
                    return  # Termina la función después de dar una pista
    else:
        print("Ya no hay más pistas disponibles.")  # Si no hay más pistas, imprimir un mensaje

# Función para reiniciar el Sudoku
def restart_game():
    global puzzle, hint_count
    puzzle = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
    [3, 0, 4, 0]
]
    hint_count = 0
    print("Juego reiniciado.")

# Función para salir
def quit_game():
    pygame.quit()
    quit()

# Función para verificar si el Sudoku está completo y correcto
def check_sudoku_complete():
    global puzzle
    filled = True  # Variable para verificar si el tablero está completamente lleno

    for row in range(4):
        for col in range(4):
            if puzzle[row][col] == 0:  # Si hay una celda vacía, el tablero no está completo
                filled = False
            elif puzzle[row][col] != solution[row][col]:  # Si alguna celda no coincide con la solución
                if filled:  # Si el tablero está lleno pero tiene errores
                    print("El Sudoku está lleno pero incorrecto. Corrigiendo números erróneos...")
                    remove_incorrect_numbers()  # Llama a la nueva función para eliminar números incorrectos
                return False  # Retorna falso porque no está correcto

    if filled:  # Si el tablero está lleno y no hay errores
        print("¡Sudoku completado correctamente!")
        return True

    return False  # El tablero no está completo

# Nueva función para borrar solo los números incorrectos
def remove_incorrect_numbers():
    global puzzle
    for row in range(4):
        for col in range(4):
            if puzzle[row][col] != 0 and puzzle[row][col] != solution[row][col]:
                puzzle[row][col] = 0  # Borra los números incorrectos
                print(f"Número incorrecto eliminado en la celda ({row}, {col}).")  # Mensaje de depuración


# Función para mostrar el botón "Continuar"
def show_continue_button():
    if check_sudoku_complete():  # Solo mostrar si el puzzle está completo y correcto
        continue_button = Button(
            width - 200,  # Posición en la esquina inferior derecha
            height - 100,
            150, 60, "CONTINUAR", GREEN, hover_color, quit_game
        )
        continue_button.draw(screen)  # Dibuja el botón
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_button.rect.collidepoint(event.pos):
                    continue_button.action()  # Ejecutar la acción del botón

# Clase para manejar los botones
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action  # La acción que se ejecutará al hacer clic
        self.rect = pygame.Rect(x, y, width, height)  # Área de interacción del botón
    
    def draw(self, screen):
        # Detectar si el mouse está sobre el botón para aplicar el efecto hover
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=17)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=17)

        # Dibujar el texto del botón en el centro
        font = pygame.font.Font('martian.ttf', 35)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        # Si el botón fue presionado, ejecutar la acción
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.action:
                    self.action()

# Dibujar la cuadrícula de Sudoku
def draw_grid():
    grid_start_x, grid_start_y = width // 2 - 200, height // 2 - 100  # Baja el sudoku
    cell_size = 80

    # Dibujar las líneas de la cuadrícula
    for i in range(5):
        pygame.draw.line(screen, BLACK, 
                         (grid_start_x, grid_start_y + i * cell_size), 
                         (grid_start_x + 4 * cell_size, grid_start_y + i * cell_size), 2)
        pygame.draw.line(screen, BLACK, 
                         (grid_start_x + i * cell_size, grid_start_y), 
                         (grid_start_x + i * cell_size, grid_start_y + 4 * cell_size), 2)

    # Rellenar las celdas con números
    for row in range(4):
        for col in range(4):
            number = puzzle[row][col]
            if number != 0:
                color = NUMBERS_COLORS[number - 1]  # Color para cada número
                text = font.render(str(number), True, color)
                x = grid_start_x + col * cell_size + cell_size // 2 - text.get_width() // 2
                y = grid_start_y + row * cell_size + cell_size // 2 - text.get_height() // 2
                screen.blit(text, (x, y))

# Dibujar los números arrastrables
def draw_draggables():
    for draggable in draggable_numbers:
        # Si está seleccionado, resaltarlo con otro color
        if draggable["selected"]:
            pygame.draw.rect(screen, YELLOW, draggable["rect"])  # Resaltado en amarillo
        else:
            pygame.draw.rect(screen, GRAY, draggable["rect"])  # Color por defecto

        text = font.render(str(draggable["number"]), True, BLACK)
        x = draggable["rect"].x + draggable["rect"].width // 2 - text.get_width() // 2
        y = draggable["rect"].y + draggable["rect"].height // 2 - text.get_height() // 2
        screen.blit(text, (x, y))

# Dibujar el título
# Dibujar el título con colores para cada palabra
# Dibujar el título con la fuente Martian y colores personalizados
def draw_title():
    # Cargar la fuente Martian con tamaño personalizado
    martian_font = pygame.font.Font("martian.ttf", 70)  # Cambia el tamaño según necesites

    # Renderizar cada parte del texto con colores específicos
    text_su = martian_font.render("SUDOKU  ", True, BLACK)  # Parte inicial en negro
    text_mi = martian_font.render("MI", True, (255, 0, 0))  # "MI" en rojo
    text_nd = martian_font.render("ND", True, (169, 169, 169))  # "ND" en gris
    text_code = martian_font.render("CODE", True, (255, 192, 0))  # "CODE" en amarillo

    # Calcular la posición inicial para centrar todo el título
    total_width = (text_su.get_width() + text_mi.get_width() +
                   text_nd.get_width() + text_code.get_width())
    start_x = width // 2 - total_width // 2  # Centrar el texto en la pantalla
    y = 20  # Posición vertical del título

    # Dibujar cada segmento del texto uno al lado del otro
    screen.blit(text_su, (start_x, y))
    screen.blit(text_mi, (start_x + text_su.get_width(), y))
    screen.blit(text_nd, (start_x + text_su.get_width() + text_mi.get_width(), y))
    screen.blit(text_code, (start_x + text_su.get_width() + text_mi.get_width() + text_nd.get_width(), y))

# Dibujar la descripción debajo del título
def draw_description():
    description_text = comic_font.render(
        "Tienes que colocar los números faltantes de manera que\nal sumar los números de cada línea vertical, horizontal\nobtengas la misma cantidad.",
        True, BLACK)
    
    # Justificar el texto y agregar margen
    text_width = description_text.get_width()
    screen.blit(description_text, (width // 2 - text_width // 2, 120))  # Espacio debajo

# Bucle principal
running = True
buttons = [
    Button(width - 180, height // 2 - 60 - 80, 150, 60, "PISTA", button_pista, hover_color, give_hint),
    Button(width - 180, height // 2 - 60, 150, 60, "REINICIAR", button_reinciar, hover_color, restart_game),
    Button(width - 180, height // 2 - 60 + 80, 150, 60, "SALIR", button_salir, hover_color, quit_game)
]

while running:
    screen.blit(background_image, (0, 0))  # Dibuja la imagen de fondo en cada frame
    draw_title()
    draw_description()
    draw_grid()
    draw_draggables()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for draggable in draggable_numbers:
                if draggable["rect"].collidepoint(event.pos):
                    selected_number = draggable["number"]  # Asignar el número seleccionado
                    for d in draggable_numbers:
                        d["selected"] = False  # Desmarcar otros números
                    draggable["selected"] = True  # Marcar este número como seleccionado

            # Colocar el número en la celda seleccionada
            grid_start_x, grid_start_y = width // 2 - 200, height // 2 - 100
            cell_size = 80
            for row in range(4):
                 for col in range(4):
                    cell_rect = pygame.Rect(grid_start_x + col * cell_size, grid_start_y + row * cell_size, cell_size, cell_size)
                    if cell_rect.collidepoint(event.pos):  # Si se hace clic en una celda
                        if puzzle[row][col] != 0:  # Si la celda ya tiene un número
                            puzzle[row][col] = 0  # Borrar el número
                            print(f"Celda ({row}, {col}) borrada.")
                        elif selected_number is not None:  # Si no está vacía y el jugador ha seleccionado un número
                            puzzle[row][col] = selected_number  # Colocar el número seleccionado
                            print(f"Número {selected_number} colocado en la celda ({row}, {col})")

        # Verificar si se hace clic en un botón
        for button in buttons:
            button.check_click(event)

    # Dibujar los botones
    for button in buttons:
        button.draw(screen)

    show_continue_button()  # Mostrar el botón de continuar si el puzzle está completo

    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
