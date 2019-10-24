#!usr/bin/env python3

# Read in and solve a instance of dinner party.
# Inspired by https://github.com/pdx-cs-ai/slider 

import sys
import os.path
import random

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
        self.table = list(range(n))
        random.shuffle(self.table)

    # List of moves possible by switching 2 people at the table.
    def moves(self):
        n = self.n
        ms = []
        for i in range(n):
            for j in range(i+1,n):
                t = (i, j)
                ms.append(t)
        return ms
            
    # Switch 2 people at the table.
    def move(self, m):
        (i, j) = m
        tmp = self.table[i]
        self.table[i] = self.table[j]
        self.table[j] = tmp

    # Get the score of the current state.
    def check_score(self):
        score = 0     
        n = self.n
        g = self.g
        half = self.half
        table = self.table
        for i,p in zip(range(n-1), table):
            if i == half-1:
                p1 = p
            else:
                p1 = table[i+1]
            if i >= n/2:
                p2 = p
            else:
                p2 = table[i+(half)]
            score = score + g[p][p1] + g[p][p2]
            if (p <= 4 and p1 > 4) or (p > 4 and p1 <= 4):
                score += 1
            if (p <= 4 and p2 > 4) or (p > 4 and p2 <= 4):
                score += 2
        return score
    
    # Randomly search through the state space.
    def solve_random(self, nsteps):
        soln = []

        for _ in range(nsteps):
            # Check if at optimal score
            if self.check_score() == 100:
                return soln
            ms = self.moves()
            mnv = []
            for m in ms:
                # Do-undo.
                (f, t) = m
                self.move((f, t))
                mnv.append(m)
                self.move((t, f))

            if mnv:
                m = random.choice(mnv)
            else:
                m = random.choice(ms)
            
            soln.append(m)
            self.move(m)

        return soln

    # Local search through the state space choosing the state
    # that has the largest score each time through the loop.
    def solve_local(self, nsteps):
        soln = []

        for _ in range(nsteps):
            ms = self.moves()
            mnv = []

            for m in ms:
                # Do-undo.
                (f, t) = m
                self.move((f, t))
                c = self.check_score()
                mnv.append((c, m))
                self.move((t, f))

            mc = max(mnv, key=lambda m: m[0])
            ms = [m[1] for m in mnv if m[0] == mc[0]]
            m = random.choice(ms)
            soln.append(m)
            self.move(m)

        return soln

    # Shows the score and solution table.
    def display_output(self, soln):
        score = self.check_score()
        print("Score: {}\n".format(score))

        for i,p in zip(range(self.n), self.table):
            print("{} {}".format(p+1,i+1))

        strl = ",".join(map(str, list(self.table))).split(",")
        for i in range(0,2):
            print(" ".join(strl[i*(self.half):(i+1)*(self.half)]) + "\n")

        # print("Solution length: {}".format(len(soln)))

def usage():
    print('usage: python3 dinner.py filename solvern nsteps\n\nsolvers: {random, local)')
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
    soln = t.solve_local(nsteps)
else: usage()

t.display_output(soln)
