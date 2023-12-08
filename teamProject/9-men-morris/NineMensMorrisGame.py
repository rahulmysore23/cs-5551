import json
import os
import uuid

import constants
import random
from datetime import datetime


class NineMensMorrisGame:
    def __init__(self, db_interface, pieces, valid_positions):
        self.phase = constants.PHASE1
        self.turn = constants.PLAY1
        self.CURRENT_POSITION = constants.CURRENT_POSITION
        self.VALID_POSITIONS = valid_positions
        self.is_remove_piece = False
        self.counter = 0
        self.play1_pieces = pieces
        self.play2_pieces = pieces
        self.play1_counter = 0
        self.play2_counter = 0
        self.message = constants.PLAYER1_MESSAGE
        self.move_made = ""
        self.over = False
        self.moves_made = []  # TODO - Make it a stack, Will be useful when using undo
        self.db = db_interface
        self.game_mode = ""
        self.start_time = datetime.now()
        self.total_mens = pieces

    def update_pieces(self):
        if self.turn == constants.PLAY1:
            self.play2_pieces -= 1
        else:
            self.play1_pieces -= 1

    def change_turn(self):
        if self.phase == constants.PHASE1:
            if self.turn == constants.PLAY1:
                self.play1_counter = self.play1_counter + 1
                self.turn = constants.PLAY2
                self.message = constants.PLAYER2_MESSAGE
            else:
                self.play2_counter = self.play2_counter + 1
                self.turn = constants.PLAY1
                self.message = constants.PLAYER1_MESSAGE

            if (
                self.play1_counter == self.total_mens
                and self.play2_counter == self.total_mens
            ):
                self.set_phase(constants.PHASE2)
                self.message = (
                    "Pieces placed, Move pieces now\n" + constants.PLAY1_MOVE_MESSAGE
                )

        elif self.phase == constants.PHASE2:
            if self.turn == constants.PLAY1:
                self.turn = constants.PLAY2
                self.message = constants.PLAY2_MOVE_MESSAGE
            else:
                self.turn = constants.PLAY1
                self.message = constants.PLAY1_MOVE_MESSAGE
        else:
            self.message = "Invalid phase"

        if self.get_player_pieces() == 3:
            self.message = (
                self.get_player_from_const(self.get_turn()) + constants.FLY_MESSAGE
            )

        # check for game over
        if self.is_game_over() is not None:
            self.message = (
                self.get_player_from_const(self.is_game_over()) + " Wins the game!!"
            )
            self.over = True

    def get_turn(self):
        return self.turn

    def get_opp(self):
        if self.turn == constants.PLAY1:
            return constants.PLAY2
        return constants.PLAY1

    def get_player_pieces(self):
        if self.turn == constants.PLAY1:
            return self.play1_pieces
        return self.play2_pieces

    def set_phase(self, phase):
        self.phase = phase

    def get_player_from_const(self, player):
        if player == constants.PLAY1:
            return "Player 1"
        return "Player 2"

    def save_move(self, move_history):
        self.moves_made.append(move_history)

    def make_move(self, row, col, new_row, new_col):
        valid = self.is_move_valid(row, col, new_row, new_col)
        # print("clicked:", row, col, valid)  # Debug message, Remove it later
        move_type = constants.PLACE_PIECE
        player = self.get_turn()
        new_move = None

        if valid:
            move = self.get_move(row, col)
            if new_row is not None and new_col is not None:
                new_move = self.get_move(new_row, new_col)

            self.move_made = move
            self.counter = self.counter + 1
            if self.phase == constants.PHASE1:
                self.place_piece(row, col, self.get_turn())
                # if mill is formed, do not change the player's turn, but ask him to remove an opponent piece
                # print("Is mill:", self.is_mill(row, col, self.get_turn()))

                if self.is_mill(row, col, self.get_turn()):
                    self.message = (
                        self.get_player_from_const(self.get_turn())
                        + constants.REMOVE_PIECE_MESSAGE
                    )
                    self.is_remove_piece = True
                    move_history = {
                        "type": move_type,
                        "player": player,
                        "move": move,
                        "row": row,
                        "col": col,
                        "new_move": new_move,
                        "new_row": new_row,
                        "new_col": new_col,
                    }
                    self.save_move(move_history)
                    return
                move_type = constants.PLACE_PIECE
                self.change_turn()
            elif self.phase == constants.PHASE2:
                if self.get_player_pieces() == 3:
                    move_type = constants.FLY_PIECE
                    if not self.fly_piece(row, col, new_row, new_col, self.get_turn()):
                        return
                    if self.is_mill(new_row, new_col, self.get_turn()):
                        self.message = (
                            self.get_player_from_const(self.get_turn())
                            + constants.REMOVE_PIECE_MESSAGE
                        )
                        self.is_remove_piece = True
                        move_history = {
                            "type": move_type,
                            "player": player,
                            "move": move,
                            "row": row,
                            "col": col,
                            "new_move": new_move,
                            "new_row": new_row,
                            "new_col": new_col,
                        }
                        self.save_move(move_history)
                        return
                else:
                    move_type = constants.MOVE_PIECE
                    self.move_piece(row, col, new_row, new_col, self.get_turn())
                    print("Is mill:", self.is_mill(new_row, new_col, self.get_turn()))

                    if self.is_mill(new_row, new_col, self.get_turn()):
                        self.message = (
                            self.get_player_from_const(self.get_turn())
                            + constants.REMOVE_PIECE_MESSAGE
                        )
                        self.is_remove_piece = True
                        move_history = {
                            "type": move_type,
                            "player": player,
                            "move": move,
                            "row": row,
                            "col": col,
                            "new_move": new_move,
                            "new_row": new_row,
                            "new_col": new_col,
                        }
                        self.save_move(move_history)
                        return
                self.change_turn()
            elif self.phase == constants.PHASE3:
                pass

            move_history = {
                "type": move_type,
                "player": player,
                "move": move,
                "row": row,
                "col": col,
                "new_move": new_move,
                "new_row": new_row,
                "new_col": new_col,
            }
            self.save_move(move_history)

    def get_move(self, row, col):
        return constants.POSITIONS[col] + str(abs(row - 7))

    def place_piece(self, row, col, player):
        self.CURRENT_POSITION[row][col] = player

    def is_move_valid(self, row, col, new_row, new_col):
        if (self.phase == constants.PHASE1) or (self.phase == constants.PHASE3):
            return [row, col] in self.get_valid_moves()
        elif self.phase == constants.PHASE2:
            if not (
                0 <= row < constants.ROWS
                and 0 <= col < constants.COLS
                # and new_row is not None
                # and new_col is not None
                and 0 <= new_row < constants.ROWS
                and 0 <= new_col < constants.COLS
            ):
                return False

            if (
                self.CURRENT_POSITION[row][col] == self.get_turn()
                and self.CURRENT_POSITION[new_row][new_col] == constants.BLANK
            ):
                # Check the valid positions matrix, there should exist a 3 in it and a 0 in current position
                # Can skip 0 for a complete row or column, Should handle a special case
                if self.get_player_pieces() == 3:
                    if self.CURRENT_POSITION[new_row][new_col] == constants.BLANK:
                        return True
                else:
                    if row == new_row:
                        col_index = col
                        if new_col > col:
                            col_index += 1
                            while col_index <= new_col:
                                if (
                                    self.VALID_POSITIONS[row][col_index]
                                    == constants.VALID
                                    and self.CURRENT_POSITION[row][col_index]
                                    == constants.BLANK
                                    and col_index == new_col
                                ):
                                    return True
                                elif (
                                    self.VALID_POSITIONS[row][col_index] == 0
                                    and row != 3
                                ):
                                    col_index += 1
                                else:
                                    return False
                        else:
                            col_index -= 1
                            while col_index >= new_col:
                                if (
                                    self.VALID_POSITIONS[row][col_index]
                                    == constants.VALID
                                    and self.CURRENT_POSITION[row][col_index]
                                    == constants.BLANK
                                    and col_index == new_col
                                ):
                                    return True
                                elif (
                                    self.VALID_POSITIONS[row][col_index] == 0
                                    and row != 3
                                ):
                                    col_index -= 1
                                else:
                                    return False
                    if col == new_col:
                        row_index = row
                        if new_row > row:
                            row_index += 1
                            while row_index <= new_row:
                                if (
                                    self.VALID_POSITIONS[row_index][col]
                                    == constants.VALID
                                    and self.CURRENT_POSITION[row_index][col]
                                    == constants.BLANK
                                    and row_index == new_row
                                ):
                                    return True
                                elif (
                                    self.VALID_POSITIONS[row_index][col] == 0
                                    and col != 3
                                ):
                                    row_index += 1
                                else:
                                    return False
                        else:
                            row_index -= 1
                            while row_index >= new_row:
                                if (
                                    self.VALID_POSITIONS[row_index][col]
                                    == constants.VALID
                                    and self.CURRENT_POSITION[row_index][col]
                                    == constants.BLANK
                                    and row_index == new_row
                                ):
                                    return True
                                elif (
                                    self.VALID_POSITIONS[row_index][col] == 0
                                    and col != 3
                                ):
                                    row_index -= 1
                                else:
                                    return False

            return False

    def get_valid_moves(self):
        moves = []
        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                if (int(self.VALID_POSITIONS[r][c]) == constants.VALID) and (
                    int(self.CURRENT_POSITION[r][c]) == constants.BLANK
                ):
                    moves.append([r, c])
        return moves

    def save_game(self):
        # print("Saving moves:", self.moves_made)

        if len(self.moves_made) == 0:
            return

        if os.path.exists(constants.GAME_STATE_FILE):
            os.remove(constants.GAME_STATE_FILE)

        with open(constants.GAME_STATE_FILE, "w") as json_file:
            json.dump(self.moves_made, json_file, indent=2)

        print ("Storing moves in DB...")

        moves_json = json.dumps(self.moves_made, indent=2)
        print (moves_json)

        # Generate a random UUID
        new_uuid = uuid.uuid4()

        # Convert the UUID to a string if needed
        uuid_string = str(new_uuid)

        moves_to_store = [{
            "id": uuid_string,
            "name": "test",  # Update this
            "game_type": "9 mens",  # Update this
            "total_moves": len(self.moves_made),
            "game_mode": self.game_mode,
            "played_at":  self.start_time.now(),
            "moves": moves_json,
        }]

        self.db.save_moves(moves_to_store)

        print ("Stored moves in DB")

    def is_game_over(self):
        # Game is finished when a player loses
        if self.play1_pieces <= 2:
            return constants.PLAY2
        elif self.play2_pieces <= 2:
            return constants.PLAY1
        else:
            return None

    def move_piece(self, start_row, start_col, end_row, end_col, player):
        if self.is_move_valid(start_row, start_col, end_row, end_col):
            self.CURRENT_POSITION[start_row][start_col] = constants.BLANK
            self.CURRENT_POSITION[end_row][end_col] = player
            return True
        return False

    # Fixme - Player can remove from a mill if no other pieces are available (doesn't work for more than one mill and no free piece)
    def remove_piece(self, row, col, player):
        print("Removing piece:", row, col, player)
        if (
            self.CURRENT_POSITION[row][col] != player
            and self.CURRENT_POSITION[row][col] != constants.BLANK
        ):
            if not self.is_mill(row, col, self.CURRENT_POSITION[row][col]):
                self.CURRENT_POSITION[row][col] = constants.BLANK
                self.update_pieces()
                self.change_turn()
                return True
            if (
                self.is_mill(row, col, self.CURRENT_POSITION[row][col])
                and not self.has_free_pieces()
            ):
                self.CURRENT_POSITION[row][col] = constants.BLANK
                self.update_pieces()
                self.change_turn()
                return True

    def fly_piece(self, start_row, start_col, end_row, end_col, player):
        if self.is_move_valid(start_row, start_col, end_row, end_col):
            self.CURRENT_POSITION[start_row][start_col] = constants.BLANK
            self.CURRENT_POSITION[end_row][end_col] = player
            return True
        return False

    def is_mill(self, row, col, player):
        col_index = 0
        row_index = 0
        piece_count = 0

        if row == 3:
            if col > 3:
                col_index = 4
        if col == 3:
            if row > 3:
                row_index = 4

        while col_index < constants.COLS:
            if (
                self.VALID_POSITIONS[row][col_index] == constants.VALID
                and self.CURRENT_POSITION[row][col_index] == player
            ):
                piece_count += 1
            elif (
                self.VALID_POSITIONS[row][col_index] == constants.VALID
                and self.VALID_POSITIONS[row][col_index] != player
            ):
                piece_count = 0
            if row == 3 and col_index == 3:
                break
            col_index += 1
            if piece_count == 3:
                return True

        if piece_count == 3:
            return True

        piece_count = 0
        while row_index < constants.ROWS:
            if (
                self.VALID_POSITIONS[row_index][col] == constants.VALID
                and self.CURRENT_POSITION[row_index][col] == player
            ):
                piece_count += 1
            elif (
                self.VALID_POSITIONS[row_index][col] == constants.VALID
                and self.VALID_POSITIONS[row_index][col] != player
            ):
                piece_count = 0
            if row_index == 3 and col == 3:
                return False
            row_index += 1
            if piece_count == 3:
                return True

        if piece_count == 3:
            return True
        return False

    def has_free_pieces(self):
        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                if self.CURRENT_POSITION[r][
                    c
                ] == self.get_opp() and not self.is_mill_at_position(r, c):
                    return True  # Found a free piece belonging to the player
        return False

    def is_mill_at_position(self, row, col):
        player = self.CURRENT_POSITION[row][col]
        if player == constants.BLANK:
            return False  # No mill possible if the position is empty

        # Check horizontal and vertical lines
        if self.check_line(row, col, 0, 1, player) or self.check_line(
            row, col, 1, 0, player
        ):
            return True

        # Check diagonal lines
        if self.check_line(row, col, 1, 1, player) or self.check_line(
            row, col, 1, -1, player
        ):
            return True

        return False

    def check_line(self, row, col, dr, dc, player):
        for i in range(1, 3):  # Check up to 2 positions in the line
            r, c = row + i * dr, col + i * dc
            if (
                0 <= r < constants.ROWS
                and 0 <= c < constants.COLS
                and self.CURRENT_POSITION[r][c] != player
            ):
                return False  # The line is not valid if there is an opponent's piece
            elif (
                0 <= r < constants.ROWS
                and 0 <= c < constants.COLS
                and self.CURRENT_POSITION[r][c] == constants.BLANK
            ):
                return False  # The line is not valid if there is a blank space
        return True  # The line is valid (contains only player's pieces)

    def computer_make_move(self):
        potential_mill_moves = []
        block_opponent_mill_moves = []
        other_valid_moves = []

        # Check all possible moves for potential mills or blocking opponent's mills
        if self.phase == constants.PHASE1:
            for r, c in self.get_valid_moves():
                if self.would_form_mill(r, c, self.get_turn()):
                    potential_mill_moves.append((r, c, None, None))
                elif self.would_block_opponent_mill(r, c):
                    block_opponent_mill_moves.append((r, c, None, None))
                else:
                    other_valid_moves.append((r, c, None, None))

        elif self.phase == constants.PHASE2:
            for r in range(constants.ROWS):
                for c in range(constants.COLS):
                    if self.CURRENT_POSITION[r][c] == self.get_turn():
                        for new_r, new_c in self.get_valid_moves():
                            if self.get_player_pieces() == 3 or self.is_move_valid(
                                r, c, new_r, new_c
                            ):
                                if self.would_form_mill(new_r, new_c, self.get_turn()):
                                    potential_mill_moves.append((r, c, new_r, new_c))
                                elif self.would_block_opponent_mill(new_r, new_c):
                                    block_opponent_mill_moves.append(
                                        (r, c, new_r, new_c)
                                    )
                                else:
                                    other_valid_moves.append((r, c, new_r, new_c))

        # Select a move
        if potential_mill_moves:
            return random.choice(potential_mill_moves)
        elif block_opponent_mill_moves:
            return random.choice(block_opponent_mill_moves)
        elif other_valid_moves:
            return random.choice(other_valid_moves)
        else:
            return None

    def would_form_mill(self, row, col, player):
        # Temporarily place/move the piece
        original_value = self.CURRENT_POSITION[row][col]
        self.CURRENT_POSITION[row][col] = player
        # Check if this forms a mill
        forms_mill = self.is_mill(row, col, player)
        # Revert the board to its original state
        self.CURRENT_POSITION[row][col] = original_value

        return forms_mill

    def would_block_opponent_mill(self, row, col):
        # Temporarily place/move the piece
        original_value = self.CURRENT_POSITION[row][col]
        self.CURRENT_POSITION[row][col] = self.get_opp()
        # Check if this would form a mill for the opponent
        would_form_mill = self.is_mill(row, col, self.get_opp())
        # Revert the board to its original state
        self.CURRENT_POSITION[row][col] = original_value

        return would_form_mill

    def select_piece_to_remove(self):
        print("Selecting piece to remove...")
        # Select a piece of the opponent that is not in a mill
        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                if self.CURRENT_POSITION[r][c] == self.get_opp() and not self.is_mill(
                    r, c, self.get_opp()
                ):
                    return r, c
        # If all pieces are in mills, select any opponent's piece
        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                if self.CURRENT_POSITION[r][c] == self.get_opp():
                    return r, c
        return None
