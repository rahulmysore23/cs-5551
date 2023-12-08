import pygame
import sys
import constants


class Menu:
    def __init__(self):
        self.human_vs_computer_button_rect = None
        self.human_vs_computer_button = None
        self.human_vs_human_button_rect = None
        self.human_vs_human_button = None
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Nine/Six Men's Morris - Menu")
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
                    if self.human_vs_human_button_rect.collidepoint(event.pos):
                        self.selected_option = constants.H_VS_H
                    elif self.human_vs_computer_button_rect.collidepoint(event.pos):
                        # self.selected_option = None
                        self.selected_option = constants.H_VS_C

            self.screen.fill(constants.WHITE)

            # Load and display the background image
            background_image = pygame.image.load("./resources/background.jpg")
            self.screen.blit(background_image, (-200, -200))

            text = self.font.render("Nine/Six Men's Morris - Menu", True, constants.BLACK)
            text_rect = text.get_rect(center=(constants.SCREEN_WIDTH / 2, 100))
            self.screen.blit(text, text_rect)

            # Create buttons
            self.human_vs_human_button = pygame.draw.rect(
                self.screen, constants.GREEN, (150, 200, 280, 50)
            )
            text_hvh = self.font.render("Human vs Human", True, constants.BLACK)
            self.screen.blit(text_hvh, (175, 210))
            self.human_vs_human_button_rect = self.human_vs_human_button

            self.human_vs_computer_button = pygame.draw.rect(
                self.screen, constants.YELLOW, (150, 270, 280, 50)
            )
            text_hvc = self.font.render("Human vs Computer", True, constants.BLACK)
            self.screen.blit(text_hvc, (175, 280))
            self.human_vs_computer_button_rect = self.human_vs_computer_button

            pygame.display.flip()
            self.clock.tick(30)

    def get_selected_option(self):
        return self.selected_option
