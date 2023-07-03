# 2023_wumpusWorld_11team
2023-1 인공지능 wumpus world 프로젝트 11팀

# Wumpus World 도메인에 대한 분석
1. Percept
2. Reasoning
3. Action
# Percept
Wumpus World에서는 에이전트의 센서를 통한 입력은 다음과 같다.

[Stench, Breeze, Glitter, Bump, Scream]

stench: wumpus가 있는 격자와 인접한 격자에는 고약한 냄새가 난다.

breeze: pitch가 있는 격자와 인접한 격자에는 바람이 분다.

glitter: 금이 있는 격자에는 빛이 난다.

bump: 제한된 크기의 벽에 부딪혔을 때 인식된다.

scream: wumpus 괴물이 에이전트가 쏜 화살에 의하여 제거되면 비명이 들린다.

# Reasoning
Wumpus World에서는 K.B.에 저장되어있는 지식을 이용해 다음과 같은 추론을 할 수 있다.

K.B.(Knowledge Base):

1. (1,1)은 wumpus와 pitch가 존재하지 않는다.
2. 격자의 크기는 4x4이다.
3. 한격자에는 wumpus와 pitch 중에 하나만 존재 할 수 있다.
4. 에이전트가 wumpus나 pitch를 만나면 죽는다.
5. 사망 시 화살 2개로 초기화된다.
6. 죽기까지의 과정은 셀에 저장된다.
7. Climb이 발생하면 성공적으로 종료된다.
Reasoning:
1. M.P.(Modus Ponens)와 A.E.(And - Elimination)의 추론규칙에 따르면, 현 격자에
stench가 없을 때 인접한 격자에는 wumpus가 존재하지 않는다.
2. M.P.(Modus Ponens)의 추론규칙에 따르면, 현 격자에 stench가 있다면 인접한 격자
중 하나에 wumpus가 존재하는것을 알 수 있다.
3. U.R.(Unit Resolution) 추론규칙과 위의 경우에 따르면, 현 격자는 wumpus가 없는 격
자임을 알 수 있다.
4. M.P.(Modus Ponens)의 추론규칙에 따르면, 현 격자에 breeze가 있다면 인접한 격자
중 하나에 pitch가 존재하는것을 알 수 있다.
5. M.P.(Modus Ponens)와 A.E.(And - Elimination)의 추론규칙에 따르면, 현 격자에
breeze가 없을 때 인접한 격자에는 pitch가 존재하지 않는다.
6. U.R.(Unit Resolution) 추론규칙과 위의 경우에 따르면, 현 격자는 pitch가 없는 격자임
을 알 수 있다.
7. 3번과 6번에 따르면 안전한 격자임을 알 수 있으므로 에이전트가 이동할 수 있다.
8. 벽을 만났을 경우, 벽이 없는 방향으로 회전한다.
9. scream이 발생하면 에어전트가 향한 격자에는 wumpus가 존재하지 않음을 알 수 있
다.
10. 빛이 나면 grab한다.
# Action
에이전트가 수행할 수 있는 Action은 다음과 같다.

GoForward: 에이전트가 한 격자를 이동한다.

TurnLeft: 현재 격자에서 왼쪽으로 90도 방향 전환한다.

TurnRight: 현재 격자에서 오른쪽으로 90도 방향 전환한다.

Grab: 금(gold)을 잡는다.

Shoot: 현재 에이전트의 방향으로 화살을 쏜다.

Climb: 에이전트가 금을 획득하여 (1,1) 격자로 되돌아 오면, 동굴을 빠져나간다.

