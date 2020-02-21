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
        self.vertices[vertex] = {}

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex):
        return [id for id in self.vertices[vertex].values() if id != '?']


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


def graph_room(room, exits, exit=None, prev_room=None):

    opposite = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }

    graph.add_vertex(room)

    for exit in exits:
        graph.vertices[room][exit] = '?'

    if prev_room is not None:
        graph.add_vertex(prev_room)
        graph.vertices[room][opposite[exit]] = prev_room
        graph.vertices[prev_room][exit] = room


graph = Graph()


def bfs(starting_vertex, visited):
    q = Queue()
    q.enqueue(graph.get_neighbors(starting_vertex))

    # while queue is not empty:
    while q.size() > 0:
        # pop the path from the queue
        path = q.dequeue()
        # get the last node from the path
        node = list(path)[-1]

        print("")

        if '?' in path:
            return [starting_vertex, *path]

        if node not in visited:
            for adjacent in graph.get_neighbors(node):
                new_path = list(path)
                new_path.append(adjacent)
                q.enqueue(new_path)

        visited[node] = {}


visited = {}

s = Stack()

s.push(player.current_room.id)

prev_room = None

while s.size() > 0:
    # grab room to explore
    current_room = s.pop()

    exits = player.current_room.get_exits()
    graph_room(current_room, exits)

    if current_room not in visited:
        unexplored_exits = []

        print("EXITS:", exits)

        for exit in exits:
            unexplored_exits.append(exit)

        print("UNEXPLORED EXITS:", unexplored_exits)

        if len(unexplored_exits) > 0:
            exit = random.choice(unexplored_exits)

        # if current room has not been visited before, add to visited
        visited[current_room] = {}

        player.travel(exit)
        traversal_path.append(exit)
        prev_room = current_room
        graph_room(player.current_room.id, exits, exit, prev_room)
        s.push(player.current_room.id)

    if s.size() <= 1:
        # bfs for last room with a '?'
        print("PATH BACK:", bfs(current_room, visited))


print("CURRENT ROOM:", player.current_room)
print("VISITED:", visited)
print("PREV ROOM:", prev_room)
print("STACK:", s.stack)
print("TRAVERSAL PATH:", traversal_path)
print("GRAPH:", graph.vertices)


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
