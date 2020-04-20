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
        self.vertices = {}

    def add_vertex(self, vertex):
        if vertex in self.vertices:
            return
        else:
            self.vertices[vertex] = {}

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)


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

reverse = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}


def graph_rooms(prev_room, next_room, direction):
    graph.vertices[prev_room][direction] = next_room

    if not next_room in graph.vertices:
        graph.vertices[next_room] = {}
        for e in player.current_room.get_exits():
            graph.vertices[next_room][e] = '?'

    graph.vertices[next_room][reverse[direction]] = prev_room


def get_unexplored(room):
    for exit in room:
        if room[exit] == '?':
            return exit
    return None


def travel(direction):
    curr = player.current_room.id

    player.travel(direction)

    nxt = player.current_room.id

    print(f"moving {direction} {curr} --> {nxt}")

    # add move to traversal path
    traversal_path.append(direction)

    # graph rooms
    graph_rooms(curr, nxt, direction)


def dft():
    graph.vertices[player.current_room.id] = {}

    for exit in player.current_room.get_exits():
        graph.vertices[player.current_room.id][exit] = '?'

    while len(graph.vertices) < len(world.rooms):
        curr_room = player.current_room.id
        # check for unexplored exits
        if '?' in graph.vertices[player.current_room.id].values():
            direction = get_unexplored(graph.vertices[player.current_room.id])
            # travel
            travel(direction)

        else:
            # BFS
            q = Queue()
            q.enqueue([curr_room])
            # create list for visited nodes
            visited = set()
            # while queue is not empty:
            while q.size() > 0:
                # pop the path from the queue
                path = q.dequeue()

                # get the last node from the path
                room = path[-1]

                direction = get_unexplored(graph.vertices[room])

                if direction is not None:
                    # convert BFS rooms to directions
                    for i in range(0, len(path) - 1):
                        curr = path[i]
                        nxt = path[i + 1]

                        for direction in graph.vertices[curr]:
                            if graph.vertices[curr][direction] == nxt:
                                travel(direction)
                    break

                if room not in visited:
                    visited.add(room)
                    for exit in graph.vertices[room]:
                        new_path = path.copy()
                        new_path.append(graph.vertices[room][exit])
                        q.enqueue(new_path)


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
