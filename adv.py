from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

        

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
backtracking = []

# visited rooms dictionary 
rooms = {}

# make a funcion that goes in reverse to backtrack steps
def reverse_dir(dir):
    if dir == "n":
        return "s"
    if dir == "s":
        return "n"
    if dir == "w":
        return "e"
    if dir == "e":
        return "w"
    else:
        return "error"

# put the first room in the dictionary with the list of exits
rooms[player.current_room.id] = player.current_room.get_exits()
# print(f"Starting room: {player.current_room.id}, Exits: {player.current_room.get_exits()}\n")
# while the length of the visited rooms is less than the number of rooms in the graph - the first room
while len(rooms) < len(room_graph) - 1:
    # if the current room has never been visited
    if player.current_room.id not in rooms:
        # print(f"Current room: {player.current_room.id}, Exits: {player.current_room.get_exits()}")
        # set the list of exits to the room in visited dictionary
        rooms[player.current_room.id] = player.current_room.get_exits()
        # mark the room you came from as explored
        last_room = backtracking[-1]
        rooms[player.current_room.id].remove(last_room)
        # print(f"List of moves that happened - {traversal_path}\n")
# for dead ends
    while len(rooms[player.current_room.id]) < 1:
        # remove the last direction from backtracking
        backtrack = backtracking.pop()
        # travel back
        player.travel(backtrack)
        # add the move to the traversal path
        traversal_path.append(backtrack)
# for the unexplored rooms
    else:
        # pick the last exit
        last_exit = rooms[player.current_room.id].pop()
        # add the move to the traversal path
        traversal_path.append(last_exit)
        # store the reverse direction for going back
        backtracking.append(reverse_dir(last_exit))
        # travel to the next room
        player.travel(last_exit)
# print(f"Final List of Moves - {traversal_path}")
print("found exit!")

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
