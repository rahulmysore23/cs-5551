import constants
from GUI import NineMensMorrisGUI
from NineMensMorrisGame import NineMensMorrisGame
from game_type import GameTypeMenu
from menu import Menu
from db import GameDatabaseInterface
from SixMenMorrisBoard import SixMenMorrisBoard


def run_game(selected_option, mens):
    game = None
    database_interface = GameDatabaseInterface()

    if mens == constants.NINE_MEN_MORRIS:
        if selected_option == constants.H_VS_H:
            game = NineMensMorrisGame(database_interface, constants.TOTAL_MENS, constants.VALID_POSITIONS)
            game.game_mode = constants.H_VS_H
        elif selected_option == constants.H_VS_C:
            # Initialize game for human vs computer mode
            game = NineMensMorrisGame(database_interface, constants.TOTAL_MENS, constants.VALID_POSITIONS)
            game.game_mode = constants.H_VS_C
    elif mens == constants.SIX_MEN_MORRIS:
        if selected_option == constants.H_VS_H:
            game = NineMensMorrisGame(database_interface, constants.TOTAL_SIX_MENS, constants.VALID_POSITIONS_SIX_MENS)
            game.game_mode = constants.H_VS_H
        elif selected_option == constants.H_VS_C:
            # Initialize game for human vs computer mode
            game = NineMensMorrisGame(database_interface, constants.TOTAL_SIX_MENS, constants.VALID_POSITIONS_SIX_MENS)
            game.game_mode = constants.H_VS_C

    if game is not None:
        if mens == constants.SIX_MEN_MORRIS:
            gui = SixMenMorrisBoard(game)
        else:
            gui = NineMensMorrisGUI(game)
        gui.main_loop()


if __name__ == "__main__":
    game_type_menu = GameTypeMenu()
    game_type_menu.display_menu()
    selected_game_type = game_type_menu.get_selected_option()

    menu = Menu()
    menu.display_menu()
    selected_option = menu.get_selected_option()
    run_game(selected_option, selected_game_type)
