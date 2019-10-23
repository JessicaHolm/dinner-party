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
        for i in range(n):
            for j in range(i,n):
                g[i][j] = g[i][j] + g[j][i]
                g[j][i] = g[i][j]

        # Initialize variables.
        self.n = n
        self.g = g
        self.half = int(n/2)
        self.table = [0,1,2,3,4,5,6,7,8,9]
        self.seated = []

    def moves(self):
        n = self.n
        ms = []
        for i in range(n):
            for j in range(i+1,n):
                t = (i, j)
                ms.append(t)
        return ms
            
    def move(self, m):
        (i, j) = m
        self.table[i] = j
        self.table[j] = i
    
    # Place people in seats randomly.
    def solve_random(self, nsteps):
        for _ in range(nsteps):
            soln = defaultdict(list)
            self.seated = []
            while len(soln) < self.n:
                p = randrange(self.n)
                if p not in self.seated:
                    self.create_solution(soln, p)
            score = self.find_score(soln)
            if score == 100:
                print("Score: {}\n".format(score))
        return soln

    def solve_local(self, nsteps):
        soln = defaultdict(list)
        
        for _ in range(nsteps):
            moves = self.moves()

            mnv = []
            for m in ms:
                # Do-undo.
                (f, t) = m
                self.move((f, t))
                self.move((t, f))
        
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

        # Cite source.
        strl = ",".join(map(str, list(soln.keys()))).split(",")
        for i in range(0,2):
            print(" ".join(strl[i*(self.half):(i+1)*(self.half)]) + "\n")

def usage():
    print('usage: python3 dinner.py filename solver\n\nfilenames: {hw1-inst1.txt, hw1-inst2.txt, hw1-inst3.txt}\nsolvers: {random, local)')
    exit(0)

if len(sys.argv) != 4: usage()
filename = sys.argv[1]
solver = sys.argv[2]
nsteps = int(sys.argv[3])
gname,kind = os.path.splitext(filename)
if kind == '.txt':
    t = Table(filename=gname)
else: usage()
if solver == 'random':
    soln = t.solve_random(nsteps)
elif solver == 'local':
    soln = t.solve_local()
else: usage()

# t.display_output(soln)
