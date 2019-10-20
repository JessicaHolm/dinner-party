#!usr/bin/env python3

import sys
import os.path
from random import randrange
from collections import defaultdict

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
        for j in range(x,num_people):
            g[i][j] = g[i][j] + g[j][i]
            g[j][i] = g[i][j]
        x = x + 1
    return g

def solve_random():
    sol = defaultdict(list)
    p_list = []
    while len(sol) < 10:
        p = randrange(10)
        if p not in p_list:
            if len(sol) == 0:
                sol[p].append(None)
                sol[p].append(None)
            elif len(sol) < 5:
                sol[p].append(p_list[len(p_list)-1])
                sol[p].append(None)
            elif len(sol) == 5:
                sol[p].append(None)
                sol[p].append(p_list[0])
            else:
                sol[p].append(p_list[len(p_list)-1])
                sol[p].append(p_list[len(p_list)-5])
            p_list.append(p) 
    return sol 

def solve_heur(g):
    sol = defaultdict(list)
    p_list = []
    p = randrange(10)
    while len(sol) < 10:
        p = find_best_neighbor(g, p, p_list)
        if len(sol) == 0:
            sol[p].append(None)
            sol[p].append(None)
        elif len(sol) < 5:
            sol[p].append(p_list[len(p_list)-1])
            sol[p].append(None)
        elif len(sol) == 5:
            sol[p].append(None)
            sol[p].append(p_list[0])
        else:
            sol[p].append(p_list[len(p_list)-1])
            sol[p].append(p_list[len(p_list)-5])
        p_list.append(p) 
    return sol 

def find_best_neighbor(g, p, p_list):
    largest = -427386
    largest_index = 0
    for num in g[p]:
        gene = (i for i, n in enumerate(g[p]) if n == num)
        for i in gene:
            if i not in p_list:
                if num > largest:
                    largest = num
                    largest_index = i
    return largest_index
            

def find_score(g, sol):
    score = 0
    for p, p_list in sol.items():
        for r in p_list:
            if r is not None:
                if (p < 5 and r >= 5) or (p >= 5 and r < 5):
                    if r == p_list[0]:
                        score += 1
                    elif r == p_list[1]:
                        score += 2
                score += g[p][r]
    return score

def display_table(sol):
    strl = ",".join(map(str, list(sol.keys()))).split(",")
    for i in range(0,2):
        print(" ".join(strl[i*5:(i+1)*5]) + "\n")


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
    # sol = solve_random()
    sol = solve_heur(g)
    # for row in g:
    #     print(row)
    score = find_score(g, sol)
    print("Score: {}\n".format(score))
    for p,s in sol.items():
        print(p, s)
    print("\n")
    display_table(sol)

if __name__ == '__main__':
    main()
