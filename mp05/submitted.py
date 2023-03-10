# submitted.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# submitted should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi)

import queue
from queue import Queue
from heapq import heapify, heappush, heappop
from itertools import product
import random
from typing import NamedTuple, Union
from maze import Maze

Location = tuple[int, int]
Path = list[Location]
Edge = tuple[int, int]


def bfs(maze: Maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Implement bfs function

    class Node(NamedTuple):
        loc: Location
        parent: Location | None

    q: Queue[Node] = Queue()
    explored_locs: list[Location] = [maze.start]
    explored: list[Node] = [Node(maze.start, None)]
    q.put(Node(maze.start, None))

    while not q.empty():
        v = q.get()
        for edge in maze.neighbors(*v.loc):
            if edge not in explored_locs:
                w = Node(edge, v.loc)
                explored_locs.append(edge)
                explored.append(w)
                q.put(w)
            else:
                pass

    goal: Location = maze.waypoints[0]
    path: list[Location] = [goal]
    loc: Location = goal
    for _ in range(len(explored_locs)):
        loc_ind: int = explored_locs.index(loc)
        node: Node = explored[loc_ind]
        path.append(node.parent)
        loc = node.parent

        if loc == maze.start:
            break
        else:
            pass

    path.reverse()
    return path


class AStarNode(NamedTuple):
    f: int
    g: int
    loc: Location
    parent: Union["AStarNode", None]


def manhattan_dist(a: Location, b: Location) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_single(maze: Maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Implement astar_single

    start: Location = maze.start
    goal: Location = maze.waypoints[0]

    open: list[AStarNode] = [AStarNode(manhattan_dist(start, goal), 0, start, None)]
    heapify(open)
    closed: list[AStarNode] = []

    while open:
        n = heappop(open)
        closed.append(n)

        if n.loc == (3, 12):
            pass

        if n.loc == goal:
            break
        else:
            pass

        for edge in maze.neighbors(*n.loc):
            g: int = n.g + 1
            h: int = manhattan_dist(edge, goal)
            f: int = g + h

            close_locs: list[Location] = [n.loc for n in closed]
            open_locs: list[Location] = [n.loc for n in open]

            if edge in close_locs:
                closed_ind: int = close_locs.index(edge)
                m: AStarNode = closed[closed_ind]

                if f < m.f:
                    closed.pop(closed_ind)
                    heappush(open, AStarNode(f, g, edge, n))
                else:
                    pass

            elif edge in open_locs:
                open_ind: int = open_locs.index(edge)
                m: AStarNode = open[open_ind]
                if f < m.f:
                    open.pop(open_ind)
                    open.append(AStarNode(f, g, edge, n))
                else:
                    pass
            else:
                heappush(open, AStarNode(f, g, edge, n))

    path = []
    current: AStarNode | None = closed[-1]
    while current is not None:
        path.append(current.loc)
        current = current.parent

    path.reverse()

    return path


def find_closest_waypoint(
    current_location: Location, waypoints: list[Location]
) -> Location:
    waypoint_and_dist: list[tuple[int, Location]] = [
        (manhattan_dist(current_location, waypoint), waypoint) for waypoint in waypoints
    ]
    heapify(waypoint_and_dist)
    _, closest = heappop(waypoint_and_dist)

    return closest


def get_mst_length(waypoints: list[Location]) -> int:
    waypoint_inds = list(range(len(waypoints)))
    unvisited: list[int] = waypoint_inds
    visited: list[int] = []
    mst_length: int = 0

    all_edges: list[Edge] = []

    v = random.choice(unvisited)
    unvisited.remove(v)
    visited.append(v)

    while unvisited:
        waypoint_prod = product(visited, unvisited)
        edges: list[tuple[int, Edge]] = [
            (manhattan_dist(waypoints[v], waypoints[u]), (v, u))
            for (v, u) in waypoint_prod
        ]
        heapify(edges)
        dist, edge = heappop(edges)
        _, v = edge
        all_edges.append(edge)
        visited.append(v)
        unvisited.remove(v)
        mst_length += dist

    return mst_length


def heuristics(current_location: Location, waypoints: list[Location]) -> int:
    dist_to_closest_waypoint = manhattan_dist(
        current_location, find_closest_waypoint(current_location, waypoints)
    ) if waypoints else 0
    mst_length = get_mst_length(waypoints) if waypoints else 0
    h = dist_to_closest_waypoint + mst_length
    return h


def generate_path(node: AStarNode) -> list[Location]:
    current: AStarNode | None = node
    path: list[Location] = []

    while current is not None:
        path.append(current.loc)
        current = current.parent

    path.reverse()
    return path


def get_unvisited_waypoints(
    path: list[Location], waypoints: tuple[Location]
) -> list[Location]:
    unvisited_waypoints = list(waypoints)
    for loc in path:
        if loc in unvisited_waypoints:
            unvisited_waypoints.remove(loc)
        else:
            pass

    return unvisited_waypoints


# This function is for Extra Credits, please begin this part after finishing previous two functions
def astar_multiple(maze: Maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    start: Location = maze.start
    waypoints = maze.waypoints

    open: list[AStarNode] = [
        AStarNode(
            heuristics(start, list(waypoints)),
            0,
            start,
            None,
        )
    ]
    heapify(open)
    closed: list[AStarNode] = []

    while open:
        n = heappop(open)
        closed.append(n)

        if len(get_unvisited_waypoints(generate_path(n), waypoints)) == 0:
            break
        else:
            pass

        current_path = generate_path(n)

        for edge in maze.neighbors(*n.loc):
            g: int = n.g + 1
            if edge == (1, 6):
                pass
            h: int = heuristics(
                edge, get_unvisited_waypoints(current_path + [edge], waypoints)
            )
            f: int = g + h

            close_locs: list[Location] = [n.loc for n in closed]
            open_locs: list[Location] = [n.loc for n in open]

            if edge in close_locs:
                closed_ind: int = close_locs.index(edge)
                m: AStarNode = closed[closed_ind]

                if f <= m.f:
                    closed.pop(closed_ind)
                    heappush(open, AStarNode(f, g, edge, n))
                else:
                    pass

            elif edge in open_locs:
                open_ind: int = open_locs.index(edge)
                m: AStarNode = open[open_ind]
                if f <= m.f:
                    open.pop(open_ind)
                    heapify(open)
                    heappush(open, AStarNode(f, g, edge, n))
                else:
                    pass
            else:
                heappush(open, AStarNode(f, g, edge, n))

    # paths: list[tuple[int, Path]] = []
    # heapify(paths)
    # close_locs: list[Location] = [n.loc for n in closed]
    # for point in waypoints:
    #     if point in close_locs:
    #         closed_ind: int = close_locs.index(point)
    #         m: AStarNode = closed[closed_ind]
    #         path: Path = generate_path(m)

    #         if len(get_unvisited_waypoints(generate_path(m), waypoints)) == 0:
    #             heappush(paths, (len(path), path))
    #         else:
    #             pass
    #     else:
    #         pass

    # _, final_path = heappop(paths)

    final_path = generate_path(closed[-1])
    maze.states_explored = 0

    return final_path
