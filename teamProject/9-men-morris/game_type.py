import pygame
import sys
import constants


class GameTypeMenu:
    def __init__(self):
        self.nine_men_button_rect = None
        self.nine_men_button = None
        self.six_men_button_rect = None
        self.six_men_button = None
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Nine/Six Men's Morris - Game Type")
        self.clock = pygame.time.Clock()
        self.selected_option = None
        self.font = pygame.font.Font(None, 36)

    def display_menu(self):
        while self.selected_option is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.nine_men_button_rect.collidepoint(event.pos):
                        self.selected_option = constants.NINE_MEN_MORRIS
                    elif self.six_men_button_rect.collidepoint(event.pos):
                        self.selected_option = constants.SIX_MEN_MORRIS

            self.screen.fill(constants.WHITE)

            # Load and display the background image
            background_image = pygame.image.load("./resources/background.jpg")
            self.screen.blit(background_image, (-200, -200))

            text = self.font.render(
                "Nine/Six Men's Morris - Select Game Type", True, constants.BLACK
            )
            text_rect = text.get_rect(center=(constants.SCREEN_WIDTH / 2, 100))
            self.screen.blit(text, text_rect)

            # Create buttons
            self.nine_men_button = pygame.draw.rect(
                self.screen, constants.GREEN, (150, 200, 280, 50)
            )
            text_nine_men = self.font.render("9 Men", True, constants.BLACK)
            self.screen.blit(text_nine_men, (225, 210))
            self.nine_men_button_rect = self.nine_men_button

            self.six_men_button = pygame.draw.rect(
                self.screen, constants.YELLOW, (150, 270, 280, 50)
            )
            text_six_men = self.font.render("6 Men", True, constants.BLACK)
            self.screen.blit(text_six_men, (225, 280))
            self.six_men_button_rect = self.six_men_button

            pygame.display.flip()
            self.clock.tick(30)

    def get_selected_option(self):
        return self.selected_option
