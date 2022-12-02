from csv import writer

class Plant:
    def __init__(self, name: str, growth: int, compost: int, manure: int) -> None:
        self._name = name
        self._growth = growth
        self._compost = compost
        self._manure = manure

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def growth(self) -> int:
        return self._growth
        
    @property
    def compost(self) -> int:
        return self._compost

    @property    
    def manure(self) -> int:
        return self._manure

class Combo:
    def __init__(self, plants: list[Plant]) -> None:
        # plant count
        self._plants = {}
        # keep net stats
        self._net_growth = 0
        self._net_compost = 0
        self._net_manure = 0
        
        for p in plants:
            self._net_growth += p.growth
            self._net_compost += p.compost
            self._net_manure += p.manure

            if p.name in self.plants:
                self.plants[p.name] += 1
            else:
                self.plants[p.name] = 1
        
    
    @property
    def plants(self) -> dict[str, int]:
        return self._plants

    @property
    def net_growth(self) -> int:
        return self._net_growth
        
    @property
    def net_compost(self) -> int:
        return self._net_compost
        
    @property
    def net_manure(self) -> int:
        return self._net_manure

    def no_upkeep(self) -> bool:
        return self.net_growth >= 0 and self.net_compost >= 0 and self.net_manure >= 0

TILE_MAX_PLANT = 9
ONLY_FREE_COMBOS = False

def combine(plants: list[Plant], callback, chosen: list[Plant] = [], start = 0):
    if len(chosen) == TILE_MAX_PLANT:
        return callback(Combo(chosen))
        

    for i in range(start, len(plants)):
        chosen.append(plants[i])
        combine(plants, callback, chosen, start)
        start += 1
        chosen.pop()

def calc_combinations(plants: list[Plant]) -> list[Combo]:
    combos: list[Combo] = []

    def aggregate(combo: Combo):
        if ONLY_FREE_COMBOS:
            if not combo.no_upkeep():
                return
        combos.append(combo)

    combine(plants, aggregate)
    
    
    combos.sort(key=lambda c: [
        min(c.net_growth, c.net_compost, c.net_manure),
        -len(c.plants)
        ], reverse=True)

    return combos    

def print_combos(combos: list[Combo]):
    for c in combos:
        print(f"\nNet stats => Growth: {c.net_growth}\t\tCompost: {c.net_compost}\t\tManure: {c.net_manure}")
        for p in c.plants.items():
            print(f"{p[0]} x{p[1]}")

# define crops seperated by requirements having both seperated and combined versions for similar ones
# since similar crops don't always share favourite seasons
carrot = Plant('Carrot', -4, 2, 2)
#pumpkin = Plant('Pumpkin', -4, 2, 2)
carrot_pumpkin = Plant('Carrot/Pumpkin', -4, 2, 2)

corn = Plant('Corn', 2, -4, 2)
asparagus = Plant('Asparagus', 2, -4, 2)
corn_asparagus = Plant('Corn/Asparagus', 2, -4, 2)

potato = Plant('Potato', 2, 2, -4)
#eggplant = Plant('Eggplant', 2, 2, -4)
potato_eggplant = Plant('Potato/Eggplant', 2, 2, -4)

tomato = Plant('Tomato', -2, -2, 4)

watermelon = Plant('Watermelon', 4, -2, -2)

dragonfruit = Plant('Dragonfruit', 4, 4, -8)
pepper = Plant('Pepper', 4, 4, -8)
dragonfruit_pepper = Plant('Dragonfruit/Pepper', 4, 4, -8)

#durian = Plant('Durian', 4, -8, 4)
garlic = Plant('Garlic', 4, -8, 4)
durian_garlic = Plant('Durian/Garlic', 4, -8, 4)

onion = Plant('Onion', -8, 4, 4)
#pomegranate = Plant('Pomegranate', -8, 4, 4)
onion_pomegranate = Plant('Onion/Pomegranate', -8, 4, 4)

autumn = [
    carrot_pumpkin,
    corn,
    potato_eggplant,
    tomato,
    garlic,
    onion,
    pepper
]

winter = [
    carrot_pumpkin,
    potato,
    asparagus,
    garlic
]

spring = [
    carrot,
    corn_asparagus,
    potato_eggplant,
    tomato,
    watermelon,
    dragonfruit,
    durian_garlic,
    onion_pomegranate
]

summer = [
    corn,
    tomato,
    watermelon,
    dragonfruit_pepper,
    garlic,
    onion_pomegranate
]

seasons = {'Spring': spring, 'Summer': summer, 'Autumn': autumn, 'Winter': winter}

if __name__ == '__main__':
    try:
        TILE_MAX_PLANT = int(input('How many crops do you plant on a tile (default: 9)? '))
    except:
        TILE_MAX_PLANT = 9
        
    ONLY_FREE_COMBOS = False if input('Should the output just include free combos (default: yes)? ') == 'no' else True

    for s in seasons.items():
        with open(f'{s[0]}.csv', 'w', newline='') as file:
            csv = writer(file)
            combos = calc_combinations(s[1])
            for c in combos:
                if not ONLY_FREE_COMBOS:
                    csv.writerow([c.net_growth, c.net_compost, c.net_manure])
                for p in c.plants.items():
                    csv.writerow([p[0], p[1]])
                csv.writerow([])