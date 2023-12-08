import unittest
import constants

from NineMensMorrisGame import NineMensMorrisGame


class TestNineMensMorrisGame(unittest.TestCase):
    def setUp(self):
        self.game = NineMensMorrisGame()

    def test_initial_board_state(self):
        if self.game.turn != constants.PLAY1:
            self.fail("Board should be initialized with player 1's turn")

        if self.game.phase != constants.PHASE1:
            self.fail("Board should be initialized with Phase 1")

        if self.game.counter != 0:
            self.fail("Board should be initialized with moves counter 0")

        if self.game.play1_counter != 0:
            self.fail("Board should be initialized with player 1 moves counter 0")

        if self.game.play2_counter != 0:
            self.fail("Board should be initialized with player 2 moves counter 0")

        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                if int(self.game.CURRENT_POSITION[r][c]) != constants.BLANK:
                    self.fail("Initial board state is wrong for row and col: " + str(r) + ":" + str(c))

    def test_change_turn(self):
        self.game.make_move(4, 4, None, None)
        if self.game.get_turn() != constants.PLAY2:
            self.fail("Turn not changed, Expected player 2")

        self.game.make_move(4, 3, None, None)
        if self.game.get_turn() != constants.PLAY1:
            self.fail("Turn not changed, Expected player 1")
        self.game.remove_piece(4, 4)
        self.game.remove_piece(4, 3)

    def test_place_piece(self):
        self.game.make_move(4, 3, None, None)
        if self.game.CURRENT_POSITION[4][3] != constants.PLAY1:
            self.fail("Piece not placed")
        self.game.remove_piece(4, 3)

    def test_move_piece(self):
        # Test moving a piece on the board
        pass

    def test_remove_piece(self):
        self.game.make_move(4, 3, None, None)
        if self.game.CURRENT_POSITION[4][3] != constants.PLAY1:
            self.fail("Piece not placed")

        self.game.remove_piece(4, 3)
        if self.game.CURRENT_POSITION[4][3] != constants.BLANK:
            self.fail("Piece not removed")

    def test_save_game(self):
        self.game.make_move(4, 3, None, None)
        if self.game.CURRENT_POSITION[4][3] != constants.PLAY1:
            self.fail("Piece not placed")

        self.game.save_game()

        state_file = open(constants.GAME_STATE_FILE, "r")
        data = state_file.read()
        state_file.close()

        if data != "d3":
            self.fail("game not saved properly")

        self.game.remove_piece(4, 3)

    def test_game_over(self):
        # Test the game-over condition
        pass


if __name__ == '__main__':
    unittest.main()
