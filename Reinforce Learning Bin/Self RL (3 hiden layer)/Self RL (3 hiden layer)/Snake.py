import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# Initialize Pygame
pygame.init()
# Load the font for displaying the score
font = pygame.font.Font('assets/arial.ttf', 25)

# Define an Enum class to represent the snake's direction
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Define a namedtuple to represent a point on the game board
Point = namedtuple('Point', 'x, y')

# Define colors used in the game
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Define the size of each block in the game and speed(fps)
BLOCK_SIZE = 20
SPEED = 120

# Load and scale images for the apple and snake body parts
apple_img = pygame.image.load('assets/apple.png')
body_bottomleft_img = pygame.image.load('assets/body_bottomleft.png')
body_bottomright_img = pygame.image.load('assets/body_bottomright.png')
body_horizontal_img = pygame.image.load('assets/body_horizontal.png')
body_topleft_img = pygame.image.load('assets/body_topleft.png')
body_topright_img = pygame.image.load('assets/body_topright.png')
body_vertical_img = pygame.image.load('assets/body_vertical.png')
head_down_img = pygame.image.load('assets/head_down.png')
head_left_img = pygame.image.load('assets/head_left.png')
head_right_img = pygame.image.load('assets/head_right.png')
head_up_img = pygame.image.load('assets/head_up.png')
tail_down_img = pygame.image.load('assets/tail_down.png')
tail_left_img = pygame.image.load('assets/tail_left.png')
tail_right_img = pygame.image.load('assets/tail_right.png')
tail_up_img = pygame.image.load('assets/tail_up.png')
apple_img = pygame.transform.scale(apple_img, (BLOCK_SIZE, BLOCK_SIZE))
body_bottomleft_img = pygame.transform.scale(body_bottomleft_img, (BLOCK_SIZE, BLOCK_SIZE))
body_bottomright_img = pygame.transform.scale(body_bottomright_img, (BLOCK_SIZE, BLOCK_SIZE))
body_horizontal_img = pygame.transform.scale(body_horizontal_img, (BLOCK_SIZE, BLOCK_SIZE))
body_topleft_img = pygame.transform.scale(body_topleft_img, (BLOCK_SIZE, BLOCK_SIZE))
body_topright_img = pygame.transform.scale(body_topright_img, (BLOCK_SIZE, BLOCK_SIZE))
body_vertical_img = pygame.transform.scale(body_vertical_img, (BLOCK_SIZE, BLOCK_SIZE))
head_down_img = pygame.transform.scale(head_down_img, (BLOCK_SIZE, BLOCK_SIZE))
head_left_img = pygame.transform.scale(head_left_img, (BLOCK_SIZE, BLOCK_SIZE))
head_right_img = pygame.transform.scale(head_right_img, (BLOCK_SIZE, BLOCK_SIZE))
head_up_img = pygame.transform.scale(head_up_img, (BLOCK_SIZE, BLOCK_SIZE))
tail_down_img = pygame.transform.scale(tail_down_img, (BLOCK_SIZE, BLOCK_SIZE))
tail_left_img = pygame.transform.scale(tail_left_img, (BLOCK_SIZE, BLOCK_SIZE))
tail_right_img = pygame.transform.scale(tail_right_img, (BLOCK_SIZE, BLOCK_SIZE))
tail_up_img = pygame.transform.scale(tail_up_img, (BLOCK_SIZE, BLOCK_SIZE))

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        # Initialize the game window dimensions
        self.w = w
        self.h = h
        # Create a window for the game
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        # Initialize the game clock
        self.clock = pygame.time.Clock()
        # Reset the game to its initial state
        self.resetGame()
        
    def resetGame(self):
        # Reset the game state to its initial values
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        # Place the food at a random location on the game grid
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        # Ensure the food does not overlap with the snake
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        # Perform one step in the game
        self.frame_iteration += 1
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Move the snake
        self._move(action)
        self.snake.insert(0, self.head)

        # Check for game over conditions
        reward = -0.1  # small penalty for each step
        game_over = False

        if self.is_collision() or self.frame_iteration > 1000 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Check if the snake has eaten the food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()

        else:
            self.snake.pop()

        # Update the game UI
        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score
   
    def is_collision(self, pt = None):
        # Check if there is a collision with the walls or the snake's body
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False
        
    def _update_ui(self):
        # Update the game display
        self.display.fill(BLACK)
        
        # Draw the food
        self.display.blit(apple_img, (self.food.x, self.food.y))
        
        # Draw the snake
        for i, pt in enumerate(self.snake):
            if i == 0:  # Head of the snake
                self._draw_head(pt)
            elif i == len(self.snake) - 1:  # Tail of the snake
                self._draw_tail(pt)
            else:  # Body segments of the snake
                self._draw_body_segment(pt)
        
        # Display the score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [10, 10])
        pygame.display.flip()

    def _draw_head(self, pt):
        # Draw the head of the snake based on its direction
        if self.direction == Direction.DOWN:
            self.display.blit(head_down_img, (pt.x, pt.y))
        elif self.direction == Direction.UP:
            self.display.blit(head_up_img, (pt.x, pt.y))
        elif self.direction == Direction.LEFT:
            self.display.blit(head_left_img, (pt.x, pt.y))
        elif self.direction == Direction.RIGHT:
            self.display.blit(head_right_img, (pt.x, pt.y))

    def _draw_tail(self, pt):
        # Draw the tail of the snake based on its previous position
        prev_pt = self.snake[-2]
        if pt.x > prev_pt.x:  # Moving left
            self.display.blit(tail_right_img, (pt.x, pt.y))
        elif pt.x < prev_pt.x:  # Moving right
            self.display.blit(tail_left_img, (pt.x, pt.y))
        elif pt.y > prev_pt.y:  # Moving up
            self.display.blit(tail_down_img, (pt.x, pt.y))
        elif pt.y < prev_pt.y:  # Moving down
            self.display.blit(tail_up_img, (pt.x, pt.y))

    def _draw_body_segment(self, pt):
        # Draw the body segment of the snake based on its orientation
        prev_pt, next_pt = self.snake[self.snake.index(pt) - 1], self.snake[self.snake.index(pt) + 1]
        if prev_pt.x == next_pt.x:  # Vertical body segment
            self.display.blit(body_vertical_img, (pt.x, pt.y))
        elif prev_pt.y == next_pt.y:  # Horizontal body segment
            self.display.blit(body_horizontal_img, (pt.x, pt.y))
        elif (prev_pt.x < pt.x and next_pt.y < pt.y) or (next_pt.x < pt.x and prev_pt.y < pt.y):  # Top-left corner
            self.display.blit(body_topleft_img, (pt.x, pt.y))
        elif (prev_pt.x < pt.x and next_pt.y > pt.y) or (next_pt.x < pt.x and prev_pt.y > pt.y):  # Bottom-left corner
            self.display.blit(body_bottomleft_img, (pt.x, pt.y))
        elif (prev_pt.x > pt.x and next_pt.y < pt.y) or (next_pt.x > pt.x and prev_pt.y < pt.y):  # Top-right corner
            self.display.blit(body_topright_img, (pt.x, pt.y))
        elif (prev_pt.x > pt.x and next_pt.y > pt.y) or (next_pt.x > pt.x and prev_pt.y > pt.y):  # Bottom-right corner
            self.display.blit(body_bottomright_img, (pt.x, pt.y))
        
    def _move(self, action):
        # Define the clockwise order of directions
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        # Get the current direction index
        idx = clock_wise.index(self.direction)

        # Update the direction based on the action
        if np.array_equal(action, [1, 0, 0]):  # No change in direction
            new_dir = clock_wise[idx]

        elif np.array_equal(action, [0, 1, 0]):  # Turn right
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
            
        else:  # Turn left
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        # Update the snake's direction and position
        self.direction = new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)



