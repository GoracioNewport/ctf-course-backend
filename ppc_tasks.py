from fastapi import APIRouter
from typing import Union
from secrets import token_hex

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
        return "Bump!"

    maze_users[session_id][0] += dx
    maze_users[session_id][1] += dy

    if (x + dx == 19 and y + dy == 19):
        return "I hope you programmed a bot for this... gctf_you_are_a_maze_ing"
    return "OK"

# Bruteforce Task


@router.post("/passCheck")
def pass_check(password: Union[str, None] = None):
    if password != "bruh":
        return "Wrong password!"

    return "gctf_fastest_hands_in_the_west"
