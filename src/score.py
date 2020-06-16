# -*- coding: utf-8 -*-
"""
Created on Fri May 25 22:01:56 2018

@author: Mauro
"""
#==============================================================================
# Imports
#==============================================================================

# py imports
import datetime
from tkinter import Label, Toplevel
import os

# project imports
import visu, poly, vec #needed for the graph

# =============================================================================
# Score data structure
# =============================================================================

class Score:
    ''' Class representing a score, which is a date and a integer'''
    
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
    
    def __hash__(self):
        return hash((self.date, self.score))
    
    def __eq__(self, rhs):
        return self.score == rhs.score and self.date == rhs.date
    
    def __str__(self):
        s = self.date.isoformat() + " "
        s += str(self.score)
        return s

  
class Scores:
    
    ''' A list of scores
    the class manages the reading and writing to file of the scores and the
    sorting of different scores
    '''
    
    def __init__(self):
        
        # put the score file in the settings and untrack it from git
        self.filename = "./settings/scores.txt"
        
        self.scores = []
        
        # number of scores kept between max scores and recent scores
        self.keep_scores = 20
        
        self.last_score = None
        
        # reads the file and appends the scores
        self.read_scores()


    def read_scores(self):
        self.scores = []
        
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as f:
                lines = f.readlines()
        
            for line in lines:
                s = Score(line)
                self.scores.append(s)
    
    def add_score(self, score):
        self.scores.append(score)
        self.last_score = score
        
    def sort_by_score(self, limit):
        scores = sorted(self.scores, key=lambda s : s.score, reverse=True)
        return scores[:limit]
    
    def sort_by_date(self, limit):
        scores = sorted(self.scores, key=lambda s : s.date, reverse=True)
        return scores[:limit]
    
    def write_scores(self):
        # keep the last 20 scores and the best 20 scores
        best_scores = self.sort_by_score(self.keep_scores)
        recent_scores = self.sort_by_date(self.keep_scores)
        
        # make sure no duplicate score is reported
        scores = set(best_scores + recent_scores)
        
        # write the date and score on a new line
        with open(self.filename, "w") as f:
            f.writelines([str(score) + "\n" for score in scores])
            
    def get_top_ten_scores(self):
        return self.sort_by_score(10)
    
    # gets the last 20 scores in order of time
    def get_last_scores(self):
        return self.sort_by_date(20)

# =============================================================================
# Class Score Board - GUI    
# =============================================================================

class ScoreBoard:
    
    ''' The GUI representation of the class scores '''
    
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
        
        # score list
        # take highest score
        hscore = top_ten[0].score
        # get the character width
        cwidth_score = len(str(hscore))
        # construct the format so that the highest score will give the spacing
        format_score = "{: >" +  str(cwidth_score) + "}"   
        
        for i, score in enumerate(top_ten):
            
            # format the scores and date
            date_str = score.date.strftime("%d %b %y")
            fscore = format_score.format(score.score)

            s = f"{date_str} - {fscore}"
            
            # if the score is the last obtained color it in orange
            if score == self.scores.last_score:
                color = "darkorange3"
                rel = "groove"
            else:
                color = "green"
                rel = "flat"                
            
            ltop_board = Label(board, text=s, font=("Fixedsys", 14), fg = color,
                               borderwidth=2, relief=rel, padx=1, pady=1)
            
            ltop_board.grid(row=(i + 1), column = 0, padx=0, pady=0)             
        
        #in case needed is a graph of the scores        
        graph = visu.VisuArea(board, None, [250, 100], "Score Evolution")
        graph.fP.grid(row=0, column = 1, rowspan=len(top_ten))
        
        graph.c_center_w = 0
        graph.c_center_h = 0
        
        p = poly.Polygon()
        
        # get the scores
        score_list = self.scores.get_last_scores()
        score_list = score_list[::-1]
        
        # for each score create a point
        point_list = []
        for i, score in enumerate(score_list):
            v = vec.V2(i, score.score)
            point_list.append(v)        
        
        # determine the height of the graph
        p_max = max(point_list, key= lambda polygon : polygon.y())
        graph.area_h = p_max.y() + p_max.y() * 0.15
        graph.area_w = len(score_list)
        
        # construct the line using the polygon class
        e_list = []
        for i, p in enumerate(point_list[:-1]):
            e_list.append([i, i + 1])
        
        p.v_list = point_list
        p.e_list = e_list
        p.color = "red"
        
        graph.draw_poly(p)
        # add axis
        graph.draw_edge(vec.V2(0, graph.area_h), vec.V2(graph.area_w, graph.area_h), kwargs={"fill":"black"})
        
        # write a label reporting the max score
        graph.canvas.create_text(5, p_max.y(), 
                                 text= "Max score: " + str(p_max.y()),
                                 anchor= "w")
            
            
            
            
        
  
        