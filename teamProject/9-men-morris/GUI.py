import pygame
import sys
import time
import constants
import json

from NineMensMorrisGame import NineMensMorrisGame

# Initialize Pygame
pygame.init()


def get_coords(mouse_pos):
    col = int(mouse_pos[0] / constants.SQUARESIZE)
    row = int((mouse_pos[1]) / constants.SQUARESIZE)
    return row, col


class NineMensMorrisGUI:
    def __init__(self, game):
        # Initialize Pygame window
        self.replay_prev = None
        self.replay_stop_at_one_move = None
        self.replay_game = None
        self.replay_game_moves = None
        self.replay_game_moves_index = 0
        self.available_game_ids = None
        self.show_load_menu = False
        self.replay_stopped = False
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Nine Men's Morris")
        self.clock = pygame.time.Clock()
        self.game = game
        self.clicked_point = None
        self.load_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH - 180, 10, 120, 40
        )
        self.load_button_color = (0, 255, 0)
        self.load_button_text = "Load Game"
        self.stop_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH - 180, 80, 120, 40
        )
        self.next_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH - 180, 150, 120, 40
        )
        self.next_button_color = (0, 255, 0)
        self.next_button_text = "Next Move"

        self.prev_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH - 180, 200, 120, 40
        )
        self.prev_button_color = (0, 255, 0)
        self.prev_button_text = "Prev Move"

        self.quit_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH - 180, constants.SCREEN_HEIGHT - 60, 120, 40
        )
        self.quit_button_color = (255, 0, 0)
        self.quit_button_text = "Quit"

    def draw_board(self):
        self.screen.fill((255, 255, 255))

        myfont = pygame.font.SysFont("Comic Sans MS", 24)

        if self.replay_stopped:
            pygame.draw.rect(
                self.screen, self.next_button_color, self.next_button_rect
            )
            next_label = myfont.render(self.next_button_text, 1, constants.BLACK)
            self.screen.blit(
                next_label,
                (
                    self.next_button_rect.x + 10,
                    self.next_button_rect.y + 10,
                ),
            )
            pygame.draw.rect(
                self.screen, self.prev_button_color, self.prev_button_rect
            )
            next_label = myfont.render(self.prev_button_text, 1, constants.BLACK)
            self.screen.blit(
                next_label,
                (
                    self.prev_button_rect.x + 10,
                    self.prev_button_rect.y + 10,
                ),
            )

        pygame.draw.rect(
            self.screen, self.quit_button_color, self.quit_button_rect
        )
        quit_label = myfont.render(self.quit_button_text, 1, constants.BLACK)
        self.screen.blit(
            quit_label,
            (
                self.quit_button_rect.x + 10,
                self.quit_button_rect.y + 10,
            ),
        )

        pygame.draw.rect(
            self.screen, self.load_button_color, self.load_button_rect
        )
        myfont = pygame.font.SysFont("Comic Sans MS", 20)
        load_label = myfont.render(self.load_button_text, 1, constants.BLACK)
        self.screen.blit(
            load_label,
            (
                self.load_button_rect.x + 10,
                self.load_button_rect.y + 10,
            ),
        )

        for x in range(len(constants.LINES)):
            pygame.draw.line(
                self.screen,
                constants.BLACK,
                (
                    constants.LINES[x][0] * constants.SQUARESIZE,
                    constants.SQUARESIZE * constants.LINES[x][1],
                ),
                (
                    constants.LINES[x][2] * constants.SQUARESIZE,
                    constants.LINES[x][3] * constants.SQUARESIZE,
                ),
                5,
            )

        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                radius = constants.CIRCLE_RADIUS
                color = constants.CIRCLE_COLOR
                if int(self.game.CURRENT_POSITION[r][c]) == constants.PLAY1:
                    (color, radius) = (constants.RED, radius)
                elif int(self.game.CURRENT_POSITION[r][c]) == constants.PLAY2:
                    (color, radius) = (constants.BLUE, radius)
                elif int(constants.VALID_POSITIONS[r][c] == constants.VALID):
                    radius = int(constants.CIRCLE_RADIUS / 2)
                else:
                    radius = 0

                pygame.draw.circle(
                    self.screen,
                    color,
                    (
                        int(c * constants.SQUARESIZE + constants.SQUARESIZE / 2),
                        int(r * constants.SQUARESIZE + constants.SQUARESIZE / 2),
                    ),
                    radius,
                )

        # Highlight the selected position
        if self.game.move_made and self.clicked_point:
            r, c = self.clicked_point
            self.draw_highlight(r, c)

        myfont = pygame.font.SysFont("Comic Sans MS", 30)

        label = myfont.render(self.game.message, 1, constants.BLACK)
        self.screen.blit(label, (0.5 * constants.SQUARESIZE, 7 * constants.SQUARESIZE))

        moveLabel = myfont.render(
            "Move made: " + self.game.move_made, 1, constants.BLACK
        )
        self.screen.blit(
            moveLabel, (0.5 * constants.SQUARESIZE, 7.5 * constants.SQUARESIZE)
        )

        player1_pieces = myfont.render(
            "P1:" + str(abs(self.game.play1_counter - self.game.total_mens)),
            1,
            constants.BLACK,
            )
        self.screen.blit(
            player1_pieces, (7.5 * constants.SQUARESIZE, 0.5 * constants.SQUARESIZE)
        )

        player2_pieces = myfont.render(
            "P2:" + str(abs(self.game.play2_counter - self.game.total_mens)),
            1,
            constants.BLACK,
            )
        self.screen.blit(
            player2_pieces, (7.5 * constants.SQUARESIZE, 0.8 * constants.SQUARESIZE)
        )

    def handle_events(self):
        if self.replay_game and self.replay_prev and self.replay_game_moves_index > 0:
            new_game = NineMensMorrisGame(self.game.db, self.game.total_mens, self.game.VALID_POSITIONS)
            self.game = new_game

            for r in range(constants.ROWS):
                for c in range(constants.COLS):
                    self.game.CURRENT_POSITION[r][c] = 0

            self.draw_board()

            for index in range(self.replay_game_moves_index):
                move = self.replay_game_moves[index]
                move_type = move['type']

                if move_type == constants.REMOVE_PIECE:
                    self.game.is_remove_piece = True
                elif self.game.phase == constants.PHASE1:
                    self.game.make_move(move['row'], move['col'], None, None)
                elif self.game.phase == constants.PHASE2 and move_type != constants.REMOVE_PIECE:
                    self.game.make_move(move['row'], move['col'], move['new_row'], move['new_col'])

                if self.game.is_remove_piece:  # and self.replay_game_moves_index + 1 < len(self.replay_game_moves):
                    print("removing")
                    # self.replay_game_moves_index = self.replay_game_moves_index + 1
                    move = self.replay_game_moves[self.replay_game_moves_index]
                    player = self.game.get_turn()
                    self.game.remove_piece(move['row'], move['col'], player)
                    self.game.is_remove_piece = False
            self.replay_prev = False

        if self.replay_game and self.replay_game_moves_index < len(self.replay_game_moves):
            time.sleep(1)

            pygame.draw.rect(
                self.screen, self.load_button_color, self.stop_button_rect
            )
            myfont = pygame.font.SysFont("Comic Sans MS", 20)
            load_label = myfont.render("Pause Game", 1, constants.BLACK)
            self.screen.blit(
                load_label,
                (
                    self.stop_button_rect.x + 10,
                    self.stop_button_rect.y + 10,
                ),
            )

            print(self.replay_game_moves[self.replay_game_moves_index])
            move = self.replay_game_moves[self.replay_game_moves_index]
            move_type = move['type']

            if move_type == constants.REMOVE_PIECE:
                self.game.is_remove_piece = True
            elif self.game.phase == constants.PHASE1:
                self.game.make_move(move['row'], move['col'], None, None)
            elif self.game.phase == constants.PHASE2 and move_type != constants.REMOVE_PIECE:
                self.game.make_move(move['row'], move['col'], move['new_row'], move['new_col'])

            if self.game.is_remove_piece:  # and self.replay_game_moves_index + 1 < len(self.replay_game_moves):
                print("removing")
                # self.replay_game_moves_index = self.replay_game_moves_index + 1
                move = self.replay_game_moves[self.replay_game_moves_index]
                player = self.game.get_turn()
                self.game.remove_piece(move['row'], move['col'], player)
                self.game.is_remove_piece = False

            if not self.replay_stop_at_one_move:
                self.replay_game_moves_index = self.replay_game_moves_index + 1
            else:
                self.replay_game = False

            if self.replay_game_moves_index == len(self.replay_game_moves):
                print("moves exhausted")

        if (
            self.game.game_mode == constants.H_VS_C
            and self.game.turn == constants.PLAY2
        ):
            move = self.game.computer_make_move()
            print("turn:", self.game.get_turn())
            if move:
                if self.game.phase == constants.PHASE1:
                    self.game.make_move(move[0], move[1], None, None)
                    new_row = move[0]
                    new_col = move[1]
                elif self.game.phase == constants.PHASE2:
                    self.game.make_move(move[0], move[1], move[2], move[3])
                    new_row = move[2]
                    new_col = move[3]

                print("turn after make move:", self.game.get_turn())

                # Check for mill formation only if new_row and new_col are not None
                if new_row is not None and new_col is not None:
                    if self.game.is_mill(new_row, new_col, self.game.turn):
                        piece_to_remove = self.game.select_piece_to_remove()
                        print("piece to remove", piece_to_remove)
                        if piece_to_remove:
                            player = self.game.get_turn()
                            self.game.remove_piece(
                                *piece_to_remove, self.game.get_turn()
                            )
                            print("here:", player)
                            move_history = {
                                "type": constants.REMOVE_PIECE,
                                "player": player,
                                "move": self.game.get_move(new_row, new_col),
                                "row": new_row,
                                "col": new_col,
                                "new_move": None,
                                "new_row": None,
                                "new_col": None,
                            }
                            self.game.save_move(move_history)
                            self.game.is_remove_piece = False

        (r, c) = get_coords(pygame.mouse.get_pos())

        if self.show_load_menu:
            game_id = self.show_game_selection_menu()
            if game_id is not None:
                self.replay_game_moves_index = 0
                self.show_load_menu = not self.show_load_menu
                moves = json.loads(game_id.moves)
                self.replay_game_moves = moves
                self.replay_game = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.game.save_game()
                    pygame.quit()
                    sys.exit()
                if self.stop_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.replay_game = False
                    self.replay_stopped = True
                if self.load_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.show_load_menu = not self.show_load_menu
                    self.replay_stop_at_one_move = False
                    self.replay_game_moves_index = 0
                if self.next_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.replay_game_moves_index = self.replay_game_moves_index + 1
                    self.replay_game = True
                    self.replay_stop_at_one_move = True
                if self.prev_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.replay_game_moves_index = self.replay_game_moves_index - 1
                    self.replay_game = True
                    self.replay_stop_at_one_move = True
                    self.replay_prev = True

                if self.game.over:
                    return
                if self.game.phase == constants.PHASE1:
                    if self.game.is_remove_piece:
                        player = self.game.get_turn()
                        if self.game.remove_piece(r, c, player):
                            move_history = {
                                "type": constants.REMOVE_PIECE,
                                "player": self.game.get_turn(),
                                "move": self.game.get_move(r, c),
                                "row": r,
                                "col": c,
                                "new_move": None,
                                "new_row": None,
                                "new_col": None,
                            }
                            self.game.save_move(move_history)
                            self.game.is_remove_piece = False
                    else:
                        self.game.make_move(r, c, None, None)
                elif self.game.phase == constants.PHASE2:
                    if 0 <= r < constants.ROWS and 0 <= c < constants.COLS:
                        if self.game.is_remove_piece:
                            player = self.game.get_turn()
                            if self.game.remove_piece(r, c, player):
                                move_history = {
                                    "type": constants.REMOVE_PIECE,
                                    "player": player,
                                    "move": self.game.get_move(r, c),
                                    "row": r,
                                    "col": c,
                                    "new_move": None,
                                    "new_row": None,
                                    "new_col": None,
                                }
                                self.game.save_move(move_history)
                                self.game.is_remove_piece = False
                        else:
                            if self.game.get_turn() == constants.PLAY1:
                                if self.clicked_point is None:
                                    # If no piece is selected, check if the clicked point has a player's piece
                                    if (
                                        self.game.CURRENT_POSITION[r][c]
                                        == constants.PLAY1
                                    ):
                                        self.clicked_point = (r, c)
                                else:
                                    # Check for valid point
                                    self.game.make_move(
                                        self.clicked_point[0],
                                        self.clicked_point[1],
                                        r,
                                        c,
                                    )
                                    self.clicked_point = None
                            elif self.game.get_turn() == constants.PLAY2:
                                if self.clicked_point is None:
                                    # If no piece is selected, check if the clicked point has a player's piece
                                    if (
                                        self.game.CURRENT_POSITION[r][c]
                                        == constants.PLAY2
                                    ):
                                        self.clicked_point = (r, c)
                                else:
                                    # If a piece is selected, try to move it to the clicked point
                                    self.game.make_move(
                                        self.clicked_point[0],
                                        self.clicked_point[1],
                                        r,
                                        c,
                                    )
                                    self.clicked_point = None

    def draw_highlight(self, r, c):
        x = c * constants.SQUARESIZE + constants.SQUARESIZE / 2
        y = r * constants.SQUARESIZE + constants.SQUARESIZE / 2
        highlight_radius = (
            constants.CIRCLE_RADIUS + 5
        )  # Adjust the radius as needed for the glowing effect
        highlight_color = constants.GRAY

        # Draw a glowing circle around the piece
        pygame.draw.circle(
            self.screen, highlight_color, (int(x), int(y)), highlight_radius
        )

    def show_game_selection_menu(self):
        # Placeholder for showing a menu to select a game from the database
        myfont = pygame.font.SysFont("Comic Sans MS", 24)

        # Query the database to get available game IDs
        self.available_game_ids = self.game.db.get_moves()

        # Display a list of game IDs
        for i, game_id in enumerate(self.available_game_ids):
            text = myfont.render(f"{game_id.name} {game_id.played_at}", 1, constants.BLACK)
            y_position = 100 + i * 30
            self.screen.blit(text, (constants.SCREEN_WIDTH - 200, y_position))

        # Check if the user clicked on a game ID
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.save_game()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, game_id in enumerate(self.available_game_ids):
                    y_position = 100 + i * 30
                    if (
                        constants.SCREEN_WIDTH - 200
                        < pygame.mouse.get_pos()[0]
                        < constants.SCREEN_WIDTH
                        and y_position < pygame.mouse.get_pos()[1] < y_position + 30
                    ):
                        return game_id

        return None

    def main_loop(self):
        while True:
            self.draw_board()

            self.handle_events()

            pygame.display.flip()
            self.clock.tick(60)
