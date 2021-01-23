from typing import List, Dict, Tuple, Union, Optional, Any
import random


################### Read Before Play ###################
# Each player is given 37000 golds at the start of the game, and 1000 gold
# every time they pass the starting point.
# By stepping on the Fate and Change grid, you will pick up a card which has a
# random effect on you.
# On the Airport grid, you can buy the airport if no one owns it, otherwise you
# will have to pay the person 2*n - 100, where n is the number of airports they
# own
# On the RealEstate grid, when no one owns it, you are able to buy it; if you
# owns it, you can upgrade it to a higher level before reaching max (i.e. you
# can spend money and build more buildings on that grid, so that you can
# charge more whenever others step on it.
# If you unfortunately enter the jail, you wont be able to move for 2 rounds.


grid_en = {'ZhSh': 'Zhongshan Road', 'Huai': 'Huaihai West Road',
           'PDJC': 'Pu Dong Airport', 'YanA': 'Yan\'an Road',
           'Heng': 'Hengshan Road', 'FuXing': 'Fuxing Road',
           'Dian': 'Power Company', 'PDDD': 'PuDong Avenue',
           'ShJi': 'Shiji Avenue', 'Bin': 'BingJiang Road',
           'WaiB': 'Waibai Bridge', 'LuJZ': 'Lujiazui',
           'HQJC': 'Hongqiao Airport', 'ZiLaiS': 'Water Plant',
           'XuJiaH': 'Xujiahui Road', 'WaiTan': 'Wai Tan', 'H-Way': 'Highway',
           'NanJ': 'Nanjing Road'}


def refresh_list(lst: list) -> list:
    """Put the first item in the list to the end
    Return a list
    """
    lst.append(lst.pop(0))
    return lst


def _shuffle(dic: dict) -> List[int]:
    """Randomly shuffle keys of a dict
    Return the order of Chance / Fate cards
    """
    lst = []
    for i in range(len(dic)):
        lst.append(i)
    random.shuffle(lst)
    return lst


class Grid:
    id_: int
    name: str
    fee: Any

    def __init__(self, id_: int, name: str) -> None:
        """Initialize a Grid
        """
        self.id_ = id_
        self.name = name

    def __str__(self) -> None:
        """An abstract method
        """
        pass


class RealEstate(Grid):
    id_: int
    name: str
    price: Dict[int, int]
    fee: Dict[int, int]

    def __init__(self, id_: int, name: str, price_list: List[int],
                 fee_list: List[int]) -> None:
        """Initialize a RealEstate on a Grid
        - id_ is the id of this RealEstate
        - name is the name of this RealEstate
        - price is the price to buy / upgrade this RealEstate if no one owns it:
            0: Buy an empty ground
            1: upgrade to one house
            2: upgrade to two houses
            3: upgrade to one hotel
        - fee_list is the fee:
            0: Empty Ground
            1: one house
            2: two houses
            3: one hotel
        """
        Grid.__init__(self, id_, name)
        self.price = {}
        self.fee = {}
        for i in range(len(fee_list)):
            self.price[i] = price_list[i]
            self.fee[i] = fee_list[i]

    def __str__(self) -> str:
        """Return a description of this RealEstate
        """
        head = '+' + '-' * 67 + '+'
        left1 = f'| Buy an empty ground: {self.price[0]}'
        left2 = f'| Upgrade to one house: {self.price[1]}'
        left3 = f'| Upgrade to two houses: {self.price[2]}'
        left4 = f'| Upgrade to one hotel: {self.price[3]}'
        str1 = f'passing fee for empty ground: {self.fee[0]}'
        str2 = f'passing fee for one house: {self.fee[1]}'
        str3 = f'passing fee for two houses: {self.fee[2]}'
        str4 = f'passing fee for one hotel: {self.fee[3]}'
        len1 = 69 - 33 - len(str1) - 1
        len2 = 69 - 33 - len(str2) - 1
        len3 = 69 - 33 - len(str3) - 1
        len4 = 69 - 33 - len(str4) - 1
        price = f'{left1:<33}' + f'{str1}' + ' ' * len1 + '|\n' + \
                f'{left2:<33}' + f'{str2}' + ' ' * len2 + '|\n' + \
                f'{left3:<33}' + f'{str3}' + ' ' * len3 + '|\n' + \
                f'{left4:<33}' + f'{str4}' + ' ' * len4 + '|\n'
        return grid_en[self.name] + '\n' + head + '\n' + price + head + \
            '\n'


class Airport(Grid):
    id_: int
    name: str
    price: int
    fee: int

    def __init__(self, id_: int, name: str, price: int, fee: int) -> None:
        """Initialize an Airport
        - price: the price the buy this airport
        - fee: the fee a player other than yourself should pay
        """
        Grid.__init__(self, id_, name)
        self.price = price
        self.fee = fee

    def __str__(self) -> str:
        """Return a description of this Airport
        """
        head = '+' + '-' * 67 + '+'
        str1 = f'| Buy this airport: {self.price}'
        str2 = f'| passing fee if you have one airport: {self.fee}'
        str3 = f'| passing fee if you have two airport: {2 * self.fee - 100}'
        price = f'{str1:<68}|\n' + f'{str2:<68}|\n' + f'{str3:<68}|\n'
        return grid_en[self.name] + '\n' + head + '\n' + price + head + \
            '\n'


class WaterPlant(Grid):
    id_: int
    name: str
    price: int

    def __init__(self, id_: int, name: str, price: int) -> None:
        """Initialize an WaterPlant
        - price: the price the buy this airport
        - fee: the fee a player other than yourself should pay
        """
        Grid.__init__(self, id_, name)
        self.price = price

    def __str__(self) -> str:
        """Return a description
        """
        head = '+' + '-' * 67 + '+'
        str1 = f'| Buy this water plant: {self.price}'
        str2 = '| passing fee if you have one water plant: 100 * the ' \
               'number of dice'
        str3 = '| passing fee if you have two water plant: ' \
               '200 * the number of dice'
        price = f'{str1:<68}|\n' + f'{str2:<68}|\n' + f'{str3:<68}|\n'
        return grid_en[self.name] + '\n' + head + '\n' + price + head + \
            '\n'


class Jail(Grid):
    id_: int
    name: str

    def __init__(self, id_: int) -> None:
        """Initialize a Jail with name 'Jail'
        """
        Grid.__init__(self, id_, name='Jail')

    def __str__(self) -> str:
        """Add player name in other class
        """
        return 'is arrested.  (rest for one round)'


class Chance(Grid):
    id_: int
    name: str

    def __init__(self, id_: int) -> None:
        """Initialize a Chance Grid with name 'Chance'
        """
        Grid.__init__(self, id_, name='Chance')

    def __str__(self) -> str:
        return 'Pick up a chance card.'


class Fate(Grid):
    id_: int
    name: str

    def __init__(self, id_: int) -> None:
        Grid.__init__(self, id_, name='Fate')

    def __str__(self) -> str:
        return 'Pick up a fate card.'


class Player:
    id_: int
    name: str
    gold: int
    pos: int
    own: Dict[int, Union[Grid, Tuple[Grid, int]]]
    _proceed: Union[bool, List[bool]]

    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name
        self.gold = 0
        self.pos = 0
        self.own = {}
        self._proceed = True

    def add_gold(self, num: int) -> None:
        """Add gold to the player, negative indicates reducing

        Precondition: self.gold >= 0

        """
        self.gold += num

    def update_player_position(self) -> Optional[bool]:
        """In case self.pos is out of the grid
        """
        if self.pos > 29:
            self.pos -= 30
            return True
        elif self.pos < 0:
            self.pos += 30

    def proceed(self) -> None:
        self._proceed = False

    def jail(self) -> None:
        """Arrested, return None
        """
        self._proceed = [False, False]

    def make_turn(self) -> bool:
        """If self in Jail, chance self._proceed from [False, False] to False,
        return False
        otherwise chance False back to True, return True
        """
        if isinstance(self._proceed, list):
            self._proceed = False
            input(f'{self.name} rest for one round.')
            return False
        else:
            self._proceed = True
            return True

    def count(self, category: int) -> int:
        """Return the number of airport (0) or water plant (1) owned by this
        player in this monopoly game
        """
        if category == 0:
            n = 0
            for i in self.own:
                if isinstance(self.own[i], Airport):
                    n += 1
            return n
        elif category == 1:
            n = 0
            for i in self.own:
                if isinstance(self.own[i], WaterPlant):
                    n += 1
            return n

    def bankrupt(self) -> bool:
        """IF self.gold < 0, self is bankrupted and would be out of the game
        Return True if self is bankrupted
        """
        if self.gold < 0:
            return True

        return False

    def check_gold(self) -> str:
        return f'Player{self.id_}: {self.name} has {self.gold} gold.'

    def check_property(self) -> str:
        """Return descriptions of all properties self has
        """
        s = ''
        for prop in self.own.values():
            if isinstance(prop, tuple):
                s += str(prop[0])
            elif isinstance(prop, Grid):
                s += str(prop)
        return s


def _num2str(n: int, p: Optional[Player]) -> str:
    """Change display on the game board, depending on the level of RealEstate a
    player own
    """
    if p is None:
        id_ = ''
    else:
        id_ = str(p.id_) + ':'

    if n is not None:
        if n == 0:
            return '{:^6}'.format(id_ + '_')
        elif n == 1:
            return '{:^6}'.format(id_ + 'h.')
        elif n == 2:
            return '{:^6}'.format(id_ + 'hh')
        elif n == 3:
            return '{:^6}'.format(id_ + 'H!')
        elif n == 5:
            return '{:^6}'.format(id_ + 'Got')

    return ' ' * 6


def dice() -> int:
    """Return an int between 1 and 6
    """
    return random.choice([1, 2, 3, 4, 5, 6])


class GameBoard:
    """The GameBoard of monopoly that shows players position and real estate,
    airport and water plant they own
    """
    info: Dict[int, Tuple[str, Optional[int], Optional[Player]]]
    board: Dict[int, Grid]
    players: List[Player]

    def __init__(self) -> None:
        self.info = {}
        self.players = []

    def __str__(self) -> str:
        d = self.info
        sep = '+------' * 10 + '+\n'
        mid = '|------' * 10 + '|\n'
        sep_m = '+------+' + ' ' * 55 + '+------+\n'
        mid_m = '|------|' + ' ' * 55 + '|------|\n'

        # First row
        s = ''
        stat_str = ''
        player_info = ''
        for i in range(10):
            s += f'|{d[i][0]:^6}'
            stat = _num2str(d[i][1], d[i][2])
            stat_str += '|' + stat
            # Player position
            player_str = ''
            for p in self.players:
                if p.pos == i:
                    player_str += str(p.id_)
            player_info += f'|{player_str:^6}'

        stat_str += '|\n'
        s += '|\n'
        player_info += '|\n'
        first_line_chunk = sep + s + mid + stat_str + player_info + sep

        # Middle rows
        j_line_chunk = ''
        for j in range(29, 24, -1):
            str_ = f'|{d[j][0]:^6}|'
            sm = f'{str_:<63}' + f'|{d[39 - j][0]:^6}|\n'
            stat_m1 = _num2str(d[j][1], d[j][2])
            stat_m2 = _num2str(d[39 - j][1], d[39 - j][2])
            stat_str_m = '|' + stat_m1 + '|' + ' ' * 55 + '|' + stat_m2 + '|\n'

            player_str1 = player_str2 = ''
            for p in self.players:
                if p.pos == j:
                    player_str1 += str(p.id_)
                elif p.pos == 39 - j:
                    player_str2 += str(p.id_)
            p_info_m = f'|{player_str1:^6}|' + ' ' * 55 + \
                       f'|{player_str2:^6}|\n'
            if not j == 25:
                j_line_chunk += sm + mid_m + stat_str_m + p_info_m + \
                                sep_m
            else:
                j_line_chunk += sm + mid_m + stat_str_m + p_info_m + \
                                sep

        # Last row
        sl = ''
        stat_str_l = ''
        player_info_l = ''
        for i in range(24, 14, -1):
            sl += f'|{d[i][0]:^6}'
            stat_l = _num2str(d[i][1], d[i][2])
            stat_str_l += '|' + stat_l
            # Player position
            player_str = ''
            for p in self.players:
                if p.pos == i:
                    player_str += str(p.id_)
            player_info_l += f'|{player_str:^6}'

        stat_str_l += '|\n'
        sl += '|\n'
        player_info_l += '|\n'
        last_line_chunk = sl + mid + stat_str_l + player_info_l + sep

        return first_line_chunk + j_line_chunk + last_line_chunk

    def add_player(self) -> List[Player]:
        """If initially there is / are players, change self.players back to []
        Return a list of players
        """
        if self.players:
            self.players = []
        num = input('How many players are in this game?')
        if not num.isnumeric() or num == '0':
            self.add_player()
        else:
            for i in range(1, int(num) + 1):
                p = Player(i, input('Enter your name:'))
                p.add_gold(37000)
                self.players.append(p)

        return self.players

    def get_info(self) -> None:
        """Translate self.board to self.info type"""
        for g in self.board:
            grid = self.board[g]
            self.info[g] = (grid.name, None, None)

    def owned(self, pos: int) -> Optional[Player]:
        """Return the player that own the <pos> grid,
        if no player owns it, return None
        """
        for p in self.players:
            for o in p.own:
                if pos == o:
                    return p

        return None

    def _remove_bankrupt(self) -> Optional[str]:
        """Remove and return bankrupted players
        Return None if no player is removed
        """
        s = ''
        for i in self.players:
            if i.bankrupt():
                self.players.remove(i)
                s += 'Player' + str(i.id_) + 'has bankrupted!'

        if s != '':
            return s

    def _effect_on_grid(self, g: Grid, p: Player, d: int) -> None:
        """A helper class that make change on self.info and player, depending on
        the grids players step on.
        Use input to communicate with players to make change to the game board

        Precondition: p is eligible to make a move
        """
        id_ = g.id_
        info_ = self.info
        if type(g) in [RealEstate, Airport, WaterPlant]:
            print(g)
        # RealEstate #########################################
        if isinstance(g, RealEstate):
            if self.owned(id_) and self.owned(id_) != p:
                player = self.owned(id_)
                lvl = self.info[id_][1]
                fees = g.fee[lvl]
                input(f'You will be charged {fees} gold.')
                player.add_gold(fees)
                p.add_gold(-fees)
            elif id_ not in p.own:
                if p.gold < g.price[0]:
                    print('It seems like you don\'t have enough gold to'
                          ' purchase', g.name)
                else:
                    decision = ''
                    while decision not in ('yes', 'no'):
                        decision = input(f'Do you want to purchase {g.name} '
                                         f'with {g.price[0]} golds?  '
                                         f'(enter yes or no)'
                                         ).lower()
                    if decision == 'yes':
                        p.own[id_] = (g, 0)  # Grid object
                        p.gold -= g.price[0]
                        info_[id_] = (info_[id_][0], 0, p)  # info
            # own but not at highest lvl
            elif id_ in p.own and p.own[id_][1] < 3:
                lvl = p.own[id_][1]  # lvl of the RealEstate
                if p.gold < g.price[lvl + 1]:
                    print('It seems like you don\'t have enough gold to '
                          'upgrade', g.name)
                else:
                    decision = ''
                    while decision not in ('yes', 'no'):
                        decision = input(f'Do you want to upgrade {g.name} '
                                         f'with {g.price[lvl + 1]} golds?  '
                                         f'(enter yes or no)'
                                         ).lower()
                    if decision == 'yes':
                        p.own[id_] = (g, lvl + 1)
                        info_[id_] = (info_[id_][0], info_[id_][1] + 1,
                                      info_[id_][2])  # info
                        p.gold -= g.price[lvl + 1]
            else:
                print('Your real estate is already at the maximum level!')
            p.proceed()

        # Airport ############################################
        elif isinstance(g, Airport):
            if self.owned(id_) and self.owned(id_) != p:
                player = self.owned(id_)
                n = player.count(0)
                fees = g.fee
                if n == 2:
                    fees = 2 * fees - 100
                input(f'You will be charged {fees} gold.')
                player.add_gold(fees)
                p.add_gold(-fees)
            elif p.gold < g.price:
                print('It seems like you don\'t have enough gold to '
                      'purchase', g.name)
            elif id_ not in p.own:
                decision = ''
                while decision not in ('yes', 'no'):
                    decision = input(f'Do you want to purchase {g.name} with '
                                     f'{g.price} golds?  (enter yes or no)'
                                     ).lower()
                if decision == 'yes':
                    p.own[id_] = g
                    p.gold -= g.price
                    info_[id_] = (info_[id_][0], 5, p)
            else:
                print('You already own this airport!')
            p.proceed()

        # WaterPlant #########################################
        elif isinstance(g, WaterPlant):
            if self.owned(id_) and self.owned(id_) != p:
                player = self.owned(id_)
                n = player.count(1)
                fees = 100 * d
                if n == 2:
                    fees = 200 * d
                input(f'You will be charged {fees} gold.')
                player.add_gold(fees)
                p.add_gold(-fees)
            elif p.gold < g.price:
                print('It seems like you don\'t have enough gold to '
                      'purchase', g.name)
            elif id_ not in p.own:
                decision = ''
                while decision not in ('yes', 'no'):
                    decision = input(f'Do you want to purchase {g.name} with '
                                     f'{g.price} golds?  (enter yes or no)'
                                     ).lower()
                if decision == 'yes':
                    p.own[id_] = g
                    p.gold -= g.price
                    info_[id_] = (info_[id_][0], 5, p)
            else:
                print('You already own this water plant!')
            p.proceed()

        # Jail ###############################################
        elif isinstance(g, Jail):
            print(p.name, str(g))
            p.jail()

        # Chance #############################################
        elif isinstance(g, Chance):
            input(str(g))
            i = c_list[0]
            if i == 0:
                p.add_gold(-550)
            elif i == 1:
                p.add_gold(800)
            elif i == 2:
                p.add_gold(700)
            elif i == 3:
                p.pos -= 1
            elif i == 4:
                p.add_gold(450)
            elif i == 5:
                p.add_gold(-500)
            elif i == 6:
                p.add_gold(-600)
            elif i == 7:
                p.add_gold(-700)
            elif i == 8:
                p.add_gold(750)
            elif i == 9:
                p.add_gold(600)
            elif i == 10:
                p.add_gold(-500)
            elif i == 11:
                p.add_gold(900)
            print(chances_dict[i])
            p.proceed()
            refresh_list(c_list)

        # Fate ###############################################
        elif isinstance(g, Fate):
            input(str(g))
            i = f_list[0]
            if i == 0:
                p.add_gold(650)
            elif i == 1:
                p.add_gold(-700)
            elif i == 2:
                p.add_gold(800)
            elif i == 3:
                p.add_gold(900)
            elif i == 4:
                p.add_gold(650)
            elif i == 5:
                p.pos = 0
            elif i == 6:
                p.add_gold(800)
            elif i == 7:
                p.add_gold(1000)
            elif i == 8:
                p.add_gold(-1500)
            elif i == 9:
                pass
            elif i == 10:
                p.add_gold(1000)
            elif i == 11:
                p.add_gold(-700)
            print(fates_dict[i])
            p.proceed()
            refresh_list(f_list)

    def game(self) -> None:
        """Each players make turn by order, using a bunch of helper method
        """
        print('GAME STARTS!')
        while len(self.players) > 1:
            for p in self.players:
                print(self)
                if p.make_turn():
                    d = dice()
                    print(f'Player {p.id_}: {p.name}\'s turn!')
                    input('Press return to roll a dice.')
                    input(f'The number on your dice is {d}')
                    p.pos += d
                    if p.update_player_position():
                        p.add_gold(1000)
                    g = self.board[p.pos]
                    self._effect_on_grid(g, p, d)
                    input(p.check_gold())

                if self._remove_bankrupt():
                    print(f'Player {p.id_} has bankrupted!')

                prompt = input('Do you want to check your properties?  '
                               '(enter yes to check)')
                if prompt.lower() == 'yes':
                    input(p.check_property())

            if input('End this game?  (enter end to end, enter \"enter\" '
                     'to skip)').lower() == 'end':
                print('Remember to save your game.',
                      '\n{enter data = save(), then run the program again,',
                      'and enter load(data)}')
                return None

        print(self.players[0].name, 'is the final winner!')


# Initial conditions ############
chances_dict = {0: 'Gold -550',
                1: 'You sold a tarantulas for 800 gold.',
                2: 'Gold +700',
                3: 'Go 1 step back',
                4: 'Gold +450',
                5: 'Gold -500',
                6: 'Gold -600',
                7: 'Gold -700',
                8: 'Gold +750',
                9: 'Gold +600',
                10: 'Gold -500',
                11: 'Gold +900'}
fates_dict = {0: 'Gold +600',
              1: 'Gold -700',
              2: 'Gold +800',
              3: 'Gold +900',
              4: 'Gold +650',
              5: 'Go back to the starting point',
              6: 'Gold +800',
              7: 'Gold +1000',
              8: 'You buy a PS5, gold -1500',
              9: 'You eat a tarantulas! Gold += 0',
              10: 'Gold -1000',
              11: 'Gold -700'}
c_list = _shuffle(chances_dict)
f_list = _shuffle(fates_dict)
gb = GameBoard()

g0 = Grid(0, 'START!')
g1 = RealEstate(1, 'ZhSh',
                [600, 500, 500, 500], [100, 200, 500, 900])
g2 = Fate(2)
g3 = RealEstate(3, 'Huai',
                [1000, 500, 500, 500], [100, 300, 900, 2700])
g4 = Chance(4)
g5 = Airport(5, 'PDJC', 2000, 300)
g6 = RealEstate(6, 'YanA',
                [1600, 1000, 1000, 1000], [200, 600, 1800, 5000])
g7 = Fate(7)
g8 = RealEstate(8, 'Heng',
                [2000, 1000, 1000, 1000], [200, 800, 2200, 6000])
g9 = Jail(9)
g10 = RealEstate(10, 'FuXing',
                 [2200, 1500, 1500, 1500], [180, 900, 2500, 7000])
g11 = WaterPlant(11, 'Dian', 1200)
g12 = RealEstate(12, 'PDDD',
                 [2400, 1500, 1500, 1500], [200, 1000, 3000, 7500])
g13 = Fate(13)
g14 = RealEstate(14, 'ShJi',
                 [2600, 1500, 1500, 1500], [300, 1100, 3300, 8000])
g15 = Chance(15)
g16 = RealEstate(16, 'Bin',
                 [2200, 1500, 1500, 1500], [200, 900, 2500, 7000])
g17 = RealEstate(17, 'WaiB',
                 [2400, 1500, 1500, 1500], [200, 1000, 3500, 7000])
g18 = Fate(18)
g19 = RealEstate(19, 'LuJZ',
                 [3000, 2000, 2000, 2000], [300, 1300, 3900, 9000])
g20 = Airport(20, 'HQJC', 2000, 300)
g21 = Chance(21)
g22 = WaterPlant(22, 'ZiLaiS', 1200)
g23 = RealEstate(23, 'XuJiaH',
                 [3600, 2000, 2000, 2000], [400, 1800, 5000, 11000])
g24 = Jail(24)
g25 = RealEstate(25, 'WaiTan',
                 [3200, 2000, 2000, 2000], [300, 1500, 4500, 10000])
g26 = Chance(26)
g27 = RealEstate(27, 'H-Way',
                 [2200, 1500, 1500, 1500], [200, 900, 2500, 7000])
g28 = Chance(28)
g29 = RealEstate(29, 'NanJ',
                 [1400, 1000, 1000, 1000], [100, 500, 1500, 4500])

gb.board = {0: g0, 1: g1, 2: g2, 3: g3, 4: g4, 5: g5, 6: g6, 7: g7, 8: g8,
            9: g9, 10: g10, 11: g11, 12: g12, 13: g13, 14: g14, 15: g15,
            16: g16, 17: g17, 18: g18, 19: g19, 20: g20, 21: g21, 22: g22,
            23: g23, 24: g24, 25: g25, 26: g26, 27: g27, 28: g28, 29: g29}


################################################################################


def save(g=gb) -> dict:
    """Save the game"""
    dic = {'info': g.info, 'players': g.players}
    return dic


def load(data: dict, g=gb) -> None:
    """Load the data"""
    g.info = data['info']
    g.players = data['players']
    g.game()


def new_game(g=gb) -> None:
    """Start a new game"""
    g.get_info()
    g.add_player()
    g.game()


if __name__ == '__main__':
    new_game()
