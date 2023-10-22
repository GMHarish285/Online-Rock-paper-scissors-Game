import pygame, pickle
from network import Network


pygame.font.init()
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Client')


class Button:
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 150
        self.height = 100

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(self.text, True, 'white')
        screen.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]  # pos will be pos of mouse
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:  # checking if mouse is colliding with button
            return True
        else:
            return False


def redraw_screen(screen, game, p):
    screen.fill('grey')

    if not game.connected():
        font = pygame.font.SysFont('comicsans', 80)
        text = font.render('Waiting for player...', True, 'red', True)  # 4th arg for bold
        screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render('Your move', True, 'cyan', True)  # 4th arg for bold
        screen.blit(text, (80, 200))

        text = font.render('Opponent move', True, 'cyan', True)  # 4th arg for bold
        screen.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_went():
            text1 = font.render(move1, True, 'black')
            text2 = font.render(move2, True, 'black')
        else:
            if game.p1_went and p == 0:
                text1 = font.render(move1, True, 'black')
            elif game.p1_went:
                text1 = font.render('Locked in', True, 'black')
            else:
                text1 = font.render('Waiting...', True, 'black')

            if game.p2_went and p == 1:
                text2 = font.render(move2, True, 'black')
            elif game.p2_went:
                text2 = font.render('Locked in', True, 'black')
            else:
                text2 = font.render('Waiting...', True, 'black')

            if p == 1:
                screen.blit(text2, (100, 350))
                screen.blit(text1, (400, 350))
            else:
                screen.blit(text1, (100, 350))
                screen.blit(text2, (400, 350))

        for button in buttons:
            button.draw(screen)

    pygame.display.update()


buttons = [Button('Rock', 50, 500, 'red'), Button('Paper', 250, 500, 'green'), Button('Scissors', 450, 500, 'blue')]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_p())
    print('You are player', player)
    clock.tick(60)

    while run:
        try:
            game = n.send('get')
        except:
            run = False
            print('Could not get game')
            break

        if game.both_went():
            redraw_screen(screen, game, player)
            pygame.time.delay(500)
            try:
                game = n.send('reset')
            except:
                run = False
                print('Could not get game')
                break

            font = pygame.font.SysFont('comicsans', 90)
            text = font.render('You won!', True, 'red')
            if (game.winner() == 1 and player == 1) or (game.winner == 0 and player == 0):
                text = font.render('You won!', True, 'red')
            elif game.winner == -1:
                text = font.render('Tie!', True, 'red')
            elif game.winner == -1:
                text = font.render('You lost!', True, 'red')

            screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1_went:
                                n.send(button.text)
                        else:
                            if not game.p2_went:
                                n.send(button.text)

        redraw_screen(screen, game, player)


main()
