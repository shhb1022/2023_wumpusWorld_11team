class WumpusWorld:
    def __init__(self, blocks, pits, gold, wumpus, initial_location):
        self.initial_location = initial_location  # copy the input
        self.wumpus = wumpus
        self.pits = pits
        self.gold = gold
        self.blocks = blocks
        self.player = self.initial_location
        self.arrow_cnt = 2
        self.round = 0

        self.breeze = {}  # breeze 위치 저장할 배열
        self.stench = {}  # stench 위치 저장할 배열
        self.glitter = {}  # glitter 위치 저장할 배열

        for p in self.pits:  # pit 인접,해당 격자에 breeze true 저장
            for l in self.neighbours(p):
                self.breeze[l] = True
        for w in self.wumpus:  # wumpus 인접,해당 격자에 stench true 저장
            for l in self.neighbours(w):
                self.stench[l] = True
        for gold in self.gold:  # 금이 있는 격자만 glitter true 저장
            self.glitter[gold] = True

    def neighbours(self, loc):  # 해당 격자와 상하좌우 격자 위치 반환하는 함수
        return [(loc[0] + 1, loc[1]), (loc[0] - 1, loc[1]), (loc[0], loc[1] + 1), (loc[0], loc[1] - 1),
                (loc[0], loc[1])]

    def scream(self, location, dx, dy):
        x, y = location
        while True:
            # 멀리 떨어져서 화살을 쏜 경우도 wumpus가 죽어야 하기때문에 벽을 만나기 전까지 dx, dy를 더하는 것을 반복
            x += dx
            y += dy
            new_location = (x, y)
            if new_location in self.blocks:
                break
            # wumpus가 화살에 맞은 경우
            if new_location in self.wumpus:
                # 죽인 웜퍼스 리스트 제거
                self.wumpus.discard(new_location)
                # stench 배열 초기화 후, 다시 채우기
                self.stench = {}
                for w in self.wumpus:
                    for l in self.neighbours(w):
                        self.stench[l] = True
                return True
        return False

    # world 상태 출력
    # --------------------
    # agent의 위치
    # ######
    # #    #
    # # P  #
    # # Y  P#
    # #  W #
    # ######
    # 남은 화살 개수
    # 현재 격자의 breeze 여부
    # 현재 격자의 stench 여부
    # 현재 격자의 glitter 여부
    # gold grab 여부
    # 다음에 수행할 action -이 부분은 sim 함수에서 출력
    # ---------------------
    def print(self):
        print(self.player)
        xmin = min([x for x, y in self.blocks])
        xmax = max([x for x, y in self.blocks])
        ymin = min([y for x, y in self.blocks])
        ymax = max([y for x, y in self.blocks])
        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):
                if (x, ymax - y) in self.blocks:
                    print('#', end='')
                elif (x, ymax - y) in self.wumpus:
                    print('W', end='')
                elif (x, ymax - y) in self.pits:
                    print('P', end='')
                elif (x, ymax - y) in self.gold:
                    print('G', end='')
                elif self.player == (x, ymax - y):
                    print('Y', end='')
                else:
                    print(' ', end='')
            print("")
        b = self.player in self.breeze
        s = self.player in self.stench
        g = self.player in self.glitter
        print("arrowCnt: " + str(self.arrow_cnt),end="   ")
        print("breeze: " + str(b),end="   ")
        print("stench: " + str(s),end="   ")
        print("glitter: " + str(g))

    def play(self, agent):
        t = 0
        self.arrow_cnt = 2
        self.player = self.initial_location
        back_state = False

        while t < 10000:
            t += 1
            # print 함수 호출
            self.print()

            b = self.player in self.breeze  # 에이전트가 breezy의 위치인가? true/false
            s = self.player in self.stench  # 에이전트가 stench의 위치인가? true/false
            g = self.player in self.glitter

            # percept 정보 agent에게 전달
            agent.give_senses(self.player, b, s, g)
            action = agent.get_action()
            agent.shoot = ""

            # give_senses를 바탕으로 agent가 결정한 다음 행동 출력
            print(action, end='\n\n')

            new_location = self.player

            # action에 따라 agent의 위치 변경
            if action == 'MOVE_UP':
                new_location = (self.player[0], self.player[1] + 1)
            elif action == 'MOVE_DOWN':
                new_location = (self.player[0], self.player[1] - 1)
            elif action == 'MOVE_LEFT':
                new_location = (self.player[0] - 1, self.player[1])
            elif action == 'MOVE_RIGHT':
                new_location = (self.player[0] + 1, self.player[1])

            # shoot action을 취한 경우
            elif action == 'SHOOT_UP':
                if self.scream(self.player, 0, 1):
                    agent.Shoot()
            elif action == 'SHOOT_DOWN':
                if self.scream(self.player, 0, -1):
                    agent.Shoot()
            elif action == 'SHOOT_LEFT':
                if self.scream(self.player, -1, 0):
                    agent.Shoot()
            elif action == 'SHOOT_RIGHT':
                if self.scream(self.player, 1, 0):
                    agent.Shoot()
            # elif action == 'WUMPUS_DIE':
            #     agent.arrow_State = True
            elif action == 'QUIT':
                return 'QUIT'

            # 화살을 쏜 경우, 화살 개수 감소시킴
            if action[0:5] == 'SHOOT':
                self.arrow_cnt = self.arrow_cnt - 1

            # if agent.kb[new_location[0]][new_location[1]] == 'P':
            #     print("pit가 확실한 격자이므로 건너뜀 !!!!!!")
            #     continue
            # if agent.wump[new_location[0]][new_location[1]] == 'W':
            #     print("wumpus가 확실한 격자이므로 건너뜀 !!!!!!")
            #     continue
            # agent의 위치가 pit라면, 죽음(이동 경로 비움, restart 출력, 화살 개수 초기화, 몇번 죽었는지 확인하기 위해 라운드 cnt 증가, 현 격자 pit로 저장, 초기위치로 이동, while문 cnt인 t=0으로 초기화)
            if new_location in self.pits:
                agent.move_stack = []
                print('fell. restart')
                self.arrow_cnt = 2
                agent.arrow_Cnt = 2
                self.round += 1
                agent.kb[new_location[0]][new_location[1]] = 'p'
                self.player = self.initial_location
                new_location = self.player
                agent.i = 0
                agent.unsafe = []
                agent.tb = False
                agent.actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
                agent.breeze_check = False
                t = 0
            # agent의 위치가 wumpus라면, 죽음(위와 동일)
            if new_location in self.wumpus:
                agent.move_stack = []
                print('eaten. restart')
                self.arrow_cnt = 2
                agent.arrow_Cnt = 2
                self.round += 1
                agent.wump[new_location[0]][new_location[1]] = 'w'
                self.player = self.initial_location
                new_location = self.player
                agent.i = 0
                agent.unsafe = []
                agent.tb = False
                agent.actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
                agent.breeze_check = False
                t = 0
            # agent 위치가 gold 라면, 백트래킹으로 (1,1)로 돌아감
            if new_location in self.gold:
                print("Gold!")
                back_state = agent.state_back()
                back_state = True
                agent.move_stack.append(action)  # 금을 잡으러 이동한 마지막 방향 저장
                # print("Gold를 찾으러 간 이동방향: ",agent.move_stack)
                self.gold = {}

            if new_location not in self.blocks:
                self.player = new_location

            # agent의 위치가 (1,1)이면서, gold를 grab한 상태인 경우 (back_state == true) => 현재 라운드 출력하고 게임 성공적으로 종료
            if new_location == (1, 1) and back_state == True:
                print('라운드: ' + str(self.round))
                return 'Climb Complete!!'