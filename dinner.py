#!usr/bin/env python3

# Read in and solve a instance of dinner party.

import sys
import os.path
from random import randrange
from collections import defaultdict

class Table(object):

    # Create the scoring matrix.
    def __init__(self, filename):
        with open(filename + '.txt', "r") as f:
            n = int(f.readline())
            g = [[0] * n for _ in range(n)]
            for i,row in zip(range(n), f):
                rnums = row.strip().split(" ")
                for j,col in zip(range(n), rnums):
                    num = int(col)
                    g[i][j] = num

        # Make the matrix symmetric.
        x = 0
        for i in range(n):
            for j in range(x,n):
                g[i][j] = g[i][j] + g[j][i]
                g[j][i] = g[i][j]
            x = x + 1

        # Initialize variables.
        self.n = n
        self.half = int(n/2)
        self.g = g
        self.seated = []
    
    # Place people in seats randomly.
    def solve_random(self):
        soln = defaultdict(list)
        while len(soln) < self.n:
            p = randrange(self.n)
            if p not in self.seated:
                self.create_solution(soln, p)
        return soln

    # Randomly choose one person for the first seat then
    # find their best match, place them next to the first
    # person and continue the process until finished.
    def solve_greedy(self):
        soln = defaultdict(list)
        p = randrange(self.n)
        while len(soln) < self.n:
            p = self.find_best_neighbor(p)
            self.create_solution(soln, p)
        return soln

    # Adds people to the final solution table.
    def create_solution(self, soln, p):
        # First seat.
        if len(soln) == 0:
            soln[p].append(None)
            soln[p].append(None)
        # Seats 1..n/2 or the rest of the first row of seats.
        elif len(soln) < self.half:
            soln[p].append(self.seated[len(self.seated)-1])
            soln[p].append(None)
        # Seat n/2+1 or the first seat of the second row.
        elif len(soln) == self.half:
            soln[p].append(None)
            soln[p].append(self.seated[0])
        # Seats n/2+2..n or the rest of the second row.
        else:
            soln[p].append(self.seated[len(self.seated)-1])
            soln[p].append(self.seated[len(self.seated)-self.half])
        self.seated.append(p)

    # Finds the index of the passed in person's highest match 
    # according to the preference matrix
    def find_best_neighbor(self, p):
        largest = float('-inf')
        largest_index = 0
        for num in self.g[p]:
            # Get index for current num or multiple indexes if
            # there are duplicate numbers in a row
            gene = (i for i, n in enumerate(self.g[p]) if n == num)
            for i in gene:
                # Only check the indexes of people not already seated
                if i not in self.seated:
                    if num > largest:
                        largest = num
                        largest_index = i
        return largest_index
                
    # Scores a table based on where people are sitting.
    def find_score(self, soln):
        score = 0
        for p, seated in soln.items():
            for r in seated:
                if r is not None:
                    if (p < (self.half) and r >= (self.half)) or (p >= (self.half) and r < (self.half)):
                        # A host and a guest are sitting next to each other.
                        if r == seated[0]:
                            score += 1
                        # A host and a guest are sitting across from each other.
                        elif r == seated[1]:
                            score += 2
                    # Add points according to the preference matrix.
                    score += self.g[p][r]
        return score
    
    # Shows the score and solution table.
    def display_output(self, soln):
        score = self.find_score(soln)
        print("Score: {}\n".format(score))

        for i,p in zip(range(self.n), soln.keys()):
            print("{} {}".format(p+1,i+1))

        strl = ",".join(map(str, list(soln.keys()))).split(",")
        for i in range(0,2):
            print(" ".join(strl[i*(self.half):(i+1)*(self.half)]) + "\n")

def usage():
    print('usage: python3 dinner.py filename solver\n\nfilenames: {hw1-inst1.txt, hw1-inst2.txt, hw1-inst3.txt}\nsolvers: {random, greedy)')
    exit(0)

if len(sys.argv) < 3: usage()
filename = sys.argv[1]
solver = sys.argv[2]
gname,kind = os.path.splitext(filename)
if kind == '.txt':
    t = Table(filename=gname)
else: usage()
if solver == 'random':
    soln = t.solve_random()
elif solver == 'greedy':
    soln = t.solve_greedy()
else: usage()

t.display_output(soln)
