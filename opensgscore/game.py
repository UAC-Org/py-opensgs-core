from dataclasses import dataclass
import random
from typing import Optional


@dataclass
class Player:
    name: str
    cards: list
    identity: str
    general: str
    equipments: list
    hp: int
    max_hp: int


def empty_player(name: str = "") -> Player:
    return Player(
        name, cards=[], identity="", general="", equipments=[], hp=0, max_hp=0
    )


def is_empty_player(player: Player) -> bool:
    return (
        player.name == "" and player.cards == [] and player.general == "" and
        player.identity == "" and player.equipments == [] and
        player.hp == 0 and player.max_hp == 0
    )


class Game:
    players: list[Player]

    def __init__(
        self, cards: list, generals: dict, equipments: list,
        players: Optional[list[Player]] = None
    ):
        self.players = [] if not players else players
        self.cards = cards
        self.generals = generals
        self.equipments = equipments

    def __str__(self):
        return f"""Game(
    players={self.players},
    cards={self.cards},
    generals={self.generals},
    equipments={self.equipments}
)"""

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Game(self.cards, self.generals, self.equipments, self.players)

    def reset(
        self, cards: list, generals: dict, equipments: list,
        players: Optional[list[Player]] = None
    ):
        self.players = [] if not players else players
        self.cards = cards
        self.generals = generals
        self.equipments = equipments

    def get_player(self, name: str) -> Player:
        for player in self.players:
            if player.name == name:
                return player
        return empty_player()

    def get_player_index(self, name: str) -> int:
        for i, player in enumerate(self.players):
            if player.name == name:
                return i
        return -1

    def add_player(self, player: Player):
        if self.get_player_index(player.name) < 0:
            self.players.append(player)

    def remove_player(self, name: str):
        index = self.get_player_index(name)
        if index >= 0:
            self.players.pop(index)

    def _generate_identities(self) -> list[str]:
        """
        Generate identities for all players.
        """
        ids = []
        rebels = (len(self.players) // 2)
        loyals = (len(self.players) - rebels)
        ids.extend(["反贼"] * (rebels // 2))
        ids.extend(["忠臣"] * (loyals - 1))
        ids.append("主公")
        ids.extend(["内奸"] * (len(self.players) - len(ids)))
        random.shuffle(ids)
        return ids

    def apply_identity(self, name: str, identity: str):
        player = self.get_player(name)
        player.identity = identity
        self.players[self.get_player_index(name)] = player

    def apply_all_identities(self):
        """
        Apply identities to all players.
        """
        ids = self._generate_identities()
        for pl, id in zip(self.players, ids):
            self.apply_identity(pl.name, id)