import enum
import json
import os
import string


class Lotto645GameType(enum.IntEnum):
    AUTO = 0
    MANUAL = 1
    SEMIAUTO = 2


class Lotto645BuyRequest:
    MAX_NUMBER_COUNT_IN_GAME = 6
    MAX_GAME_COUNT = 5

    def __init__(self, games):
        """
        :param 게임은 다섯 개 이하의 list 로 이루어져 있다.
        각 게임은 여섯 칸 이하의 list 로 이루어져 있다. 각 칸은 1~45 의 숫자를 사용한다.
        - 숫자가 없는 list는 자동을 의미한다.
        - 여섯개의 숫자를 갖는 list는 수동을 의미한다.
        - 한개 이상 여섯개 미만의 숫자를 갖는 list는 반자동을 의미한다.
        e.g. [[], [], [], [1, 2], [1, 2, 3, 4, 15, 45]]
        - This example shows three auto games, one semi-auto game and one manual game.
        """
        self._games = games

        if not self._is_correct_games(games):
            raise RuntimeError(f"비정상적인 구매 요청입니다.\n{self.format()}")

    def _is_correct_games(self, games):
        # fmt: off
        return (isinstance(games, list)
            and len(games) <= self.MAX_GAME_COUNT
            and all(map(lambda x: self._is_correct_game(x), games)))
        # fmt: on

    def _is_correct_game(self, game):
        # fmt: off
        return (isinstance(game, list)
            and len(game) <= self.MAX_NUMBER_COUNT_IN_GAME
            and all(map(lambda x: isinstance(x, int) and 1 <= x <= 45, game))
            and len(game) == len(set(game)))
        # fmt: on

    def has_auto_game(self):
        return any(filter(lambda game: self._is_auto_game(game), self._filter_used_games()))

    def _is_auto_game(self, game):
        return self._get_manual_count_in_game(game) == 0

    def has_semi_auto_game(self):
        return any(filter(lambda game: self._is_semi_auto_game(game), self._filter_used_games()))

    def _is_semi_auto_game(self, game):
        return 0 < self._get_manual_count_in_game(game) < self.MAX_NUMBER_COUNT_IN_GAME

    def has_manual_game(self):
        return any(filter(lambda game: self._is_manual_game(game), self._filter_used_games()))

    def _is_manual_game(self, game):
        return self._get_manual_count_in_game(game) == self.MAX_NUMBER_COUNT_IN_GAME

    def _get_auto_count_in_game(self, game):
        return self.MAX_NUMBER_COUNT_IN_GAME - len(game)

    def _get_manual_count_in_game(self, game):
        return len(game)

    def get_game_count(self):
        return len(self._filter_used_games())

    def _filter_used_games(self):
        return list(filter(lambda x: x is not None, self._games))

    def _get_game_type(self, game):
        if self._is_auto_game(game):
            return Lotto645GameType.AUTO
        if self._is_manual_game(game):
            return Lotto645GameType.MANUAL
        if self._is_semi_auto_game(game):
            return Lotto645GameType.SEMIAUTO

        raise RuntimeError("지원하지 않는 게임 타입입니다.")

    def _get_gen_type(self, game_type):
        if not isinstance(game_type, Lotto645GameType):
            raise RuntimeError("지원하지 않는 게임 타입입니다.")

        return str(game_type.value)

    def _encode_game(self, slot, game):
        game_type = self._get_game_type(game)
        # fmt: off
        return {
            "genType": self._get_gen_type(game_type),
            "arrGameChoiceNum": ",".join(map(str, game)) if game_type != Lotto645GameType.AUTO else None,
            "alpabet": slot
        }
        # fmt: on

    def format(self):
        return f"""
[Lotto645 Buy Request]
{os.linesep.join(f'Game {string.ascii_uppercase[i]}: {game}' for i, game in enumerate(self._games))}
"""

    def create_dhlottery_request_param(self):
        params = []

        for i, game in enumerate(self._games):
            slot = string.ascii_uppercase[i]
            params.append(self._encode_game(slot, sorted(game)))

        return json.dumps(params)
