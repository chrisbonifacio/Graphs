from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class Graph():
    def __init__(self):
        self.vertices = {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}

    def add_vertex(self, vertex):
        if vertex in self.vertices:
            return
        else:
            self.vertices[vertex] = {}

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex):
        return [id for id in self.vertices[vertex].values()]


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def size(self):
        return len(self.stack)


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)


graph = Graph()

back_path = []

reverse = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}


def graph_rooms(prev_room, prev_exits, direction):

    # if room exists, assign exit
    if player.current_room.id in graph.vertices:
        for exit in player.current_room.get_exits():
            if reverse[direction] == exit:
                graph.vertices[player.current_room.id][reverse[exit]] = prev_room
    else:
        # if room does not exit, create and assign exits
        graph.add_vertex(player.current_room.id)

        for exit in player.current_room.get_exits():
            if reverse[direction] == exit:
                graph.vertices[player.current_room.id][exit] = prev_room
            else:
                graph.vertices[player.current_room.id][exit] = '?'

    # assign last used exit to previous room
    for exit in prev_exits:
        if exit == direction:
            graph.vertices[prev_room][exit] = player.current_room.id


def get_unexplored(unexplored):

    for exit in player.current_room.get_exits():
        if graph.vertices[player.current_room.id][exit] == '?':
            unexplored.append(exit)

    return unexplored


def travel(direction):
    player.travel(direction)
    traversal_path.append(direction)


def bfs(starting_vertex):
    q = Queue()
    q.enqueue([id for id in graph.get_neighbors(
        starting_vertex)])
    # create list for visited nodes
    visited = {}
    # while queue is not empty:
    while q.size() > 0:
        # pop the path from the queue
        path = q.dequeue()
        # get the last node from the path
        node = list(path)[-1]

        if node == '?':
            path.pop()

            return [starting_vertex, *path]

        if node not in visited:
            for adjacent in graph.get_neighbors(node):
                new_path = list(path)
                new_path.append(adjacent)
                q.enqueue(new_path)

        visited[node] = graph.vertices[node]


def dft():
    while len(graph.vertices) < len(world.rooms):
        # get the player's current room
        prev_room = player.current_room.id

        # get exits
        exits = player.current_room.get_exits()

        # get unexplored exits
        unexplored = []

        get_unexplored(unexplored)

        if len(unexplored) > 0:
            # choose random direction
            direction = random.choice(unexplored)

            # travel
            travel(direction)
            back_path.append(reverse[direction])
            print("GRAPH:", graph.vertices)

        else:
            # go back until unexplored room found
            while len(unexplored) == 0:
                # BFS
                directions = bfs(player.current_room.id)

                path_back = []
                print(directions)
                print("CURRENT ROOM:", player.current_room.id)

                # TODO: convert BFS

                for i in range(0, len(directions) - 1):
                    for direction in reverse:
                        curr = directions[i]
                        nxt = directions[i + 1]

                        if direction in graph.vertices[curr].keys() and graph.vertices[curr][direction] == nxt:
                            path_back.append(direction)
                            print("PATH BACK:", path_back)

                if len(path_back) > 0:
                    for step in path_back:
                        player.travel(step)
                        get_unexplored(unexplored)

        # graph rooms
        graph_rooms(prev_room, exits, direction)


dft()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
