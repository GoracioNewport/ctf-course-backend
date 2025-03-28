from fastapi import APIRouter
from typing import Union
from secrets import token_hex

import random
import string

router = APIRouter(prefix="/ppc")


# Maze Task

maze = [
    "#####################",
    "#                   #",
    "####### # ### # #####",
    "#       #   # # #   #",
    "# # ##### ##### # # #",
    "# #   #   #   #   # #",
    "# # ### # ### # ### #",
    "# # # # #   #   # # #",
    "### # ########### ###",
    "#         #     #   #",
    "# ####### # ##### # #",
    "#   # #           # #",
    "##### # ### ####### #",
    "#       #   #     # #",
    "##### ### # # # ### #",
    "# #   #   # # #   # #",
    "# # # ### # # ##### #",
    "# # #   # #       # #",
    "# ####### # # ### ###",
    "#         # #   #   #",
    "#####################"
]

maze_users = dict()


@router.get("/maze")
def maze_make_turn(session_id: Union[str, None] = None, direction: Union[str, None] = None):
    global maze_users, maze
    if not session_id and not direction:

        token = token_hex(20)
        maze_users[token] = [1, 1]
        return "Welcome to the Maze. You are at the top-left corner of the map, flag is at the opposite corner. Please, provide 'session_id' and 'direction' query parametrs to start the game. Valid moves are: left, right, up, down. Your token is: " + token

    if not session_id:

        return "session_id not specified"

    if direction not in ['left', 'right', 'up', 'down']:

        return "Invalid direction"

    if session_id not in maze_users:

        return "Invalid token"

    dx = 0
    dy = 0

    if direction == "up":
        dx -= 1
    if direction == "down":
        dx += 1
    if direction == "left":
        dy -= 1
    if direction == "right":
        dy += 1

    x = maze_users[session_id][0]
    y = maze_users[session_id][1]

    if maze[x + dx][y + dy] == '#':
        maze_users[session_id][0] = 1
        maze_users[session_id][1] = 1
        return "Bump! Position restored :)"

    maze_users[session_id][0] += dx
    maze_users[session_id][1] += dy

    if (x + dx == 19 and y + dy == 19):
        return "I hope you programmed a bot for this... gctf_you_are_a_maze_ing"
    return "OK"


# Index Cycle Tas

pos = 0
cycle_flag = "gctf_this_one_is_very_long_because_i_want_you_to_write_a_program_for_this"


@router.get("/letter")
def get_letter():
    global pos
    r = cycle_flag[pos]
    pos += 1
    if pos >= len(cycle_flag):
        pos = 0

    return r


# Sort Task

@router.get("/sort")
def get_sort(s: Union[str, None] = None):
    k = 2280
    if not s:
        r = ""
        for i in range(k):
            r += random.choice(string.ascii_lowercase)
        return r

    if len(s) != k:
        return "Wrong string!"

    for i in range(len(s) - 1):
        if (s[i] > s[i + 1]):
            return "String is not sorted!"

    return "gctf_do_you_prefer_quicksort_or_mergesort?"
