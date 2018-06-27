# -*- coding: utf-8 -*-
"""
Created on Fri May 25 22:01:56 2018

@author: Mauro
"""
#==============================================================================
# Score board
#==============================================================================

import datetime
import os
from tkinter import Label, Toplevel
#import visu, poly, vec #needed for the graph

#==============================================================================
# Class score
#   small class to store a score and a date
#==============================================================================
class Score:
    def __init__(self, date, score = None):
        if type(date) == str:
            self.read_from_line(date)
        elif type(date) is datetime.datetime and type(score) is int:
            self.date = date
            self.score = score
        else:
            raise ValueError("wrong parameters: " + str(date) + ", " + str(score))
    
    def read_from_line(self, line):
        data = line.split(" ")
        self.date = datetime.datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S.%f")
        self.score = int(data[1])
    
    def __str__(self):
        s = self.date.isoformat() + " "
        s += str(self.score)
        return s

#==============================================================================
# A list of scores
#    the class manages the reading and writing to file of the scores and the
#   sorting of different scores
#==============================================================================

class Scores:
    def __init__(self):
        
        self.filename = "./score.txt"
        self.scores = []
        self.new_scores = []
        
        # read in from the score file the scores
        old_scores = []
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as f:
                old_scores = f.readlines()
        
        # parse the line in scores
        for line in old_scores:
            s = Score(line)
            self.scores.append(s)
        
        print("Loaded", len(self.scores), "scores")
        
    def add_score(self, score):
        self.new_scores.append(score)
    
    def write_scores(self):
        # append the new scores in the file
        with open(self.filename, "a") as f:
            f.write("\n")
            f.writelines([str(score) for score in self.new_scores])
        
        self.scores = self.scores + self.new_scores
        self.new_scores = []
      
    # get the top ten scores in terms of score
    def get_top_ten_scores(self):
        all_scores = self.scores + self.new_scores
        
        all_scores = sorted(all_scores, key=lambda x : x.score)
        all_scores = all_scores[::-1]
        
        return all_scores[:10]
    
    # gets the last 20 scores in order of time
    def get_last_scores(self):
        all_scores = self.scores + self.new_scores
        
        all_scores = sorted(all_scores, key=lambda x : x.date)
        all_scores = all_scores[::-1]
        return all_scores[:20]

#==============================================================================
# The GUI representation of the class scores        
#==============================================================================

class ScoreBoard:
    
    def __init__(self, parent):
        self.parent = parent
        self.scores = Scores()
    
    def add_score(self, score):
        self.scores.add_score(score)
        self.scores.write_scores()
        
    def render_scores(self):
        board = Toplevel(self.parent)

        # title lable 
        titlel = Label(board, text = "---- HIGH SCORE ----", font=("Arial", 20))
        titlel.grid(row = 0, column = 0)
        
        # get top ten
        top_ten =  self.scores.get_top_ten_scores()
       
        # get last score
        if self.scores.new_scores:
            last_score = self.scores.new_scores[0]
        elif self.scores.scores:
            last_score = self.scores.scores[-1]
        
        # create a list from the scores, if the last score is in the list
        # split the list according to previous score - curr score - prev score
        label_list = []
        label_list.append([])
        idx = 0
        for score in top_ten:
            
            if score.date == last_score.date and score.score == last_score.score:
                label_list.append([])
                idx += 1
                label_list[idx].append(score)
                label_list.append([])
                idx += 1
            else:
                label_list[idx].append(score)

        # score list
        # take highest score
        hscore = top_ten[0].score
        # get the character width
        cwidth_score = len(str(hscore))
        # construct the format
        format_score = "{: >" +  str(cwidth_score) + "}"
        
        # *BUG* if is first or last in the list magics happen...
        for i, ss in enumerate(label_list):
            s = ""
            for score_line in ss:
                # print the formatted score
                fscore = format_score.format(score_line.score)
                # assemble the formatted string with date and score
                s += score_line.date.strftime("%d %b %y") + " - " + fscore + "\n" 
            s = s[:len(s)-1]
            
            if (i == 1 and len(ss) == 3) or (i == 0 and len(ss) == 2):
                color = "darkorange3"
                rel = "groove"
            else:
                color = "green"
                rel = "flat"
            
            ltop_board = Label(board, text=s, font=("Fixedsys", 14), fg = color,
                               borderwidth=2, relief=rel, padx=1, pady=1)
            
            ltop_board.grid(row=(i + 1), column = 0, padx=0, pady=0) 

#        in case needed is a graph of the scores        
#
#
#        row = len(label_list) + 1
#        
#        graph = visu.VisuArea(board, None, [250, 100], "Score Evolution")
#        graph.fP.grid(row=row, column = 0)
#        
#        graph.c_center_w = 0
#        graph.c_center_h = 0
#        
#        p = poly.Polygon()
#        
#        score_list = self.scores.get_last_scores()
#        score_list = score_list[::-1]
#        
#        point_list = []
#        for i, score in enumerate(score_list):
#            print(score.score)
#            v = vec.V2(i, score.score)
#            point_list.append(v)        
#        
#        p_max = max(point_list, key= lambda polygon : polygon.y())
#        graph.area_h = p_max.y() + 2
#        graph.area_w = len(score_list)
#        
#        e_list = []
#        for i, p in enumerate(point_list[:-1]):
#            e_list.append([i, i + 1])
#        
#        p.v_list = point_list
#        p.e_list = e_list
#        p.color = "red"
#        
#        graph.draw_poly(p)
#        graph.draw_edge(vec.V2(0, graph.area_h), vec.V2(graph.area_w, graph.area_h), kwargs={"fill":"black"})
#        graph.canvas.create_text(5, p_max.y(), text= str(p_max.y()), anchor= "w")
            
            
            
            
        
  
        