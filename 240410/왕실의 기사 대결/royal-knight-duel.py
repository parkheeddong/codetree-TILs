def check_dead(health, i) :
    if health[i] == 0 :
        return True
    else :
        return False


def check_wall(x, y, chess) :
    l = len(chess)
    if x < 0 or y < 0 or x > l-1 or y > l-1 or chess[x][y] == 2 :
        return True # 벽이 있음
    else :
        return False # 벽이 없음

def simulation(location, dx, dy, idx, chess, dead) :
    moved = set()
    moved_idx = set()
    new_location = dict()
    new_location[idx] = set()
    for x, y in location[idx] :
        new_location[idx].add((x+dx, y+dy))
        moved.add((x+dx, y+dy))
        if check_wall(x+dx, y+dy, chess) :
            return (False, dict(), set())
    moved_idx.add(idx)

    while moved :
        new_moved = set()
        for i in location.keys()-moved_idx-dead :
            if moved & location[i] : # 교집합이 있는 경우 (겹치는 경우)

                new_location[i] = set()
                moved_idx.add(i)
                for x, y in location[i] :
                    new_location[i].add((x+dx, y+dy))
                    new_moved.add((x+dx, y+dy))
                    if check_wall(x + dx, y + dy, chess):
                        return (False, dict(), set())

        moved = new_moved


    for i in location.keys()-moved_idx-dead :
        new_location[i] = location[i]

    return (True, new_location, moved_idx)

def check_damage(new_location, chess, idx, damage, health, dead, moved_idx) :
    for i in moved_idx :
        if i == idx :
            continue
        for x, y in new_location[i] :
            if chess[x][y] == 1 :
                damage[i] += 1
                health[i] -= 1
        if health[i] <= 0 :
            dead.add(i)
    return damage, health, dead



l, n, q = map(int, input().split()) # l = 체스판 크기, n = 기사 수, q = 명령 수
chess = [list(map(int, input().split())) for _ in range(l)] # 함정, 벽

health = [] # 체력
damage = [0] * n
dead = set()
location = dict()
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(n) :
    x, y, h, w, k = map(int, input().split())
    x, y = x-1, y-1
    health.append(k)
    location[i] = set([(i, j) for i in range(x, x+h) for j in range(y, y+w)])

for _ in range(q) :
    i, d = map(int, input().split())
    i -= 1

    # 0. 체력 0 인 기사인지 체크 - 0이면 continue
    if i in dead:
        continue

    # 1. 기사 이동 시뮬레이션
    # 1-1. 벽 있는지 체크 -> 있으면 이동
    # 1-2. 벽 없으면 이동x
    no_wall, new_location, moved_idx = simulation(location, dx[d], dy[d], i, chess, dead)
    if no_wall == False:
        # print(i)
        continue

    # 2. 없으면 새 위치의 함정 체크 -> 데미지 계산 (i번째는 계산 x)
    # 3. 기사별 체력 업데이트, 데미지 업데이트 (i번째는 업데이트 x)
    damage, health, dead = check_damage(new_location, chess, i, damage, health, dead, moved_idx)
    location = new_location

answer = 0
for i in location.keys() - dead :
    answer += damage[i]
print(answer)