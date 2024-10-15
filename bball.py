# Version: 4.9 @ 2024/10/13 04:15

import pygame
import sys
import math
import os
import random

# Constants
GRAVITY = -9810  # Negative acceleration due to gravity in mm/s^2
FPS = 120  # Frames per second for smoother animation
box_height = 1000
box_width = 500
marginpx = 340

class Ball:
    def __init__(self, initial_height_mm, initial_vx, radius_mm, color, floor_height):
        self.bounce_height = initial_height_mm + radius_mm  # bounce_height in mm (input value)
        self.y = floor_height + radius_mm  # Start at the specified height in mm
        self.vy = 0  # Initial vertical velocity in mm/s
        self.x = random.randint(0, box_width)  # Initial horizontal position in mm (set to random)
        self.vx = initial_vx  # Initial horizontal velocity in mm/s
        self.ax = 0  # Initial horizontal acceleration in mm/s²
        self.bounces = 0  # Bounce counter
        self.last_bounce_ticks = pygame.time.get_ticks()  # Time of last bounce in ticks
        self.last_bpm = 0

        # New attributes for ball properties
        self.radius = radius_mm  # Radius of the ball in mm
        self.color = color  # Color of the ball
        self.floor_height = floor_height  # Floor height in mm (bottom of the window is 0)

    @property
    def xpx(self):
        return int(self.x * WIDTH / box_width)

    @property
    def ypx(self):
        return int(self.y * HEIGHT / box_height)

    @property
    def bpm(self):
        return (self.last_bpm)

    def bounce(self):
        current_ticks = pygame.time.get_ticks()
        cycle_time = None

        if self.bounces > 0:
            cycle_time = current_ticks - self.last_bounce_ticks

        self.y = self.floor_height + self.radius
        self.vy = math.sqrt(2 * abs(GRAVITY) * self.bounce_height)

        print(f"Bouncing to {self.bounce_height} mm at {self.y} mm in {int(cycle_time) if cycle_time else 'N/A'} ms at BPM {int(self.bpm)}")

        if cycle_time and cycle_time > 0:
            self.last_bpm = (1000 * 60) / cycle_time
        
        self.last_bounce_ticks = current_ticks
        self.bounces += 1

    def update(self, delta_time):
        self.vy += GRAVITY * delta_time  
        self.y += self.vy * delta_time  
        self.x += self.vx * delta_time  

        if self.y <= self.floor_height:
            self.bounce()

        if self.xpx >= WIDTH - marginpx or self.xpx <= marginpx:
            self.vx = -self.vx  

def main(drop_height_mm):
    global WIDTH, HEIGHT
    
    pygame.init()
    
    info_object = pygame.display.Info()
    WIDTH, HEIGHT = info_object.current_w // 2, info_object.current_h
    
    print(f"Screen Width: {WIDTH}, Screen Height: {HEIGHT}")
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{info_object.current_w // 2},{0}"  
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Bouncing Balls Simulation")
    
    clock = pygame.time.Clock()
    
    balls = []  # List to hold multiple balls
    
    # Create initial balls with random properties
    for floor_height in [50, 50, 250, 250, 300]: 
        initial_vx = random.randint(-100, 100) 
        radius_mm = random.randint(30, 30) 
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
        
        balls.append(Ball(drop_height_mm, initial_vx, radius_mm, color, floor_height))

    paused = False

    while True:
        delta_time = clock.tick(FPS) / 1000.0
        
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.w, event.h
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:   # Quit on 'Q' key press
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p:   # Toggle pause on 'P' key press
                        paused = not paused
                    elif event.key == pygame.K_n:   # Create a new ball on 'N' key press
                        initial_vx = random.randint(-100, 100)
                        radius_mm = random.randint(30, 30)
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        floor_height = HEIGHT - marginpx

                        balls.append(Ball(drop_height_mm, initial_vx, radius_mm, color, floor_height))
                    elif event.key == pygame.K_RETURN:   # Remove the last ball on Enter key press
                        if balls:
                            balls.pop()
                    elif event.key == pygame.K_q:   # Change color of all balls on 'Q' key press
                        for ball in balls:
                            ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    elif event.key == pygame.K_UP:   # Increase bounce height on UP arrow key press
                        for ball in balls:
                            ball.bounce_height += 10
                    elif event.key == pygame.K_DOWN:   # Decrease bounce height on DOWN arrow key press
                        for ball in balls:
                            ball.bounce_height -= 10
                    elif event.key == pygame.K_LEFT:   # Increase x movement on LEFT arrow key press
                        for ball in balls:
                            ball.vx += 10 
                            print(f"Moving at {ball.vx} mm/s")
                    elif event.key == pygame.K_RIGHT:   # Decrease x movement on RIGHT arrow key press
                        for ball in balls:
                            ball.vx -= 10 
                            print(f"Moving at {ball.vx} mm/s")

            if not paused:   # Only update and draw balls if not paused
                for ball in balls:
                    ball.update(delta_time)

            screen.fill((0,0,0))  # Set background color to black

            for ball in balls:
                pygame.draw.circle(screen, ball.color, (ball.xpx, HEIGHT - ball.ypx), int(ball.radius))  

            pygame.display.flip()  

        except Exception as e:
            print(f"An error occurred: {e}")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    try:
       drop_height_input=int(input("Enter the drop height in mm (default is `250`): ") or "250")   
    except ValueError:
       drop_height_input=250

    main(drop_height_input)