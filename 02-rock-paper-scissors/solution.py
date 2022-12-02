# coding=utf-8
from enum import Enum
from typing import List, Tuple


def read_input() -> List[str]:
    input_file_name = "input.txt"

    try:
        with open(input_file_name) as input_file:
            input_lines = input_file.read()
            if not input_lines:
                raise Exception(f"File {input_file_name} is empty")
            return [line.strip() for line in input_lines.split("\n")]
    except EnvironmentError as e:
        raise Exception(f"File {input_file} is missing or invalid") from e


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Decrypter:
    class Shapes:
        ROCK = ["A", "X"]
        PAPER = ["B", "Y"]
        SCISSORS = ["C", "Z"]

    def _decrypt_move(self, shape: str) -> Shape:
        if shape in self.Shapes.ROCK:
            return Shape.ROCK
        if shape in self.Shapes.PAPER:
            return Shape.PAPER
        if shape in self.Shapes.SCISSORS:
            return Shape.SCISSORS

    def decrypt_strategy(self, encrypted_moves: List[str]) -> List[Tuple[Shape, Shape]]:
        decrypted_moves = []
        for line in encrypted_moves:
            first_player_shape, second_player_shape = line.split(" ")
            decrypted_moves.append((self._decrypt_move(first_player_shape), self._decrypt_move(second_player_shape)))
        return decrypted_moves


class TwoStepDecrypter(Decrypter):
    class Shapes(Decrypter.Shapes):
        ROCK = "A"
        PAPER = "B"
        SCISSORS = "C"

    class RoundResult:
        LOST = "X"
        DRAW = "Y"
        WIN = "Z"

    def decrypt_strategy(self, encrypted_moves):
        decrypted_moves = []
        for line in encrypted_moves:
            first_player_shape, desired_round_result = line.split(" ")
            decrypted_first_player_move = self._decrypt_move(first_player_shape)
            second_player_move = self.get_move_based_on_result(decrypted_first_player_move, desired_round_result)
            decrypted_moves.append((decrypted_first_player_move, second_player_move))
        return decrypted_moves

    def get_move_based_on_result(self, first_player_move, desired_round_result):
        if desired_round_result == self.RoundResult.DRAW:
            return first_player_move
        if desired_round_result == self.RoundResult.WIN:
            if first_player_move == Shape.ROCK:
                return Shape.PAPER
            if first_player_move == Shape.PAPER:
                return Shape.SCISSORS
            if first_player_move == Shape.SCISSORS:
                return Shape.ROCK
        if desired_round_result == self.RoundResult.LOST:
            if first_player_move == Shape.ROCK:
                return Shape.SCISSORS
            if first_player_move == Shape.PAPER:
                return Shape.ROCK
            if first_player_move == Shape.SCISSORS:
                return Shape.PAPER


class Game:
    class Result(Enum):
        LOST = 0
        DRAW = 3
        WIN = 6

    def __init__(self, moves):
        self.moves = moves

    def calculate_round_score_second_player(self, first_player_move: Shape, second_player_move: Shape) -> Result:
        if first_player_move == second_player_move:
            return self.Result.DRAW
        if (
            (first_player_move == Shape.ROCK and second_player_move == Shape.PAPER)
            or (first_player_move == Shape.SCISSORS and second_player_move == Shape.ROCK)
            or (first_player_move == Shape.PAPER and second_player_move == Shape.SCISSORS)
        ):
            return self.Result.WIN
        return self.Result.LOST

    def calculate_total_score_second_player(self) -> int:
        total_score = 0
        for first_player_move, second_player_move in self.moves:
            total_score += second_player_move.value
            total_score += self.calculate_round_score_second_player(first_player_move, second_player_move).value
        return total_score


if __name__ == "__main__":
    input_lines = read_input()
    strategy = Decrypter().decrypt_strategy(input_lines)
    print(Game(strategy).calculate_total_score_second_player())

    second_part_strategy = TwoStepDecrypter().decrypt_strategy(input_lines)
    print(Game(second_part_strategy).calculate_total_score_second_player())
