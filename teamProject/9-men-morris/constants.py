# current positions on the board
CURRENT_POSITION = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# Valid positions on the board
VALID_POSITIONS = [
    #    0  1  2  3  4  5  6  7
    [3, 0, 0, 3, 0, 0, 3, 0],  # 0
    [0, 3, 0, 3, 0, 3, 0, 0],  # 1
    [0, 0, 3, 3, 3, 0, 0, 0],  # 2
    [3, 3, 3, 0, 3, 3, 3, 0],  # 3
    [0, 0, 3, 3, 3, 0, 0, 0],  # 4
    [0, 3, 0, 3, 0, 3, 0, 0],  # 5
    [3, 0, 0, 3, 0, 0, 3, 0],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0],  # 7
]

LINES = [
    # plus sign pattern
    [3.5, 0.5, 3.5, 2.5],
    [0.5, 3.5, 2.5, 3.5],
    [3.5, 4.5, 3.5, 6.5],
    [4.5, 3.5, 6.5, 3.5],
    # outer square
    [0.5, 0.5, 6.5, 0.5],
    [6.5, 0.5, 6.5, 6.5],
    [6.5, 6.5, 0.5, 6.5],
    [0.5, 6.5, 0.5, 0.5],
    # middle square
    [1.5, 1.5, 5.5, 1.5],
    [5.5, 1.5, 5.5, 5.5],
    [5.5, 5.5, 1.5, 5.5],
    [1.5, 5.5, 1.5, 1.5],
    # small square
    [2.5, 2.5, 4.5, 2.5],
    [4.5, 2.5, 4.5, 4.5],
    [4.5, 4.5, 2.5, 4.5],
    [2.5, 4.5, 2.5, 2.5],
]


# Valid positions on the board
VALID_POSITIONS_SIX_MENS = [
    # 0  1  2  3  4  5  6  7
    [0, 0, 0, 0, 0, 0, 0, 0],  # 0
    [0, 3, 0, 3, 0, 3, 0, 0],  # 1
    [0, 0, 3, 3, 3, 0, 0, 0],  # 2
    [0, 3, 3, 0, 3, 3, 0, 0],  # 3
    [0, 0, 3, 3, 3, 0, 0, 0],  # 4
    [0, 3, 0, 3, 0, 3, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0],  # 7
]

LINES_SIX_MEN = [
    # plus sign pattern
    [3.5, 1.5, 3.5, 2.5],
    [1.5, 3.5, 2.5, 3.5],
    [3.5, 4.5, 3.5, 5.5],
    [4.5, 3.5, 5.5, 3.5],
    # middle square
    [1.5, 1.5, 5.5, 1.5],
    [5.5, 1.5, 5.5, 5.5],
    [5.5, 5.5, 1.5, 5.5],
    [1.5, 5.5, 1.5, 1.5],
    # small square
    [2.5, 2.5, 4.5, 2.5],
    [4.5, 2.5, 4.5, 4.5],
    [4.5, 4.5, 2.5, 4.5],
    [2.5, 4.5, 2.5, 2.5],
]

# Board status
BLANK = 0
PLAY1 = 1
PLAY2 = 2
VALID = 3

# Game Phases
PHASE1 = 1
PHASE2 = 2
PHASE3 = 3

# board size and pieces
ROWS = 7
COLS = 7

# Constants for the screen dimensions and board
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 0, 0)
CIRCLE_RADIUS = 15

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 155)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

SQUARESIZE = 80
TOTAL_MENS = 9
TOTAL_SIX_MENS = 6

PLAYER1_MESSAGE = "Player 1 (Red) turn to place piece"
PLAYER2_MESSAGE = "Player 2 (Blue) turn to place piece"

PLAY1_MOVE_MESSAGE = "Player 1 (Red) turn to move piece"
PLAY2_MOVE_MESSAGE = "Player 2 (Blue) turn to move piece"

REMOVE_PIECE_MESSAGE = ", Remove a piece from opponent"

FLY_MESSAGE = "You can FLY your piece"

H_VS_H = 0
H_VS_C = 1

POSITIONS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g"}

GAME_STATE_FILE = "game_state.txt"

PLACE_PIECE = "place_piece"
MOVE_PIECE = "move_piece"
REMOVE_PIECE = "remove_piece"
FLY_PIECE = "fly_piece"

SIX_MEN_MORRIS = "six_men_morris"
NINE_MEN_MORRIS = "nine_men_morris"
