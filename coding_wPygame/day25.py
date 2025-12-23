import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# 1. Setup
pygame.init()
display = (800, 600)

# DOUBLEBUF: specialized video buffer for smooth 3D
# OPENGL: Tells Pygame we aren't doing 2D blitting
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# 2. Camera Setup
# (FOV, Aspect Ratio, Near Clip, Far Clip)
gluPerspective(70, (display[0]/display[1]), 0.1, 50.0)

# Move the camera BACK 5 units so we can see the cube
# (x, y, z) -> Moving -5 in Z pulls us away from the object
glTranslatef(0.0, 0.0, -5)

# --- THE CUBE DATA ---
# 8 Corner points (x, y, z)
vertices = (
    (1, -1, -1),  (1, 1, -1),
    (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1),   (1, 1, 1),
    (-1, -1, 1),  (-1, 1, 1)
)

# Pairs of indices (Which vertices connect to which?)
edges = (
    (0,1), (0,3), (0,4),
    (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7),
    (5,1), (5,4), (5,7)
)

def draw_cube():
    glBegin(GL_LINES) # Start drawing Lines
    for edge in edges:
        for vertex in edge:
            # Send the vertex data to the GPU
            glVertex3fv(vertices[vertex])
    glEnd() # Stop drawing

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # 1. Rotate
    # (Angle, x_axis, y_axis, z_axis)
    # Rotate 1 degree per frame on the X and Y axes
    glRotatef(1, 3, 1, 1)

    # 2. Clear Screen
    # Clear both the Color Buffer (Pixels) and Depth Buffer (Layers)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 3. Draw
    draw_cube()

    # 4. Flip
    pygame.display.flip()
    # Simple wait to cap FPS (clock.tick doesn't work perfectly with OpenGL context sometimes)
    pygame.time.wait(10)