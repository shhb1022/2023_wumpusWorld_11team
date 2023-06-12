import random
import game
import agent

width = 5

blocks = set()

for x in range(width + 1):
    blocks.add((0, x))
    blocks.add((x, 0))
    blocks.add((width, x))
    blocks.add((x, width))

gold = set()
wumpus_location = set()
pits = set()
initial_location = (1, 1)

# gold 배치
while len(gold) == 0:
    x = random.randint(1, width)
    y = random.randint(1, width)
    if (x, y) not in blocks and (x, y) != initial_location and (x, y) not in gold and (x, y) not in wumpus_location and (x, y) not in pits:
        gold.add((x, y))

# wumpus와 pits 배치
for x in range(1, width + 1):
    for y in range(1, width + 1):
        if (x, y) not in blocks and (x, y) != initial_location and (x, y) not in gold:
            if random.random() < 0.1:
                if random.random() > 0.5:
                    wumpus_location.add((x, y))
                else:
                    pits.add((x, y))

        # 하나 이상의 wumpus, pits 있는지 확인
        while len(wumpus_location) == 0:
            x = random.randint(1, width)
            y = random.randint(1, width)
            if (x, y) not in gold and (x, y) not in blocks and (x, y) != initial_location and (
            x, y) not in wumpus_location and (x, y) not in pits:
                wumpus_location.add((x, y))
        while len(pits) == 0:
            x = random.randint(1, width)
            y = random.randint(1, width)
            if (x, y) not in gold and (x, y) not in blocks and (x, y) != initial_location and (
            x, y) not in wumpus_location and (x, y) not in pits:
                pits.add((x, y))

        # wumpus와 pits가 동일한 격자 내 존재하지 않는지 확인
        while wumpus_location & pits:
            wumpus_location.remove(random.choice(list(wumpus_location & pits)))

        # wumpus와 pits가 gold와 같은 격자 내 존재하지 않는지 확인
        while wumpus_location & gold or pits & gold:
            wumpus_location.remove(random.choice(list(wumpus_location & gold | pits & gold)))
world = game.WumpusWorld(blocks=blocks, gold=gold, wumpus=wumpus_location, pits=pits, initial_location=initial_location)

print(world.play(agent.Agent()))