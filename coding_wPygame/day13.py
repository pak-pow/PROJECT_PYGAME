import pygame, sys, array
import math

# 1. Setup
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)  # CD Quality Audio
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Day 13: Audio System")


# --- SOUND SYNTHESIZER (Making fake sound files in memory) ---
def generate_beep(frequency=440, duration=0.1):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = array.array('h')  # 'h' means signed short (16-bit)

    for i in range(n_samples):
        # Math to create a sine wave
        val = math.sin(2 * math.pi * frequency * (i / sample_rate))
        # Volume scale (32767 is max for 16-bit audio)
        buf.append(int(val * 10000))

    return pygame.mixer.Sound(buffer=buf)


# 2. Create Sounds
jump_sfx = generate_beep(frequency=600, duration=0.1)  # High pitch beep
boom_sfx = generate_beep(frequency=150, duration=0.3)  # Low pitch rumble

# Music State
is_music_playing = False

font = pygame.font.SysFont(None, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # SFX: Jump
            if event.key == pygame.K_SPACE:
                jump_sfx.play()
                print("Played Jump SFX")

            # SFX: Explosion
            if event.key == pygame.K_z:
                boom_sfx.play()
                print("Played Boom SFX")

            # MUSIC TOGGLE (Simulated loop)
            if event.key == pygame.K_RETURN:
                if is_music_playing:
                    pygame.mixer.stop()  # Stops all playback (simulating music stop)
                    is_music_playing = False
                else:
                    # In real code: pygame.mixer.music.play(-1)
                    # Here we just loop a long beep to simulate it
                    long_note = generate_beep(frequency=200, duration=5.0)
                    long_note.play(loops=-1)  # -1 means loop forever
                    is_music_playing = True

    screen.fill((20, 20, 20))

    # UI Instructions
    text1 = font.render("SPACE: Jump Sound", True, (0, 255, 0))
    text2 = font.render("Z: Boom Sound", True, (255, 50, 50))
    text3 = font.render("ENTER: Toggle Loop", True, (50, 100, 255))

    screen.blit(text1, (50, 100))
    screen.blit(text2, (50, 150))
    screen.blit(text3, (50, 200))

    pygame.display.update()