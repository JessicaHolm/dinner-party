#!usr/bin/env python3

import sys
import os.path
from random import randrange

def read_people(filename):
    with open(filename + '.txt', "r") as f:
        num_people = int(f.readline())
        g = [[0] * num_people for _ in range(num_people)]
        for i,row in zip(range(num_people), f):
            rnums = row.strip().split(" ")
            for j,col in zip(range(num_people), rnums):
                num = int(col)
                g[i][j] = num
    x = 0
    for i in range(len(g)):
        for j in range(x,10):
            g[i][j] = g[i][j] + g[j][i]
            g[j][i] = g[i][j]
        x = x + 1
    return g

def solve_random(g):
    x = 0
    sol = {}
    while len(sol) < 10:
        i = randrange(10)
        j = randrange(10)
        if i not in sol:
            sol[i] = x
            x = x + 1
    return sol 


def usage():
    print('usage: python3 dinner.py hw1-inst1.txt')
    exit(0)

def main():
    if len(sys.argv) < 2: usage()
    f = sys.argv[1]
    gname,kind = os.path.splitext(f)
    if kind == '.txt':
        g = read_people(gname)
    else: usage()
    sol = solve_random(g)
    for p,s in sol.items():
        print(p, s)
        
    # write_dot_graph(gname, g)

# Read in input txt and make an internal graph
# Check all 45 unique relationships and find the best score for each person
# Find the overall best score and place those two people across from each other
# Figure out how to add in host and guest checks
# Display output

if __name__ == '__main__':
    main()
