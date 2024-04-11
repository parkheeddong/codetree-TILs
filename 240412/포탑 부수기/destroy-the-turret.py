def make_alive_walls(walls, n, m) :
    alive_walls = set()
    for i in range(n) :
        for j in range(m) :
            if walls[i][j] != 0 :
                alive_walls.add((i, j))
    return alive_walls

def dfs(x, y, routes, visited) :
    global min_route_cnt, min_routes

    # 이미 최단 경로가 아닌 경우 - 백트래킹
    if len(routes) >= min_route_cnt :
        return

    # 정답 체크
    if x == end_x and y == end_y :
        min_route_cnt = len(routes)
        min_routes = routes

    visited[x][y] = True

    # 우
    if y+1 > m-1 and walls[x][0] > 0 and visited[x][0] == False:
        dfs(x, 0, routes + [(x, 0)], visited)
        visited[x][0] = False

    elif y+1 <= m-1 and walls[x][y+1] > 0 and visited[x][y+1] == False:
        dfs(x, y+1, routes + [(x, y+1)], visited)
        visited[x][y+1] = False

    # 하
    if x+1 > n-1 and walls[0][y] > 0 and visited[0][y] == False:
        dfs(0, y, routes + [(0, y)], visited)
        visited[0][y] = False

    elif x+1 <= n-1 and walls[x+1][y] > 0 and visited[x+1][y] == False:
        dfs(x+1, y, routes + [(x+1, y)], visited)
        visited[x+1][y] = False

    # 좌
    if y-1 < 0 and walls[x][m-1] > 0 and visited[x][m-1] == False:
        dfs(x, m-1, routes + [(x, m-1)], visited)
        visited[x][m-1] = False
    elif y-1 >= 0 and walls[x][y-1] > 0 and visited[x][y-1] == False:
        dfs(x, y-1, routes + [(x, y-1)], visited)
        visited[x][y-1] = False
    # 상
    if x-1 < 0 and walls[n-1][y] > 0 and visited[n-1][y] == False:
        dfs(n-1, y, routes + [(n-1, y)], visited)
        visited[n-1][y] = False

    elif x-1 >= 0 and walls[x-1][y] > 0 and visited[x-1][y] == False:
        dfs(x-1, y, routes + [(x-1, y)], visited)
        visited[x-1][y] = False

def attack_surrounds(start_x, start_y, end_x, end_y, walls, half_attack, n, m, alive_walls) :
    global min_routes
    min_routes.append((start_x, start_y))
    min_routes.append((end_x, end_y))
    x_idx, y_idx = end_x - 1, end_y - 1
    # 대각선 왼쪽 위
    if x_idx < 0:
        x_idx = n - 1
    if y_idx < 0:
        y_idx = m - 1
    if (start_x, start_y) != (x_idx, y_idx) :
        if walls[x_idx][y_idx] > 0:
            walls[x_idx][y_idx] -= half_attack
            min_routes.append((x_idx, y_idx))
            if walls[x_idx][y_idx] <= 0:
                alive_walls.remove((x_idx, y_idx))

    # 상
    x_idx = end_x - 1
    if x_idx < 0:
        x_idx = n - 1
    if (start_x, start_y) != (x_idx, end_y) :
        if walls[x_idx][end_y] > 0:
            walls[x_idx][end_y] -= half_attack
            min_routes.append((x_idx, end_y))
            if walls[x_idx][end_y] <= 0:
                alive_walls.remove((x_idx, end_y))

    # 대각선 오른쪽 위
    x_idx, y_idx = end_x - 1, end_y + 1
    if x_idx < 0:
        x_idx = n - 1
    if y_idx > m - 1:
        y_idx = 0
    if (start_x, start_y) != (x_idx, y_idx) :
        if walls[x_idx][y_idx] > 0:
            walls[x_idx][y_idx] -= half_attack
            min_routes.append((x_idx, y_idx))
            if walls[x_idx][y_idx] <= 0:
                alive_walls.remove((x_idx, y_idx))

    # 왼쪽
    y_idx = end_y - 1
    if y_idx < 0:
        y_idx = m - 1
    if (start_x, start_y) != (end_x, y_idx) :
        if walls[end_x][y_idx] > 0:
            walls[end_x][y_idx] -= half_attack
            min_routes.append((end_x, y_idx))
            if walls[end_x][y_idx] <= 0:
                alive_walls.remove((end_x,y_idx))

    # 오른쪽
    y_idx = end_y + 1
    if y_idx > m - 1:
        y_idx = 0
    if (start_x, start_y) != (end_x, y_idx) :
        if walls[end_x][y_idx] > 0:
            walls[end_x][y_idx] -= half_attack
            min_routes.append((end_x, y_idx))
            if walls[end_x][y_idx] <= 0:
                alive_walls.remove((end_x,y_idx))

    # 대각선 왼쪽 아래
    x_idx, y_idx = end_x + 1, end_y - 1
    if x_idx > n - 1:
        x_idx = 0
    if y_idx < 0:
        y_idx = m - 1
    if (start_x, start_y) != (x_idx, y_idx) :
        if walls[x_idx][y_idx] > 0:
            walls[x_idx][y_idx] -= half_attack
            min_routes.append((x_idx, y_idx))
            if walls[x_idx][y_idx] <= 0:
                alive_walls.remove((x_idx, y_idx))

    # 아래
    x_idx = end_x + 1
    if x_idx > n - 1:
        x_idx = 0
    if (start_x, start_y) != (x_idx, end_y) :
        if walls[x_idx][end_y] > 0:
            walls[x_idx][end_y] -= half_attack
            min_routes.append((x_idx, end_y))
            if walls[x_idx][end_y] <= 0:
                alive_walls.remove((x_idx, end_y))

    # 대각선 오른쪽 아래
    x_idx, y_idx = end_x + 1, end_y + 1
    if x_idx > n - 1:
        x_idx = 0
    if y_idx > m - 1:
        y_idx = 0
    if (start_x, start_y) != (x_idx, y_idx) :
        if walls[x_idx][y_idx] > 0:
            walls[x_idx][y_idx] -= half_attack
            min_routes.append((x_idx, y_idx))
            if walls[x_idx][y_idx] <= 0:
                alive_walls.remove((x_idx, y_idx))


import heapq
n, m, k = map(int, input().split()) # n = 행, m = 열, k = 반복 회수
handicap = n+m
walls = [list(map(int, input().split())) for _ in range(n)]
turns = [[0]*m for _ in range(n)] # 공격 턴 리스트 (디폴트 = 0)
alive_walls = make_alive_walls(walls, n, m) # 0이 아닌 포탑 집합

for turn in range(1, k+1) :  # k번 반복

    # 1. 공격 대상 선정
    attacker, attacked = [], []
    for x, y in alive_walls :
        heapq.heappush(attacker, (walls[x][y], (-1)*turns[x][y], (-1)*(x+y), (-1)*y, (-1)*x))
        heapq.heappush(attacked, ((-1)*walls[x][y], turns[x][y], x+y, y, x))

    start = heapq.heappop(attacker)
    end = heapq.heappop(attacked)
    start_x, start_y = -start[-1], -start[-2]
    end_x, end_y = end[-1],end[-2]

    # 2. 공격자의 공격력 증가 및 공력 순서 업데이트
    walls[start_x][start_y] += handicap
    turns[start_x][start_y] = turn
    # 3. 레이저 공격
    visited = [[False]*m for _ in range(n)]
    min_route_cnt = n * m + 1
    min_routes = []
    dfs(start_x, start_y, [(start_x, start_y)], visited)
    if min_routes != [] : # 레이저 공격이 가능한 경우, 피해 업데이트 및 살아남은 포탑 업데이트
        walls[end_x][end_y] -= walls[start_x][start_y]
        half_attack = walls[start_x][start_y] // 2
        if walls[end_x][end_y] <= 0 :
            alive_walls.remove((end_x, end_y))
        if len(min_routes) >= 2 :
            for x, y in min_routes[1:-1] :
                walls[x][y] -= half_attack
                if walls[x][y] <= 0 :
                    alive_walls.remove((x,y))

    else : # 4. 레이저 공격이 불가능한 경우 포탄 공격
        walls[end_x][end_y] -= walls[start_x][start_y]
        half_attack = walls[start_x][start_y] // 2
        if walls[end_x][end_y] <= 0 :
            alive_walls.remove((end_x, end_y))
        attack_surrounds(start_x, start_y, end_x, end_y, walls, half_attack, n, m, alive_walls)

    # 4. 포탑 정비 - 무관한 포탑의 공격력 +1
    for x, y in alive_walls - set(min_routes) :
        walls[x][y] += 1
        
    if len(alive_walls) == 1 :
        break

# 가장 강한 포탑의 공격력 출력
max_attack = 0
for x, y in alive_walls :
    if walls[x][y] > max_attack :
        max_attack = walls[x][y]
print(max_attack)