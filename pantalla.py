import pygame
from moviepy.editor import VideoFileClip

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mind Code")

# Cargar el video
clip = VideoFileClip("vortexmenu.mp4")
background_frames = clip.iter_frames(fps=60, dtype="uint8")  # Iterar sobre los frames del video

# Obtener dimensiones del video
video_width, video_height = clip.size

# Calcular las coordenadas para centrar el video
x_offset = (width - video_width) // 2
y_offset = (height - video_height) // 2

# Cargar el logo (imagen)
logo_image = pygame.image.load("loguito.png")

# Colores de los botones
button_color = (0, 255, 255)
hover_color = (255, 255, 255 )


# Fuente y su tamaño
font = pygame.font.Font('martian.ttf', 48)

# Dimensiones de los botones
button_width, button_height = 260, 55
config_button_width = 220  # Ancho específico para el botón de "CONFIGURACIÓN"
button_spacing = 45 # Espaciado entre los botones

# Función para dibujar un botón
def draw_button(text, x, y, width, height, color, hover_color,radius=17):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Dibujar el botón con hover
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=radius)
        if click[0] == 1:
            # Lógica para cada botón
            if text == "JUGAR":
                print("¡Comenzando el juego!")
            elif text == "CONFIGURACIÓN":
                print("Abriendo el menú de configuración")
            elif text == "SALIR":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=radius)
    # Dibujar el texto del botón
    
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)  # Centrar el texto en el botón
    screen.blit(text_surface, text_rect)

# Bucle principal del juego
running = True
frame_gen = background_frames  # Generador de fotogramas
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener el siguiente fotograma del video
    try:
        frame = next(frame_gen)
    except StopIteration:
        # Reiniciar el video volviendo a cargar el clip
        clip = VideoFileClip("vortexmenu.mp4")
        frame_gen = clip.iter_frames(fps=60, dtype="uint8")  # Volver a crear el generador
        frame = next(frame_gen)  # Obtener el primer fotograma del video reiniciado

    # Convertir el fotograma a un formato que Pygame pueda usar
    background_image = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    # Dibujar la imagen de fondo centrada
    screen.blit(background_image, (x_offset, y_offset))

    # Calcular la posición X para centrar los botones
    center_x = width // 2 - button_width // 2
    config_center_x = width // 2 - 330/ 2

    
    # Dibujar los botones
    draw_button("JUGAR", center_x, 500, button_width, button_height, button_color, hover_color)
    draw_button("CONFIGURACION", config_center_x, 590, 330, button_height, button_color, hover_color)
    draw_button("SALIR", center_x, 680, button_width, button_height, button_color, hover_color)

    # Dibujar el logo (opcional, fuera de los botones)
    logo_rect = logo_image.get_rect(center=(width // 2, 400))  # Centrado en la parte superior de la pantalla
    screen.blit(logo_image, logo_rect)

    pygame.display.update()

pygame.quit()
