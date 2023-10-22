class Game:
    def __init__(self, id):
        self.p1_went = False  # whether p1 made its moved or not
        self.p2_went = False  # whether p2 made its moved or not
        self.ready = False
        self.id = id  # id of each game, so that multiple games can take place
        self.moves = [None, None]  # [move of p1, move of p2]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, player):
        return self.moves[player]

    def play(self, player, move):
        self.moves[player] = move  # updating the move
        if player == 0:
            self.p1_went = True
        else:
            self.p2_went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1_went and self.p2_went

    def winner(self):
        p1 = self.moves[0].upper()[0]  # getting the first letter of the move of p1 in uppercase
        p2 = self.moves[1].upper()[0]  # getting the first letter of the move of p2 in uppercase

        winner = -1  # if winner remains -1 it will be a tie; 0 - p1 is winner; 1 - p2 is winner
        if p1 == 'R' and p2 == 'P':
            winner = 1
        elif p1 == 'R' and p2 == 'S':
            winner = 0
        elif p1 == 'P' and p2 == 'R':
            winner = 0
        elif p1 == 'P' and p2 == 'S':
            winner = 1
        elif p1 == 'S' and p2 == 'R':
            winner = 1
        elif p1 == 'S' and p2 == 'P':
            winner = 0

        return winner

    def reset(self):
        self.p1_went = False
        self.p2_went = False
