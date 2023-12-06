import pygame as pg
import sys
from Circle import Circle
from Bucket import Bucket
from ScoreCounter import ScoreCounter

# Initialize Pygame
pg.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60
WHITE = (255, 255, 255)

# Game window
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Circle Physics")

clock = pg.time.Clock()

#Score counter
score_counter = ScoreCounter("arial.ttf", 60, 0.7*WIDTH, 0.15*HEIGHT)

bucket_height = 0.8*HEIGHT
bucket_width = 2*HEIGHT/3

#Bucket
bucket = Bucket((WIDTH - 2*bucket_width) // 2, HEIGHT - 1.1*bucket_height, bucket_width, bucket_height, (0,0,255))


#Circle array
circles = []

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                new_circle = Circle(x, y, 30)
                circles.append(new_circle)

    # Update circles
    for circle in circles:
        circle.update(WIDTH, HEIGHT, bucket.rect, circles, score_counter)

    # Check collision and combine circles
    # Inside the game loop
    # Suika.py - Inside the game loop where circles are checked for collision and combined
    for circle in circles:
        for other_circle in circles:
            if circle != other_circle and circle.check_collision(other_circle):
                new_circle, removed_circle_radius = circle.combine(other_circle)
                if new_circle:
                    circles.remove(circle)
                    circles.remove(other_circle)
                    score_counter.increase_score(removed_circle_radius)
                    circles.append(new_circle)
                    break
        else:
            continue
        break






    # Clear the screen
    screen.fill(WHITE)

    # Draw Graphics
    score_counter.render_score(screen)

    # Bucket
    screen.blit(bucket.image, bucket.rect)

    # Draw circles
    for circle in circles:
        screen.blit(circle.image, circle.rect)

    # Update display
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
sys.exit()
