# -*- coding: utf-8 -*-
"""
Created on Tue May 22 22:15:01 2018

@author: Mauro
"""

import snake, poly, vec
import random

class GameEngine:
    
    def __init__(self):
        self.snake = snake.Snake()
        
        # create bbox
        self.bbox_size = 3
        
        self.bbox = poly.create_cube4d(vec.V4(0, 0, 0, 0), self.bbox_size * 2, "black")
        
        
        self.food = self.initialize_food()
        
        self.state = "run"
        
        self.score = 0
        
        self.p_list = []
        self.generate_plist()
    
    def generate_plist(self):
        self.p_list = []
        # add the bbox
        self.p_list.append(self.bbox)
        
        # add the food
        self.p_list.append(self.food)
        
        # add the snake cubes
        for cube in self.snake.p_list:
            self.p_list.append(cube)
    
    def initialize_food(self):
        # give random coords
        def generate_rand_point():
            coords = []
            for i in range(4):
                coords.append(random.randrange(-self.bbox_size, self.bbox_size))
            return vec.V4(coords)
        
        redo = True
        while redo:
            
            food_point = generate_rand_point()
            redo = False
            
            for p in self.snake.p_list:
                if self.intersect(food_point, p):
                    redo = True
                    break   
        print("new food at", food_point)
        return poly.create_cube4d(food_point, 1, "blue")
    
    
    def intersect(self, point, polygon):
        # the polygon stores the biggest and smallest vertex in the first 2
        # is dependent on the create cube function tho...
        
        pbbox_low = polygon.v_list[0]
        pbbox_high = polygon.v_list[1]
        
        for i in range(4):
            if not (point[i] > pbbox_low[i] and point[i] < pbbox_high[i]):
                return False
        return True
    
    def check_collision(self, snake_dir):
        self.snake.move(snake_dir)
        
        if not self.intersect(self.snake.head_pos, self.bbox):
            return "out_bbox"
        
        if self.intersect(self.snake.head_pos, self.food):
            return "food"
        
        for p in self.snake.p_list:
            if self.intersect(self.snake.head_pos, p):
                return "snake"
    
    def evaluate_collision(self, collision):
        
        if collision == "out_bbox" or collision == "snake":
            self.state = "game_over"
            
        elif collision == "food":
            self.snake.add_segment()
            self.food = self.initialize_food()
            self.score += 1
        
    def routine(self):
        c = self.check_collision(self.snake.head_dir)
        self.evaluate_collision(c)
        self.generate_plist()
        
        
            