import random
from enum import Enum
from abc import ABC, abstractmethod

class MoveResult(Enum):
    INVALID = 0
    VALID = 1
    GAMEOVER = 2

class Player(ABC):
    @abstractmethod
    def input(self):
        pass

class HumanPlayer(Player):
    def input(self):
        return input("Enter move (w/a/s/d): ").strip()
    
class ComPlayer(Player):
    def input(self):
        return random.choice("wasd")

class Game:
    PROB_4 = 0.1

    def __init__(self, player:Player=HumanPlayer(), size:int=4):
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.player = player
        self.size = size
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        vacant = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if vacant:
            i, j = random.choice(vacant)
            self.board[i][j] = 4 if random.random() < self.PROB_4 else 2
            return True
        return False

    def show(self):
        for row in self.board:
            print(*["{:5d}".format(x) for x in row])
        print(f"score: {self.score}")

    def rotate_board(self):
        self.board = [list(reversed(col)) for col in zip(*self.board)]
       

    def combine_line(self, line):
        d = []
        score_add = 0
        flag = True
        for value in line:
            if value == 0:
                continue
            if flag and d and d[-1] == value:
                d[-1] *= 2
                score_add += d[-1]
                flag = False
            else:
                d.append(value)
                flag = True
        return d + [0] * (self.size - len(d)), score_add
    
    def move_left(self):
        moved = False
        for i in range(self.size):
            new_row, score_add = self.combine_line(self.board[i])
            if self.board[i] != new_row:
                moved = True
                self.board[i] = new_row
                self.score += score_add
        return moved
            
    def move(self, direction) -> MoveResult:
        rotation = {"a":0, "s":1, "d":2, "w":3}
        if direction not in rotation:
            print("Illegal move!")
            return MoveResult.INVALID
        
        for _ in range(rotation[direction]):
            self.rotate_board()
        moved = self.move_left()
        for _ in range(4 - rotation[direction]):
            self.rotate_board()

        if not moved:
            return MoveResult.INVALID
        
        if not self.add_random_tile():
            return MoveResult.GAMEOVER
        if self.check_gameover():
            return MoveResult.GAMEOVER
        return MoveResult.VALID

    def check_gameover(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return False
                if j < self.size - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < self.size - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True

    def read_input(self):
        return self.player.input()

    def start(self):
        self.show()
        if self.check_gameover():
            print("Game over!")
            return self.score
        while True:
            direction = self.read_input()
            result = self.move(direction)
            self.show()
            if result == MoveResult.INVALID:
                print("Invalid move!")
            elif result == MoveResult.GAMEOVER:
                print("Game over!")
                print(f"score: {self.score}")
                return self.score
    


if __name__ == "__main__":
    game = Game()
    game.start()
