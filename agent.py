import random
class Agent:
    def __init__(self):
        self.wump = [['U' for i in range(50)] for j in range(50)]  # stench 냄새가 나는곳
        self.kb = [['U' for i in range(50)] for j in range(50)]  # 안전한 곳 0, breeze가 있는 곳 b
        self.move = 1  # 현재 이동 방향
        self.tb = False
        self.move_stack = []
        self.unsafe = []
        self.border = False
        self.prev = []
        self.f = False
        self.exp_t = False
        self.shoot = ""
        self.arrow_Cnt = 2
        self.pre_block = 'null'  # 이전 방향
        self.step_back = False
        self.counter = 0
        self.move_p = None
        self.back_gold = False
        self.back_gold_move = False
        self.back_list = []
        self.forward_list = []
        self.breeze_check = False
        self.i = 0
        self.actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']

    def give_senses(self, location, breeze, stench, glitter):  # breeze,stench 위치
        actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        x = location[0]
        y = location[1]
        if glitter == True:
            self.kb[x][y] = 'g'
            self.locate_gold(location)
        if stench == True:  # stench가 나는경우
            self.wump[x][y] = 's'
        if breeze == True:  # breeze가 있는 경우
            self.kb[x][y] = 'b'
            self.locate_pit(location)  # 물 웅덩이의 위치 현재위치 주변에 b가 2개 있다면 그곳은 pitch
        if breeze == False and stench == False:
            self.kb[x][y] = 'o'  # 안전한 곳 위치 저장
            self.wump[x][y] = 'o'  # 안전한 상태 저장
        if self.prev == location:  # 이전 위치가 현재 위치와  같은 경우
            self.border = True  # 화면 경계에 있음
        else:  # 이전위치랑 현재위치가 다른 경우
            self.prev = location  # 이전위치값에 현재 위치를 저장 여기서 이전 위치 저장!
            self.border = False  # 경계가 없음
        if (breeze == True):  # 물웅덩이가 있는 경우breeze
            t = self.check_pit(self.prev)
            if isinstance(t, int):
                if self.breeze_check == False:
                    action = actions[t]
                    print("Pitch의 위치:", action)
                    self.unsafe.append(action)
        if stench == True:
            if self.breeze_check == False:
                w = self.check_wump(self.prev)
                if isinstance(w, int):
                    action = actions[self.check_wump(self.prev)]
                    self.unsafe.append(action)
                c = self.Shoot()  # 에이전트의 위치에 인접해 있는 경우 Wumpus를 죽임
                if c in extras:
                    self.shoot = c  # 사격 동작
            # if self.state_back ==True and :
            #     print("활을 쏘고 move_p가 stack에 들어감:",shoot_action)
            #     self.move_stack.append(self.move_p)

            # 주변 격자를 돌면서 갈 방향을 정함

    def Turn(self):
        actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
        if self.actions[self.i] == "BUMP":
            if self.i == 3:
                self.exp_t = True
            return self.actions[self.i]
        else:
            if self.tb == False:
                self.tb = True
                self.move_p = self.actions[self.i]
                self.move_visited = self.actions[self.i]
                return self.actions[self.i]
            if self.tb == True:
                self.tb = False
                if self.i == 3:
                    self.exp_t = True
                if self.border == False:
                    self.move_p = self.toggle_move(actions[self.i])
                    return self.toggle_move(actions[self.i])
                else:
                    self.unsafe.append(actions[self.i])
                    return "BUMP"

    # 물웅덩이를 기준으로 이동할 곳을 랜덤으로 이동
    def GoForward(self):
        self.f = False
        actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
        temp = []
        t = self.check_pit(self.prev)  # 물웅덩이가 있는 방향
        g = self.Grab(self.prev)
        if isinstance(g, int):
            print(g, "에서 Grab")
            return actions[g]
        for item in actions:
            if item not in self.unsafe:  # 안전한 위치존재하면
                temp.append(item)  # 모두 temp에 넣음
        self.unsafe = []  # 안전하지 않은 위치 초기화
        if temp:  # 안전한 위치가 있다면
            # print("이동 가능한 격자",temp)
            sit = random.choice(temp)
            self.pre_block = sit
            self.unsafe.append(self.toggle_move(sit))  # 이동할 격자의 반대 격자를 넣어서 이전 위치로 되돌아가 가지 않게 함
            return sit  # 랜덤값 으로 이동
        else:
            print("이동할수 있는 위치가 없습니다.")
            print("왔던 길로 돌아갑니다.")
            return self.toggle_move(self.pre_block)

    def toggle_move(self, move):
        actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
        if move == actions[0]:
            return actions[1]
        elif move == actions[1]:
            return actions[0]
        elif move == actions[2]:
            return actions[3]
        else:
            return actions[2]

    # 에이전트가 이동하는 방식
    def get_action(self):
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        self.counter += 1
        if self.counter > 9999:
            return "QUIT"

        g = self.Grab(self.prev)
        if isinstance(g, int) and self.back_gold == False:
            print("Grab!")  # 금의 위치를 확신 한 경우
            return actions[g]
        if self.back_gold == True:  # 백트레킹
            return self.Climb()
        else:
            if self.shoot in extras and self.arrow_Cnt > 0:  # 화살 화살을 쏠때는 이전 값을 저장하고 화살을 쏜다.
                self.step_back = True
                self.arrow_Cnt = self.arrow_Cnt - 1
                return self.shoot

            if self.step_back == True:  # 화살을 쏠때 저장한 이전값이 있는경우 이전값을 전송한다. 따라서 움직이지 않음.
                self.step_back = False
                if self.shoot == extras[0]:
                    shoot_action = actions[0]
                elif self.shoot == extras[1]:
                    shoot_action = actions[1]
                elif self.shoot == extras[2]:
                    shoot_action = actions[2]
                else:
                    shoot_action = actions[3]
                self.i = 0
                self.tb = False
                self.unsafe = []
                self.actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
                return "WUMPUS_DIE"

            if self.f == False:  # 4방향으로 이동
                if self.exp_t == True:  # 4방향 한번 다 돈 경우
                    self.i = 0
                    self.exp_t = False
                    self.f = True  # 아래 if로 넘어감

                else:
                    self.breeze_check = True
                    if self.unsafe:
                        for move in self.unsafe:
                            self.actions = ["BUMP" if x == move else x for x in self.actions]
                    action = self.Turn()
                    if self.tb == False:
                        self.i += 1
                    return action

            if self.f == True:
                t = self.GoForward()
                self.f = False
                self.move_stack.append(t)
                self.breeze_check = False
                self.actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
                return t

    def Shoot(self):
        c = (0, 0)
        v = (0, 0)
        x = 0
        y = 0
        l = []
        l = self.prev  # 이전 위치 값

        for i, lst in enumerate(self.wump):  # 인덱스 와 값
            for j, k in enumerate(lst):  # 인덱스 와 값
                if k == "s":  # 악취가 있는 경우
                    c = (i, j)  # c에 할당
        if c:  # 악취가 있는 경우
            x, y = c
            # 괴물의 위치 저장
            if self.wump[x + 2][y] == 's':
                self.wump[x + 1][y] = 'w'  # wumpus의 정확한 위치를 결정하기 위해 다른 이웃 위치를 확인
            if self.wump[x - 2][y] == 's':
                self.wump[x - 1][y] = 'w'
            if self.wump[x + 1][y + 1] == 's':
                self.wump[x + 1][y] = 'w'
            if self.wump[x + 1][y - 1] == 's':
                self.wump[x + 1][y] = 'w'
            if self.wump[x - 1][y + 1] == 's':
                self.wump[x][y + 1] = 'w'
            if self.wump[x - 1][y - 1] == 's':
                self.wump[x][y - 1] = 'w'

        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        for i, lst in enumerate(self.wump):
            for j, k in enumerate(lst):
                if k == "w":  # 괴물이 있는 경우
                    v = (i, j)  # wumpus의 존재위치 할당
                    self.wump[i][j] = 'U'

        if l[0] == v[0]:  # x 좌표
            if l[1] > v[1]:
                return (extras[1])  # 아래에 활
            else:
                return (extras[0])  # 위에 활

        if l[1] == v[1]:  # y 좌표
            if l[0] > v[0]:
                return (extras[2])
            else:
                return (extras[3])

    # 물웅덩이의 위치
    def locate_pit(self, location):
        x = location[0]
        y = location[1]
        if self.kb[x + 2][y] == 'b' and self.kb[x + 1][y + 1] == 'b':
            self.kb[x + 1][y] = 'p'
        if self.kb[x + 2][y] == 'b' and self.kb[x + 1][y - 1] == 'b':
            self.kb[x + 1][y] = 'p'
        if self.kb[x - 2][y] == 'b' and self.kb[x - 1][y + 1] == 'b':
            self.kb[x - 1][y] = 'p'
        if self.kb[x - 2][y] == 'b' and self.kb[x - 1][y - 1] == 'b':
            self.kb[x + 1][y] = 'p'
        if self.kb[x][y + 2] == 'b' and self.kb[x + 1][y + 1] == 'b':
            self.kb[x][y + 1] = 'p'
        if self.kb[x][y + 2] == 'b' and self.kb[x - 1][y + 1] == 'b':
            self.kb[x][y + 1] = 'p'
        if self.kb[x][y - 2] == 'b' and self.kb[x + 1][y - 1] == 'b':
            self.kb[x][y - 1] = 'p'
        if self.kb[x][y - 2] == 'b' and self.kb[x - 1][y - 1] == 'b':
            self.kb[x][y - 1] = 'p'

    def check_pit(self, l):  # l은 이전 위치
        x = l[0]
        y = l[1]
        if self.kb[x + 1][y] == 'p':
            return 0
        if self.kb[x - 1][y] == 'p':
            return 1
        if self.kb[x][y + 1] == 'p':
            return 2
        if self.kb[x][y - 1] == 'p':
            return 3
        # 0:위 1:아래 2:왼쪽 3:오른쪽

    def check_wump(self, l):
        x = l[0]
        y = l[1]
        if self.wump[x + 1][y] == 'w':
            return 0
        if self.wump[x - 1][y] == 'w':
            return 1
        if self.wump[x][y + 1] == 'w':
            return 2
        if self.wump[x][y - 1] == 'w':
            return 3

    # 금의 위치
    def locate_gold(self, location):
        x = location[0]
        y = location[1]
        if self.kb[x + 2][y] == 'g' and self.kb[x + 1][y + 1] == 'g':
            self.kb[x + 1][y] = 'G'
        if self.kb[x + 2][y] == 'g' and self.kb[x + 1][y - 1] == 'g':
            self.kb[x + 1][y] = 'G'
        if self.kb[x - 2][y] == 'g' and self.kb[x - 1][y + 1] == 'g':
            self.kb[x - 1][y] = 'G'
        if self.kb[x - 2][y] == 'g' and self.kb[x - 1][y - 1] == 'g':
            self.kb[x + 1][y] = 'G'
        if self.kb[x][y + 2] == 'g' and self.kb[x + 1][y + 1] == 'g':
            self.kb[x][y + 1] = 'G'
        if self.kb[x][y + 2] == 'g' and self.kb[x - 1][y + 1] == 'g':
            self.kb[x][y + 1] = 'G'
        if self.kb[x][y - 2] == 'g' and self.kb[x + 1][y - 1] == 'g':
            self.kb[x][y - 1] = 'G'
        if self.kb[x][y - 2] == 'g' and self.kb[x - 1][y - 1] == 'g':
            self.kb[x][y - 1] = 'G'

    def Grab(self, l):
        x = l[0]
        y = l[1]
        if self.kb[x + 1][y] == 'G':
            return 0
        if self.kb[x - 1][y] == 'G':
            return 1
        if self.kb[x][y + 1] == 'G':
            return 2
        if self.kb[x][y - 1] == 'G':
            return 3

    def Climb(self):
        actions = ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']
        if self.move_stack:
            next_move = self.move_stack.pop()
        self.back_list.append(next_move)
        if next_move == actions[0]:
            return actions[1]
        elif next_move == actions[1]:
            return actions[0]
        elif next_move == actions[2]:
            return actions[3]
        elif next_move == actions[3]:
            return actions[2]

    # 상태 확인용
    def state_back(self):
        self.back_gold = True
        return self.back_gold
