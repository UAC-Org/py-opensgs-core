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
    "playerdie", "err_gennavail", "err_mhpmin"
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
        if general in self.generals:
            player.general = general
            player.hp = player.max_hp = self.generals[general]
            self.generals.pop(general)
        else:
            self.err_gennavail(self)  # type: ignore

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

    def change_maxhp(self, name: str, d: int):
        player = self.get_player(name)
        player.max_hp += d
        if player.max_hp < 1:
            player.max_hp = 1
            self.err_mhpmin(self)  # type: ignore
        elif player.hp > player.max_hp:
            player.hp = player.max_hp
            self.err_hpoverflow(self)  # type: ignore

    def hpincr1(self, name: str):
        self.change_hp(name, 1)

    def hpdecr1(self, name: str):
        self.change_hp(name, -1)

    def maxhpincr1(self, name: str):
        self.change_maxhp(name, 1)

    def maxhpdecr1(self, name: str):
        self.change_maxhp(name, -1)

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def draw_cards(self, name: str, n: int = 1, top: bool = False):
        player = self.get_player(name)
        cards = self.cards[:n] if not top else self.cards[-n:]
        self.cards = self.cards[n:] if not top else self.cards[:-n]
        player.cards.extend(cards)
        # for c in cards:
        #     self.cards.remove(c)

    def throw_cards(self, name: str, *cards: str, deprecate: bool = False):
        player = self.get_player(name)
        for c in cards:
            player.cards.remove(c)
            if not deprecate:
                self.cards.append(c)

    def equip(self, name: str, equipment: str):
        player = self.get_player(name)
        if equipment in player.cards:
            player.equipments.append(equipment)
            player.cards.remove(equipment)
        else:
            self.err_notfound(self)  # type: ignore

    def unequip(self, name: str, equipment: str):
        player = self.get_player(name)
        if equipment in player.equipments:
            player.equipments.remove(equipment)
            player.cards.append(equipment)
        else:
            self.err_notfound(self)  # type: ignore