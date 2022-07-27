from heapq import heappop, heappush
import subprocess as sp
from time import sleep
import sys
import os


def clear_screen():
    sp.call('cls',shell=True) #for windows to relace CLEAR with CLS

def heuristic_func(cell, goal):
    temp_cell  = float("inf")
    for element in goal:
        if temp_cell  > (abs(cell[0] - element[0]) + abs(cell[1] - element[1])):
            temp_cell  = abs(cell[0] - element[0]) + abs(cell[1] - element[1])
    return temp_cell 

def maze_to_graph(maze):
    #define the sizes of the maze
    height = len(maze)
    width = len(maze[0]) if height else 0 #dummy check if the maze is empty

    #make a dictionary of the maze
    graph = {}
    for j in range(width):
        for i in range(height):
            if maze[i][j] == 32 or maze[i][j] == 80 or maze[i][j] == 46:
                graph[(i, j)] = []

    goal = set()
    for row, col in graph.keys():
        #defining start and end of the maze
        if maze[row][col] == 80:
            start = (row, col)
        if maze[row][col] == 46:
            temp_cell  = (row, col)
            goal.add(temp_cell )
    #adding the neighbours to each index in the dicitonary
        if row < height - 1 and (maze[row + 1][col] == 32 or maze[row + 1][col] == 80 or maze[row + 1][col] == 46):
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and (maze[row][col + 1] == 32 or maze[row][col + 1] == 80 or maze[row][col + 1] == 46):
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph, start, goal

def print_maze(path,start,cost,maze):
    (Vy, Vx) = start
    sleep(0.01)
    path_cost = 0
    clear_screen()
    sleep(0.00001)
    if path != "" and cost != 0:
        for direction in range(len(path)):
            for index in graph[(Vy, Vx)]:
                if index[0] == path[direction]:
                    Maze[Vy][Vx] = 46
                    (Vy, Vx) = index[1]
                    Maze[Vy][Vx] = 64
                    path_cost += 1 
                    sleep(0.01)
                    clear_screen()
                    sleep(0.00001)
                    for line in Maze:
                        print(bytes(line))

        print("path: ",path,end='\n')
        print("path cost: ",path_cost,end='\n')
        print("nodes expanded: ",cost,end='\n')
    else:
        for line in Maze:
            print(bytes(line))
            

def astar_path_find(maze):
    graph, start, goal = maze_to_graph(maze)
    pr_queue = []
    costs = 0
    heappush(pr_queue, (heuristic_func(start, goal), 0, "", start))
    visited_nodes = set()
    complete_path = ""
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if len(goal) == 0:
            return complete_path,costs,start,graph

        if current in goal:
            complete_path = complete_path + path
            goal.remove(current)
            visited_nodes.clear()
            costs = costs + 1
            visited_nodes.add(current)
            (Vy,Vx) = current
            pr_queue.clear()
            for direction, neighbour in graph[current]:
                heappush(pr_queue, (cost + heuristic_func(neighbour, goal), cost + 1,
                                    "" + direction, neighbour))
            continue
        if current in visited_nodes:
            continue
        costs = costs + 1
        visited_nodes.add(current)
        (Vy,Vx) = current
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + heuristic_func(neighbour, goal), cost + 1,
                                path + direction, neighbour))
    return "NO WAY!",0,start,graph

user_input = input("Enter the path of your file: \n")
assert os.path.exists(user_input), "I did not find the file at, "+str(user_input)
MazeFile = open(user_input,'rb')
Maze = []
for line in MazeFile.readlines():
    Maze.append(list(line.strip()))

path, cost, (Vy, Vx), graph = astar_path_find(Maze)
print_maze(path,(Vy,Vx),cost,Maze)
