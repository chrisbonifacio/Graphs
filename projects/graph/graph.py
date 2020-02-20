"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # keep a queue containing people to check
        queue = Queue()
        queue.enqueue(starting_vertex)
        searched = set()

        # while the queue is not empty
        while queue.size() > 0:
            # pop a item off the queue
            current = queue.dequeue()

            # if current item has not already been searched, do stuff
            if not current in searched:
                print(current)
                # mark node as searched
                searched.add(current)
                # queue all neighbors to be searched
                for node in self.get_neighbors(current):
                    queue.enqueue(node)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create an empty stack
        stack = Stack()

        # create empty set to keep track of visited nodes
        visited = set()

        # push starting vertex onto the stack
        stack.push(starting_vertex)

        # while stack is not empty
        while stack.size() > 0:
            # pop the top item off of the stack
            current = stack.pop()

            # if current item has not been visited already, check it
            if current not in visited:
                print(current)

                # mark as visited
                visited.add(current)

                # push all neighbors to top of the stack
                for neighbor in self.get_neighbors(current):
                    stack.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """

        if starting_vertex in visited:
            return
        else:
            print("DFT_RECURSIVE", starting_vertex)
            visited.add(starting_vertex)

            neighbors = self.get_neighbors(starting_vertex)

            for neighbor in neighbors:
                if neighbor not in visited:
                    self.dft_recursive(neighbor, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create an empty queue of paths
        q = Queue()
        # put starting path in queue
        q.enqueue(self.get_neighbors(starting_vertex))
        # create list for visited nodes
        visited = set()

        # while queue is not empty:
        while q.size() > 0:
            # pop the path from the queue
            path = q.dequeue()
            # get the last node from the path
            node = list(path)[-1]

            if node == destination_vertex:
                return [starting_vertex, *path]

            if node not in visited:
                for adjacent in self.get_neighbors(node):
                    new_path = list(path)
                    new_path.append(adjacent)
                    q.enqueue(new_path)

            visited.add(node)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """

        stack = Stack()
        visited = set()
        path = []

        stack.push(starting_vertex)

        while stack.size() > 0:
            curr = stack.pop()
            path.append(curr)

            if curr == destination_vertex:
                return path

            for neighbor in self.get_neighbors(curr):
                stack.push(neighbor)

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
