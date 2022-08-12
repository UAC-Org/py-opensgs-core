from dataclasses import dataclass
import random
from typing import Optional

from .util import plant_trigger


@dataclass(eq=True)
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


@plant_trigger(
    "postinit", "err_dup", "err_notfound", "err_hpoverflow", "iddist",
    "playerdie"
)
class Game:
    players: list[Player]
    emperor: Player
    current: int

    def __init__(
        self, cards: list[str], generals: dict[str, int],
        equipments: list[str], players: Optional[list[Player]] = None
    ):
        self.reset(cards, generals, equipments, players)
        self.postinit(self)  # type: ignore

    def __str__(self):
        return f"""Game(
    players={self.players},
    cards={self.cards},
    generals={self.generals},
    equipments={self.equipments}
)"""

    def __repr__(self):
        return self.__str__()

    def __next__(self):
        if self.current == 0:
            self.current = self.get_player_index(self.emperor.name) - 1
        self.current = (self.current + 1) % len(self.players)
        return self.players[self.current]

    def reset(
        self, cards: list, generals: dict, equipments: list,
        players: Optional[list[Player]] = None
    ):
        self.players = [] if not players else players
        self.cards = cards
        self.generals = generals
        self.equipments = equipments
        self.emperor = empty_player()
        self.current = 0

    def get_player(self, name: str) -> Player:
        for player in self.players:
            if player.name == name:
                return player
        return empty_player()

    def get_player_index(self, name: str) -> int:
        for i, player in enumerate(self.players):
            if player.name == name:
                return i
        self.err_notfound(self)  # type: ignore
        return -1

    def add_player(self, player: Player):
        if self.get_player_index(player.name) < 0:
            self.players.append(player)
        else:
            self.err_dup(self)  # type: ignore

    def remove_player(self, name: str):
        index = self.get_player_index(name)
        if index >= 0:
            self.players.pop(index)
        else:
            self.err_notfound(self)  # type: ignore

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
            if id == "主公":
                self.emperor = pl
        self.iddist(self)  # type: ignore

    def apply_general(self, name: str, general: str):
        player = self.get_player(name)
        player.general = general
        player.hp = player.max_hp = self.generals[general]
        self.players[self.get_player_index(name)] = player
        self.generals.pop(general)

    def check_all_generals(self):
        return all(g.general for g in self.players)

    def change_hp(self, name: str, hp: int):
        player = self.get_player(name)
        player.hp += hp
        if player.hp > player.max_hp:
            player.hp = player.max_hp
            self.err_hpoverflow(self)  # type: ignore
        elif player.hp < 0:
            player.hp = 0
            self.playerdie(self)  # type: ignore
        self.players[self.get_player_index(name)] = player

    def incr1(self, name: str):
        self.change_hp(name, 1)

    def decr1(self, name: str):
        self.change_hp(name, -1)