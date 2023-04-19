import pygame
import sys


# Blocks sprite
class Blocks(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)


pygame.init()
pygame.mixer.init()


class Main:
    def __init__(self):
        # Game screen
        self.screen = pygame.display.set_mode((720, 700))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.game_on = True
        self.dt = 0
        # Player turns
        self.turns = 3
        # Player score
        self.score = 0
        # Blocks
        self.blocks_group = pygame.sprite.Group()
        self.size_decrease = False
        # Player position and dimensions
        self.player_x = 335
        self.player_y = 600
        self.player_pos = pygame.Vector2(self.player_x, self.player_y)
        self.player_width = 50
        self.player_height = 10
        # Ball
        self.ball = pygame.Rect(720 / 2 - 8, 700 / 2 - 8, 16, 16)
        self.ball_x_speed = 6
        self.ball_y_speed = 6
        # Level
        self.level = 1

        self.mouse_rect = pygame.Rect(0, 0, 75, 75)
        self.blocks_add()
        self.main_loop()

    def blocks_add(self):
        x_position = 25
        y_position = 125
        # Brick colors
        colors = (
            (139, 0, 0), (139, 0, 0), (255, 165, 0), (255, 165, 0), (0, 255, 0), (0, 255, 0), (144, 238, 144),
            (144, 238, 144))

        # Adding blocks to their group and setting their positions
        for row in range(8):
            for i in range(14):
                blocks = Blocks(45, 10, x_position, y_position, colors[row])
                x_position += 51
                self.blocks_group.add(blocks)
            x_position = 25
            y_position += 16

    # Text showing turns remaining
    def turns_text(self):
        font = pygame.font.Font("freesansbold.ttf", 60)
        text = font.render(f"0{self.turns}", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (50, 50)
        self.screen.blit(text, text_rect)

    # Text showing current score
    def score_text(self):
        font = pygame.font.Font("freesansbold.ttf", 60)
        text = font.render(f"0{self.score}", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (650, 50)
        self.screen.blit(text, text_rect)

    # Increases score depending on color of block destroyed
    def score_increase(self, block):
        if block.color == (144, 238, 144):
            self.score += 1
        elif block.color == (0, 255, 0):
            self.score += 3
        elif block.color == (255, 165, 0):
            self.score += 5
        elif block.color == (255, 0, 0):
            self.score += 7

    def main_loop(self):
        # Main game loop
        while self.game_on:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_on = False
                sys.exit()

            self.screen.fill("black")
            # Keys for controlling player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if self.player_pos.x > 0:
                    self.player_pos.x -= 250 * self.dt
            if keys[pygame.K_d]:
                if self.player_pos.x < 670:
                    self.player_pos.x += 250 * self.dt

            self.turns_text()
            self.score_text()

            # Player
            player = pygame.Rect(self.player_pos.x, self.player_pos.y, self.player_width, self.player_height)
            self.ball.x += self.ball_x_speed
            self.ball.y += self.ball_y_speed

            # Change ball direction if it collides with the player
            if pygame.Rect.colliderect(player, self.ball):
                self.ball_y_speed *= -1

            # Change ball direction if it collides with block
            for block in self.blocks_group:
                if pygame.Rect.colliderect(self.ball, block):
                    pygame.mixer.Sound("sounds/block_break.wav").play()
                    self.score_increase(block)

                    block.kill()
                    self.ball_y_speed *= -1

            # Change ball direction if it touches wall
            if self.ball.x > 690 or self.ball.x < 5:
                self.ball_x_speed *= -1
            if self.ball.y < 5:
                self.ball_y_speed *= -1
            if self.ball.y > 680:
                self.turns -= 1
                self.ball_y_speed *= -1
            if self.turns == 0:
                self.game_over()

            # Checks if player has reached top of screen and halves thier size for added difficulty
            if self.ball.y < 5:
                if not self.size_decrease:
                    self.player_width = self.player_width / 2
                    self.player_x -= self.player_width
                    self.size_decrease = True

            # Drawing and displaying everything
            self.blocks_group.draw(self.screen)
            pygame.draw.rect(self.screen, (0, 0, 255), player)
            pygame.draw.ellipse(self.screen, (255, 0, 0), self.ball)
            pygame.display.flip()

            # Next Level
            if not self.blocks_group:
                if self.level == 1:
                    self.level += 1
                    self.blocks_add()
                # Shows winning screen if player has beaten level 2
                else:
                    self.win_screen()

            # Setting clock so fps is 60
            self.dt = self.clock.tick(60) / 1000

    def game_over(self):
        self.screen.fill("black")
        self.game_on = False

        # Game over text
        font = pygame.font.Font("freesansbold.ttf", 40)
        text = font.render("Game Over", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (720 // 2, 700 // 2)
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.mixer.stop()
        pygame.mixer.Sound("sounds/game_over.wav").play()
        done = False
        while not done:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Checks if button is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Main()
            self.mouse_rect.center = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, (0, 0, 0), self.mouse_rect, 6, 1)
            button_x = 720 // 2 - 75
            button_y = 700 // 2 + 40
            retry_button = pygame.Rect(button_x, button_y, 150, 50)
            # Changes button color if mouse hovering over button
            if pygame.Rect.colliderect(self.mouse_rect, retry_button):
                pygame.draw.rect(self.screen, (255, 99, 99), retry_button)
            else:
                pygame.draw.rect(self.screen, (255, 0, 0), retry_button)

            # Button text
            button_font = pygame.font.Font("freesansbold.ttf", 20)
            retry_text = button_font.render("Retry", True, "white")
            retry_text_rect = retry_text.get_rect(bottomright=(button_x + 100, button_y + 35))
            self.screen.blit(retry_text, retry_text_rect)

            pygame.display.flip()

    # Stops game and shows win screen
    def win_screen(self):
        self.screen.fill("black")
        self.game_on = False

        # Win text
        font = pygame.font.Font("freesansbold.ttf", 40)
        text = font.render("You Win!", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (720 // 2, 700 // 2)
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.mixer.stop()
        pygame.mixer.Sound("sounds/you_win.wav").play()
        done = False
        while not done:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Main()
            self.mouse_rect.center = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, (0, 0, 0), self.mouse_rect, 6, 1)
            button_x = 720 // 2 - 75
            button_y = 700 // 2 + 40
            play_button = pygame.Rect(button_x, button_y, 150, 50)
            # Changes button color if mouse hovering over button
            if pygame.Rect.colliderect(self.mouse_rect, play_button):
                pygame.draw.rect(self.screen, (144, 238, 144), play_button)
            else:
                pygame.draw.rect(self.screen, (0, 255, 0), play_button)

            # Button text
            button_font = pygame.font.Font("freesansbold.ttf", 20)
            play_text = button_font.render("Play Again", True, "white")
            play_text_rect = play_text.get_rect(bottomright=(button_x + 100, button_y + 35))
            self.screen.blit(play_text, play_text_rect)


Main()
