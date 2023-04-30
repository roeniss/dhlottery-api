import json


class Lotto645BuyRequest:
    def __init__(self, games=None):
        """
        :param 게임은 다섯 개의 list 로 이루어져 있다. 각 게임은 여섯 칸 짜리 list 로 이루어져 있다. 각 칸은 1~45 의 숫자 또는 '자동'을 의미하는 "x" 를 사용한다.
         e.g. [["x", "x", "x", "x", "x"], ["x"], [1, 2, 3, 4, 15, 45], None, [3, 5, "x", "x", "x"]]
         - This example shows two auto games, one manual game, one half-auto game and forth game is not used.
        """
        self._games = games

        if not self._is_correct_games(games):
            raise RuntimeError(f"비정상적인 구매 요청입니다.\n{self.format()}")

    def _is_correct_games(self, games):
        return isinstance(games, list) and len(games) == 5 and all(map(lambda x: self._is_correct_game(x), games))

    def _is_correct_game(self, game):
        return game is None or (
            isinstance(game, list)
            and (len(game) == 6 or len(game) == 1)
            and (len(set(filter(lambda x: x != "x", game))) == len(list(filter(lambda x: x != "x", game))))
            and all(map(lambda x: x == "x" or 1 <= x <= 45, game))
        )

    def has_auto_game(self):
        return any(filter(lambda game: self._is_auto_game(game), self._filter_used_games()))

    def _is_auto_game(self, game):
        return self._get_auto_count_in_game(game) == 6

    def has_half_auto_game(self):
        return any(filter(lambda game: self._is_half_auto_game(game), self._filter_used_games()))

    def _is_half_auto_game(self, game):
        return 0 < self._get_auto_count_in_game(game) < 6 and (self._get_auto_count_in_game(game) != 1)

    def has_manual_game(self):
        return any(filter(lambda game: self._is_manual_game(game), self._filter_used_games()))

    def _is_manual_game(self, game):
        return self._get_auto_count_in_game(game) == 0

    def _get_auto_count_in_game(self, game):
        """한 게임 내에서의 자동번호 개수를 반환한다. 사용하지 않는 게임(None)에 대해선 사용할 수 없다."""
        return len(list(filter(lambda x: x == "x", game)))

    def get_game_count(self):
        return len(self._filter_used_games())

    def _filter_used_games(self):
        return list(filter(lambda x: x is not None, self._games))

    def format(self):
        return f"""[Lotto645 Buy Request]
Game A: {self._games[0]}
Game B: {self._games[1]}
Game C: {self._games[2]}
Game D: {self._games[3]}
Game E: {self._games[4]}
----------------------"""

    def create_dhlottery_request_param(self):
        params = []
        slots = ["A", "B", "C", "D", "E"]

        for i, game in enumerate(self._games):
            slot = slots[i]
            if game is None:
                continue
            elif self._is_auto_game(game):
                params.append({"genType": "0", "arrGameChoiceNum": None, "alpabet": slot})
            elif self._is_half_auto_game(game):
                raise NotImplementedError("반자동 모드는 아직 구현되지 않았습니다.")
            else:
                params.append({"genType": "0", "arrGameChoiceNum": game, "alpabet": slot})

        return json.dumps(params)
