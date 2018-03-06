# Imports
import pygame
from pygame.locals import *
import time
import random

pygame.init()
window_width = 600
window_height = 630

# Values
snake_color = (76, 154, 0)
food_color = (255, 0, 0)
white = (255, 255, 255)
message_bg_color = (0, 128, 255)
score_bg_color = (120, 120, 120)
square_size = 15

# Game
gameWindow = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Py Snake')
clock = pygame.time.Clock()

# Snake class
class Snake(object):
    def __init__(self):
        self.body = [[4, 4]]
        # Current direction snake is moving in
        self.curdir = None
        self.score = 0
        
        self.gameover = False
        self.moved = True

    def update(self, direction):
        self.curdir = direction

    # Moves snake
    # Takes in the current food position to check for collision.
    # Returns boolean value for whether food was eaten. 
    def move(self, food_pos):
        atefood = False
        if self.curdir:
            x, y = self.body[0]
        
            if self.curdir == 'up':
                self.body.insert(0, [x, y-1])
            elif self.curdir == 'down':
                self.body.insert(0, [x, y+1])
            elif self.curdir == 'right':
                self.body.insert(0, [x+1, y])
            elif self.curdir == 'left':
                self.body.insert(0, [x-1, y])

            self.check_gameover()

            if not self.gameover:
                # Check if ate food
                if self.body[0] == food_pos:
                    self.score += 1
                    atefood = True
                else:
                    # If food not eaten, then do not extend body
                    self.body.pop() 
                
                self.moved = True
            return atefood
                        
    def draw(self):
        for seg in self.body:
            pygame.draw.rect(gameWindow, snake_color, (seg[0]*square_size, seg[1]*square_size, square_size, square_size))

    def check_gameover(self):
        x, y = self.body[0]
        # Check out of bounds
        if x < 0 or x >= (window_width/square_size):
            self.gameover = True            
        if y < 2 or y >= (window_height/square_size):            
            self.gameover = True            

        # Check if collision with self
        if len(self.body) > 3:
            if self.body[0] in self.body[1:]:
                self.gameover = True                
                
# Food class
class Food(object):
    def __init__(self):
        self.position = [7, 7]
    
    def new_position(self, snake_body):
        x_max = (window_width / square_size) - 1
        y_max = (window_height / square_size) - 1        
        new_x = random.randint(0, x_max)
        new_y = random.randint(2, y_max)

        # Generate until food not on snake body
        while [new_x, new_y] in snake_body:
            new_x = random.randint(0, x_max)
            new_y = random.randint(2, y_max)            
        
        self.position = [new_x, new_y]        

    def draw(self):        
        pygame.draw.circle(gameWindow, food_color, (self.position[0]*square_size + 7, self.position[1]*square_size + 7), 7)

def score_label(score):
    font = pygame.font.SysFont(None, 40)    
    textSurf = font.render("Score: {}".format(score), True, white)

    pygame.draw.rect(gameWindow, score_bg_color, (0, 0, window_width, 30))
    gameWindow.blit(textSurf, (window_width - 145, 0))
    
def draw_gameover():
    font = pygame.font.SysFont(None, 60)

    condition = True
    while condition:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    condition = False
                    
        gameoverSurf = font.render("Game Over!", True, message_bg_color)
        gameoverSurf2 = font.render("Press R to Restart", True, message_bg_color)
        gameWindow.blit(gameoverSurf, (100, 210))
        gameWindow.blit(gameoverSurf2, (100, 260))
        
        pygame.display.update()
        
    loop() # Run the game loop again

# Game loop
def loop():
    snake = Snake()
    food = Food()
    food.new_position(snake.body)

    gameExit = False
    while not gameExit and not snake.gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                # Only allow update after snake has moved 1 space. Prevents 180 degree movement.
                if snake.moved: 
                    if event.key == pygame.K_UP and snake.curdir != 'down':
                        snake.update('up')
                    elif event.key == K_DOWN and snake.curdir != 'up':
                        snake.update('down')
                    elif event.key == K_RIGHT and snake.curdir != 'left':
                        snake.update('right')
                    elif event.key == K_LEFT and snake.curdir != 'right':
                        snake.update('left')
                    snake.moved = False

        gameWindow.fill(white)
        # snake.moved will be set to True when this runs
        ate = snake.move(food.position)
        if ate:
            food.new_position(snake.body)            

        # Draw should be done last
        snake.draw()
        food.draw()
        score_label(snake.score)
            
        pygame.display.update()
        clock.tick(8)        
            
    else: 
        draw_gameover()

# main
if __name__ == "__main__":
    loop()
    
