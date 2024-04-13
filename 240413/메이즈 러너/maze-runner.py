def check_wall(x, y) :
    # print(miro)
    if 0 <= x <= n-1 and 0 <= y <= n-1 and miro[x][y] == 0 :
        return True
    else :
        return False

def make_nemo(min_idx, min_dist) :
    # min_idx = 거리가 최소값인 인덱스 리스트 [0, 1, 2]
    # min_dist = 거리값 (2)
    square_list = []
    for idx in min_idx:
        x, y = people[idx]
        if exit_y == y :
            small_x, big_x = min(x, exit_x), max(x, exit_x)
            if (y - min_dist) >= 0 :
                square = [(small_x, y-min_dist), (small_x, y), (big_x, y-min_dist), (big_x, y)]
            else :
                diff = y
                square = [(small_x, y-diff), (small_x, y+min_dist-diff), (big_x, y-diff), (big_x, y+min_dist-diff)]
        elif exit_x == x :
            small_y, big_y = min(y, exit_y), max(y, exit_y)
            if (x - min_dist) >= 0 :
                square= [(x-min_dist, small_y), (x-min_dist, big_y), (x, small_y), (x, big_y)]
            else :
                diff = x
                square = [(x-diff, small_y), (x-diff, big_y), (x+min_dist-diff, small_y), (x+min_dist-diff, big_y)]
        else :
            small_x, big_x = min(x, exit_x), max(x, exit_x)
            small_y, big_y = min(y, exit_y), max(y, exit_y)
            square = [(small_x, small_y), (small_x, big_y), (big_x, small_y), (big_x, big_y)]
        square_list.append(square)

    square_list.sort(key = lambda x:(x[0][0], x[0][1]))
    return square_list[0]

def update(x, y, small_x, small_y, min_dist) :
    dx, dy = x-small_x, y-small_y # 상대적인 값
    return [dy+small_x, min_dist-dx+small_y]

from sys import stdin
n, m, k = map(int, stdin.readline().split())
# n = 미로 크기, m = 참가자 수, k = 게임 시간

miro = [list(map(int, stdin.readline().split())) for _ in range(n)]
people = [list(map(int, stdin.readline().split())) for _ in range(m)]
exit_x, exit_y = map(int, stdin.readline().split())
exit_x, exit_y = exit_x-1, exit_y-1

moving_count = 0

# 초기 세팅 ) 참가자와 Exit 거리 계산
dist = [0] * m
for idx, [x,y] in enumerate(people) :
    people[idx] = [x-1, y-1]
    dist[idx] = abs(exit_x - (x-1)) + abs(exit_y - (y-1))

for second in range(1, k+1) :

    # 1. 참가자의 이동
    delete_list = []
    for idx, [x,y] in enumerate(people) :
        nx, ny = x, y
        if x == exit_x :
            if y < exit_y and check_wall(nx, ny+1):
                ny += 1
            elif y > exit_y and check_wall(nx, ny-1) :
                ny -= 1
        elif x < exit_x :
            if check_wall(nx+1, ny) :
                nx += 1
            elif y < exit_y and check_wall(nx, ny + 1):
                ny += 1
            elif y > exit_y and check_wall(nx, ny - 1):
                ny -= 1
        elif x > exit_x :
            if check_wall(nx-1, ny) :
                nx -= 1
            elif y < exit_y and check_wall(nx, ny + 1):
                ny += 1
            elif y > exit_y and check_wall(nx, ny - 1):
                ny -= 1

        # 이동한 경우, count 업데이트
        if (x, y) != (nx, ny) :
            # print(f'{x},{y}에서{nx},{ny}로')

            moving_count += 1
            dist[idx] = abs(nx-exit_x) + abs(ny-exit_y)
            people[idx] = [nx, ny]
            if (nx, ny) == (exit_x, exit_y) :
                delete_list.append(idx)
    for idx in delete_list :
        del dist[idx]
        del people[idx]

    if people == [] :
        break
    # 2. 출구와 참가자를 포함한 정사각형 구하기

    min_dist = min(dist)
    min_idx = []
    for idx, value in enumerate(dist) :
        if value == min_dist :
            min_idx.append(idx)

    square = make_nemo(min_idx, min_dist)
    # print('square ', square)

    # 3. 정사각형 회전
    small_x, small_y = square[0]
    big_x, big_y = square[-1]

    # 1) 사람과 출구의 값 업데이트
    exit_x, exit_y = update(exit_x, exit_y, small_x, small_y, min_dist)
    for idx, [x,y] in enumerate(people) :
        if small_x <= x <= big_x and small_y <= y <= big_y :
            people[idx] = update(x, y, small_x, small_y, min_dist)

    # 2) 정사각형 내부 회전 및 값 -1
    cnt = small_x
    temp_list = []
    for i in range(small_y, big_y+1) :
        temp = []
        cnt = small_x
        for j in range(small_x, big_x+1) :
            if miro[j][i] > 0 :
                temp.append(miro[j][i]-1)
            else:
                temp.append(miro[j][i])
        temp_list.append(temp[::-1])
    cnt = 0
    for i in range(small_x, big_x+1):
        miro[i] = miro[i][:small_y]+ temp_list[cnt] + miro[i][big_y+1:]
        cnt += 1

    for idx in range(len(dist)) :
        x, y = people[idx]
        dist[idx] = abs(exit_x-x) + abs(exit_y-y)
#     print('최종 people ', people)
#     print('최종 미로 ', miro)
#     print('최종 exit ', exit_x, exit_y)

print(moving_count)
print(f'{exit_x+1} {exit_y+1}')