#!usr/bin/env python3

import sys
import os.path

def add_vertex(g,v):
    if v not in g:
        g[v] = {}

def read_people(filename):
    with open(filename + '.txt', "r") as f:
        g = {}
        num_people = int(f.readline())
        for i,row in zip(range(num_people), f):
            rnums = row.strip().split(" ")
            for j,col in zip(range(num_people), rnums):
                add_vertex(g,i)
                add_vertex(g,j)
                g[i][j] = col
    return g

def write_dot_graph(name,g):
    with open(name + '.dot','w') as f:
        f.write('graph ' + name + ' {') 
        for v, w in g.items():
            if v != None and w != None:
                f.write('"' + str(v) + '" -- "' + str(w) + '"')
        f.write('}')

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
    print(g)
    write_dot_graph(gname, g)

# Read in input txt and make an internal graph
# Check all 45 unique relationships and find the best score for each person
# Find the overall best score and place those two people across from each other
# Figure out how to add in host and guest checks
# Display output

if __name__ == '__main__':
    main()
