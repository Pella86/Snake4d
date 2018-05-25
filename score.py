# -*- coding: utf-8 -*-
"""
Created on Fri May 25 22:01:56 2018

@author: Mauro
"""
import datetime
import os
from tkinter import Frame, Label, StringVar, Toplevel

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

class Scores:
    def __init__(self):
        
        self.filename = "./score.txt"
        self.scores = []
        self.new_scores = []
        
        old_scores = []
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as f:
                old_scores = f.readlines()
        
        for line in old_scores:
            s = Score(line)
            self.scores.append(s)
        
        for score in self.scores:
            print(score)
        
    def add_score(self, score):
        self.new_scores.append(score)
    
    def write_scores(self):
        # append the new scores in the file
        with open(self.filename, "a") as f:
            f.write("\n")
            f.writelines([str(score) for score in self.new_scores])
        
        self.scores = self.scores + self.new_scores
        self.new_scores = []
      
    def get_top_ten_scores(self):
        all_scores = self.scores + self.new_scores
        
        all_scores = sorted(all_scores, key=lambda x : x.score)
        all_scores = all_scores[::-1]
        for score in all_scores:
            print(score)
        
        return all_scores[:10]


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
                
        print(label_list)

        # score list
        # take highest score
        hscore = top_ten[0].score
        # get the character width
        cwidth_score = len(str(hscore))
        # construct the format
        format_score = "{: >" +  str(cwidth_score) + "}"
        
        for i, ss in enumerate(label_list):
            s = ""
            for score_line in ss:
                # print the formatted score
                fscore = format_score.format(score_line.score)
                # assemble the formatted string with date and score
                s += score_line.date.strftime("%d %b %y") + " - " + fscore + "\n" 
            s = s[:len(s)-1]
            
            if i == 1:
                color = "darkorange3"
                rel = "groove"
            else:
                color = "green"
                rel = "flat"
            
            ltop_board = Label(board, text=s, font=("Fixedsys", 14), fg = color,
                               borderwidth=2, relief=rel, padx=1, pady=1)
            
            ltop_board.grid(row=(i + 1), column = 0,padx=0, pady=0)            
            
            
            
        
        # scroll the top ten list
        # if last score == one of the scores
        # append to score table labels
        # append the [string]
        # continue in a new new_score label
        

#        s = ""
#        for score in top_ten:
#            # construct the format
#            format_score = "{: >" +  str(cwidth_score) + "}"
#            # print the formatted score
#            fscore = format_score.format(score.score)
#            # assemble the formatted string with date and score
#            s += score.date.strftime("%d %b %y") + " - " + fscore + "\n"
#        
#        
#        ltop_board = Label(board, text=s, font=("Fixedsys", 14), fg = "green" )
#        ltop_board.pack()
        
        # graph sort by date, take last 30 time points
        # plot xy in a 2d polygon, render it 
        