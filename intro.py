import pygame
from moviepy.editor import VideoFileClip


# Inicializar Pygame y el mezclador de audio
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mind Code")

# Cargar el video de fondo para el menú principal
clip_menu = VideoFileClip("vortexmenu.mp4")  # Video para el menú
background_frames_menu = clip_menu.iter_frames(fps=60, dtype="uint8")

# Cargar el video de fondo para la configuración
clip_config = VideoFileClip("vortexfuturo.mp4")  # Video para la configuración
background_frames_config = clip_config.iter_frames(fps=60, dtype="uint8")

# Obtener dimensiones de los videos
video_width_menu, video_height_menu = clip_menu.size
x_offset_menu = (width - video_width_menu) // 2
y_offset_menu = (height - video_height_menu) // 2

video_width_config, video_height_config = clip_config.size
x_offset_config = (width - video_width_config) // 2
y_offset_config = (height - video_height_config) // 2

# Cargar el logo (imagen)
logo_image = pygame.image.load("loguito.png")

# Cargar música de fondo y efecto de sonido
pygame.mixer.music.load("juego.mp3")
pygame.mixer.music.play(-1)  # Reproducción en bucle infinito
effect_sound = pygame.mixer.Sound("master.wav")

# Colores de los botones y barra
button_color = (0, 255, 255)
hover_color = (255, 255, 255)
bar_background_color = (100, 100, 100)
bar_fill_color = (0, 255, 255)

# Fuente y su tamaño
font = pygame.font.Font('martian.ttf', 48)
font_config=pygame.font.Font('martian.ttf', 60)

# Variables de configuración de audio
music_volume = 0.1  # Volumen inicial de la música
sfx_volume = 0.1  # Volumen inicial de efectos de sonido
pygame.mixer.music.set_volume(music_volume)
effect_sound.set_volume(sfx_volume)

# Pantallas de menú
main_menu = True
audio_settings = False

# Cargar iconos
music_icon = pygame.image.load("ico.png")  # Reemplaza con el ícono de música
sfx_icon = pygame.image.load("ico.png")    # Reemplaza con el ícono de efectos de sonido
button_font = pygame.font.Font('martian.ttf', 36)  # Fuente más pequeña para los botones

# Función para dibujar un botón
def draw_button(text, x, y, width, height, color, hover_color, radius=17):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=radius)
        if click[0] == 1:
            global main_menu, audio_settings
    
            if text == "JUGAR":
                # Ejecutar el script utilizando subprocess
                print("Iniciando")
               
            elif text == "CONFIGURACION":
                main_menu = False
                audio_settings = True
            elif text == "SALIR":
                pygame.quit()
                quit()
            elif text == "VOLVER":  # Arreglar la acción de VOLVER
                audio_settings = False
                main_menu = True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=radius)
    
    #Ubicar el texto de los botones en el centro    
    text_surface = button_font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    screen.blit(text_surface, text_rect)

# Función para ajustar la imagen al tamaño de la ventana sin distorsionar
def scale_background(image, screen_width, screen_height):
    img_width, img_height = image.get_size()
    
    # Mantener la relación de aspecto original
    aspect_ratio = img_width / img_height
    if screen_width / screen_height > aspect_ratio:
        new_width = screen_height * aspect_ratio
        new_height = screen_height
    else:
        new_width = screen_width
        new_height = screen_width / aspect_ratio
    
    # Redimensionar la imagen
    return pygame.transform.scale(image, (int(new_width), int(new_height)))

# Función para dibujar la pantalla de configuración de audio
# Modificar el tamaño de la fuente para el indicador de volumen
indicator_font = pygame.font.Font('martian.ttf', 25)  # Fuente más pequeña para el indicador de volumen

# Función para dibujar la pantalla de configuración de audio
def draw_audio_settings():
    global background_frames_config, music_volume, sfx_volume
    # Mantener el fondo del video para configuración (video diferente)
    try:
        frame = next(background_frames_config)
    except StopIteration:
        # Si el generador de frames se ha agotado, reiniciar el clip y el generador
        clip_config = VideoFileClip("vortexfuturo.mp4")  # Cambiar aquí al nuevo video
        background_frames_config = clip_config.iter_frames(fps=60, dtype="uint8")
        frame = next(background_frames_config)
    
    background_image = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    background_image = scale_background(background_image, width, height)  # Ajustar fondo a pantalla completa
    screen.blit(background_image, (0, 0))  # Mostrar el fondo ajustado

    # Título de configuracion de audio--
    title_text = font_config.render("Configuracion de Audio", True, (255, 0, 0))  # Texto rojo
    title_rect = title_text.get_rect(center=(width // 2, 225))
    screen.blit(title_text, title_rect)
    
    # Posición centrada de las barras
    bar_x_center = width // 2 - 200  # Ajustado para centrar las barras más largas (ancho aumentado)
    
    # Música
    music_text = font.render("Musica", True, (255, 255, 255))
    screen.blit(music_text, (bar_x_center, 320))  # Colocar el texto encima de la barra
    
    # Icono de música (a la izquierda de la barra)
    screen.blit(music_icon, (bar_x_center - 45, 328))  # Icono ajustado con la barra
    
    # Barra de volumen de música (más larga)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x_center, 370, 400, 20), border_radius=10)  # Fondo de la barra con bordes redondeados
    pygame.draw.rect(screen, (0, 139, 139), (bar_x_center, 370, int(400 * music_volume), 20), border_radius=10)  # Relleno de la barra con bordes redondeados
    
    # Indicador de volumen de música (porcentaje)
    volume_text = indicator_font.render(f"{int(music_volume * 100)}%", True, (0, 0, 0))
    screen.blit(volume_text, (bar_x_center + 400 - volume_text.get_width(), 370))  # Posición al final de la barra

    # Efectos de sonido
    sfx_text = font.render("Efectos de Sonido", True, (255, 255, 255))
    screen.blit(sfx_text, (bar_x_center, 475))  # Colocar encima de la barra
    
    # Icono de efectos de sonido (a la izquierda de la barra)
    screen.blit(sfx_icon, (bar_x_center - 45, 480))  # Icono ajustado con la barra

    # Barra de volumen de efectos de sonido (más larga)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x_center, 520, 400, 20), border_radius=10)  # Fondo de la barra con bordes redondeados
    pygame.draw.rect(screen, (0, 139, 139), (bar_x_center, 520, int(400 * sfx_volume), 20), border_radius=10)  # Relleno de la barra con bordes redondeados

    # Indicador de volumen de efectos de sonido (porcentaje)
    sfx_volume_text = indicator_font.render(f"{int(sfx_volume * 100)}%", True, (0, 0, 0))
    screen.blit(sfx_volume_text, (bar_x_center + 400 - sfx_volume_text.get_width(), 520))  # Posición al final de la barra

    # Botón "VOLVER"
    back_button_x = width // 2 - 130
    back_button_y = 650
    draw_button("VOLVER", back_button_x, back_button_y, 260, 55, button_color, hover_color)

    # Ajustar los valores del volumen al arrastrar los sliders
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Ajustar el volumen de música
    if bar_x_center < mouse[0] < bar_x_center + 400:  # Modificado para reflejar la barra más larga
        if 370 < mouse[1] < 390 and click[0] == 1:
            music_volume = (mouse[0] - bar_x_center) / 400  # Modificado para reflejar la barra más larga
            pygame.mixer.music.set_volume(music_volume)  # Aplicar volumen a la música
    
    # Ajustar el volumen de efectos de sonido
    if bar_x_center < mouse[0] < bar_x_center + 400:  # Modificado para reflejar la barra más larga
        if 520 < mouse[1] < 540 and click[0] == 1:
            sfx_volume = (mouse[0] - bar_x_center) / 400  # Modificado para reflejar la barra más larga
            effect_sound.set_volume(sfx_volume)  # Aplicar volumen a los efectos de sonido
            effect_sound.play()  # Reproduce el efecto para probar el volumen

# Bucle principal del juego
running = True
frame_gen_menu = background_frames_menu
frame_gen_config = background_frames_config

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if main_menu:
        # Obtener el siguiente fotograma del video para el menú
        try:
            frame = next(frame_gen_menu)
        except StopIteration:
            clip_menu = VideoFileClip("vortexmenu.mp4")  # Video del menú
            frame_gen_menu = clip_menu.iter_frames(fps=60, dtype="uint8")
            frame = next(frame_gen_menu)

        background_image = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        background_image = scale_background(background_image, width, height)  # Ajustar el fondo al tamaño de la ventana
        screen.blit(background_image, (0, 0))  # Mostrar el fondo ajustado

        # Dibujar botones
        draw_button("JUGAR", width // 2 - 130, 500, 260, 55, button_color, hover_color)
        draw_button("CONFIGURACION", width // 2 - 165, 590, 330, 55, button_color, hover_color)
        draw_button("SALIR", width // 2 - 130, 680, 260, 55, button_color, hover_color)

        # Dibujar el logo
        logo_rect = logo_image.get_rect(center=(width // 2, 400))
        screen.blit(logo_image, logo_rect)
    
    #Acceso a configuraciones de audio
    elif audio_settings:
        draw_audio_settings()

    pygame.display.update()

pygame.quit()
